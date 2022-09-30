"""
File: sankey.py

Description: A plotly & pandas wrapper API for generating Sankey & multi-layer Sankey diagrams

Author: Brian Reicher
"""

import plotly.graph_objects as go
import pandas as pd
from math import floor


class Sankey:
    """
        Sankey API for developing single & multi-layer sankey diagrams given various data formats

        :param filepath
            File path relative to the API wrapper to pull sankey data from
        :param src
        :param targ
        :param vals
        :param desired_columns
        :param threshold_value
    """
    def __init__(self, filepath='../data/Artists.json', src=None, targ=None, vals=None,
                 desired_columns='all', threshold_value=20):
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
            :rtype: None
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
            # started building a class function but lambda function showed better performance
            df['DecadeBorn'] = df.BeginDate.apply(lambda i: floor(i/10)*10)
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
        """Groups dataframe by src & targ columns, while filtering counts underneath a threshold"""
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
        """Maps labels/strings in self.src and self.targ and converts them into integers"""
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

    def make_sankey(self, **kwargs):
        """ Function to generate sankey diagrams"""
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

        sankey: go.Sankey = go.Sankey(link=link, node=node)
        fig: go.Figure = go.Figure(sankey)
        fig.show()

    def make_multilayer_sankey(self) -> None:
        """ Function to generate multi-layered Sankey diagrams"""
        # assignment to save memory, check if data is cleaned
        if self.is_cleaned is False:
            self._clean_data()
        df = self.dataframe

        # list all src and targ destinations using list comprehensions
        sources = [df[i] for i in self.src]
        targs = [df[j] for j in self.targ]
