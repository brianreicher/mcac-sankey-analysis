'''

2. Aggregate the data, counting the number of artists grouped by both nationality and decade.
4. Filter out rows whose artist count is below some threshold. You’ll want to experiment with this
value to produce a visually appealing visualization. I suggest trying a starting threshold around
20.
5. Generate a Sankey diagram with nationality on the left (sources) and decade of birth on the
right (targets)
6. Repeat steps 2-5, but this time count the number of artists grouped by nationality and gender.
Your Sankey diagram will show nationalities on the left and gender on the right.
7. Repeat steps 2-5, grouping by gender and decade. Your Sankey diagram will display gender on
the left and decade of birth on the right.
8. Write a ½ to 1-page interpretation of your results. What insights do you glean from your
visualizations? What does this data science exercise possibly tell us about diversity, inclusion,
and bias in the art world?
'''

import plotly.graph_objects as go
import pandas as pd
from math import floor


class Sankey:

    def __init__(self, filepath='../data/Artists.json', src=None, targ=None, vals=None,
                 desired_columns='all', threshold_value=2):
        self.dataframe = pd.read_json(filepath)
        self.src = src
        self.targ = targ
        self.vals = vals
        self.desired_columns = desired_columns
        self.threshold_value = threshold_value

        # checker bool to see if the dataframe has been cleaned
        self.cleaned = False

    def clean_data(self):
        """ Helper function to clean dataframe values """

        # set dataframe var to avoid using memory space
        if type(self.desired_columns) is str and self.desired_columns.lower() == 'all':
            df = self.dataframe
        else:
            df = self.dataframe[self.desired_columns]

        # drop Null values
        df = df.dropna()

        # check for 'BeginDate' column and use a lambda func to convert all values 'i' to their nearest decade
        # tried using _func() but lambda function showed better performance
        if 'BeginDate' in df.columns:
            df['DecadeBorn'] = df.BeginDate.apply(lambda i: floor(i/10)*10)
            df = df.drop(columns=['BeginDate'])
            df = df[df.DecadeBorn != 0]

        # convert to lowercase for formatting purposes
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].str.lower()

        if 'Nationality' in df.columns:
            df['Nationality'] = df['Nationality'].str.lower()

        self.dataframe = df
        self.cleaned = True

    # TODO
    def group_df(self):
        # if dataframe isn't cleaned, then clean it
        if self.cleaned is False:
            self.clean_data()
        df = self.dataframe

        # Group By category, count by size(), and filter if size() isn't above a threshold
        df = df.groupby([self.src, self.targ]).size()
        df = df[(df.counts >= self.threshold_value)]
        self.dataframe = df
        return self.dataframe

    def _code_mapping(self) -> list:
        """Maps labels/strings in self.src and self.targ and converts them into integers"""

        # Extract distinct labels
        labels = sorted(list(set(list(self.dataframe[self.src]) +
                                 list(self.dataframe[self.targ]))))

        # define integer codes
        codes = list(range(len(labels)))

        # pair labels with list
        lc_map = dict(zip(labels, codes))

        # in df, substitute codes for labels
        self.df = self.dataframe.replace({self.src: lc_map, self.targ: lc_map})
        return labels

    def make_sankey(self, **kwargs) -> None:
        """ Function to generate sankey diagrams"""
        labels = self._code_mapping()
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



