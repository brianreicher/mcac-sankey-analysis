"""
File: sankey.py

Description: A plotly & pandas wrapper API for generating Sankey & multi-layer Sankey diagrams

Author: Brian Reicher
"""

import plotly.graph_objects as go
import pandas as pd
import os
from math import floor


class Sankey:
    """
        Sankey API for developing single & multi-layer sankey diagrams given various data formats
    """
    def __init__(self, filepath='../data/Artists.json', src=None, targ=None, vals=None,
                 desired_columns='all', threshold_value=20):
        """
            Constructor class for the Sankey API
            :param filepath:
                File path relative to the API wrapper to pull sankey data from
            :param src:
                Source value(s) for Sankey diagram
            :param targ:
                Target value(s) for Sankey diagram
            :param vals:
                Count values for Sankey diagrams
            :param desired_columns:
                Categories from input data to use for Sankey diagrams
            :param threshold_value:
                Threshold number of paintings in order to include in Sankey diagram
        """
        self.filepath = filepath
        self.dataframe = pd.read_json(filepath)
        self.src = src
        self.targ = targ
        self.vals = vals
        self.columns = desired_columns
        self.threshold = threshold_value

        # checker booleans to see if the dataframe has been cleaned and/or grouped
        self.is_cleaned = False
        self.is_grouped = False

    def _clean_data(self):
        """
            Helper function to throw data through a preprocessing pipeline in order to retrieve the desired
            dataframe columns for sankey sources/targets, as well as format
        """
        # set dataframe var to avoid using memory space
        if type(self.columns) is str and self.columns.lower() == 'all':
            df = self.dataframe
        else:
            df = self.dataframe[self.columns]

        # drop Null values
        df = df.dropna()

        # check for 'BeginDate' column and use a lambda func to convert all values to nearest decade over literal date
        if 'BeginDate' in df.columns:
            # lambda function to drop year 0s, scale to the nearest decade, and scale back up to 4 digits
            df['DecadeBorn'] = df.BeginDate.apply(lambda val: floor(val/10)*10)
            # remove initial 'BeginDate' column
            df = df.drop(columns=['BeginDate'])
            # filter all unknown (zeroed) birth decades
            df = df[df.DecadeBorn != 0]

        # convert any string-based column to lowercase in order to eliminate sankey confusion & redundancies
        for i in df.columns:
            if df[i].dtypes is str:
                df[i] = df[i].str.lower()

        # reassign dataframe element and mark the 'cleaned' checker as True
        self.dataframe = df
        self.is_cleaned = True

    def _group_df(self):
        """
            Helper function to group dataframe by src & targ columns, while filtering counts underneath a threshold
        """
        # if dataframe isn't cleaned, then clean
        if self.is_cleaned is False:
            self._clean_data()

        # assignment to save memory
        df = self.dataframe

        # Group By category, add counts columns by size(), and filter if size() isn't above a threshold
        df = df.groupby([self.src, self.targ]).size().reset_index(name="counts")
        df = df[(df.counts >= self.threshold)]

        # reset index to start from 0
        df.index = range(len(df))
        self.dataframe = df
        self.is_grouped = True

    def _code_mapping(self) -> list:
        """
            Helper function to map labels/strings in src and targ and converts them into integers
            :rtype: list:
        """
        # if dataframe isn't cleaned and grouped, then clean and group
        if self.is_grouped is False:
            self._group_df()

        # assignment to save memory
        df = self.dataframe

        # Extract distinct labels
        labels = list(set(list(df[self.src]) + list(df[self.targ])))

        # define integer codes
        codes = list(range(len(labels)))

        # pair labels with list
        lc_map = dict(zip(labels, codes))

        # in df, substitute codes for labels
        self.df = df.replace({self.src: lc_map, self.targ: lc_map})
        return labels

    def make_sankey(self, **kwargs) -> None:
        """
             Generate sankey or multi-level Sankey diagrams & save as PNG/HTML files
             :param: **kwargs:
                Formatting **kwargs to change visual components of the Sankey diagram
            :rtype: None:
        """
        # set sankey labels via code mapping
        labels = self._code_mapping()

        # check for sankey vals, set to 1 if None
        if self.vals is None:
            self.vals = [1] * len(self.df)

        # Process **kwargs
        pad = kwargs.get('pad', 50)  # get - grabs dict value if it exists, otherwise returns defined value
        thickness = kwargs.get('thickness', 30)
        line_color = kwargs.get('line_color', 'black')
        line_width = kwargs.get('line_width', 1)

        # Init link & node dicts
        link = {'source': self.df[self.src],
                'target': self.df[self.targ],
                'value': self.df[self.vals]}
        node = {'label': labels, 'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': line_width}}

        # set and show desired Sankey plot
        sankey: go.Sankey = go.Sankey(link=link, node=node)
        fig: go.Figure = go.Figure(sankey)
        fig.update_layout(title_text=f'{self.src} vs {self.targ}')
        fig.show()

        # search for image directory in 'data' directory if it exists, else look to create in-spot
        fp = self.filepath
        if 'data' in fp:
            index = fp.index('data') + len('data')
            fp = fp[:index] + '/img/'
        else:
            fp = os.getcwd() + '/img/'

        # try/except to make image directory
        try:
            os.mkdir(fp)
        except FileExistsError:
            pass

        # save figure as an interactive HTML file and PNG, need to pip install kaleido
        fig.write_html(fp + f'{self.src}_{self.targ}_sankey.html')
        fig.write_image(fp + f'{self.src}_{self.targ}_sankey.png')
