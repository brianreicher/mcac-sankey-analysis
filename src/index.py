"""
File: index.py

Description: a simple script for testing my Sankey API

Author: Brian Reicher
"""

import sankey


def main():
    # Nationality - Birth Decade Plot
    sankey.Sankey(src='Nationality', targ='DecadeBorn', vals='counts',
                  desired_columns=['Nationality', 'BeginDate']).make_sankey()

    # Nationality - Gender Plot
    sankey.Sankey(src='Nationality', targ='Gender', vals='counts',
                  desired_columns=['Nationality', 'Gender']).make_sankey()

    # Gender - Birth Decade Plot
    sankey.Sankey(src='Gender', targ='DecadeBorn', vals='counts',
                  desired_columns=['Gender', 'BeginDate']).make_sankey()


def multi():
    sankey.Sankey(src=['Nationality', 'DecadeBorn'], targ='DecadeBorn', vals='counts',
                  desired_columns=['Nationality', 'BeginDate']).make_multilayer_sankey()


if __name__ == '__main__':
     main()
