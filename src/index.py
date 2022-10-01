"""
File: index.py

Description: a simple script for testing Sankey API

Author: Brian Reicher
"""

import sankey


def main() -> None:
    """
        Tester for single-level Sankey examples
    """
    # Nationality - Birth Decade Plot
    sankey.Sankey(src='Nationality', targ='DecadeBorn', vals='counts',
                  desired_columns=['Nationality', 'BeginDate']).make_sankey()

    # Nationality - Gender Plot
    sankey.Sankey(src='Nationality', targ='Gender', vals='counts',
                  desired_columns=['Nationality', 'Gender'], threshold_value=30).make_sankey()

    # Gender - Birth Decade Plot
    sankey.Sankey(src='Gender', targ='DecadeBorn', vals='counts',
                  desired_columns=['Gender', 'BeginDate']).make_sankey()

    # Multi-layer Plot
    sankey.Sankey(src=['Nationality', 'DecadeBorn'], targ=['DecadeBorn', 'Gender'], vals='counts',
                  desired_columns=['Gender', 'Nationality', 'BeginDate'], threshold_value=50).make_sankey()


if __name__ == '__main__':
    main()

