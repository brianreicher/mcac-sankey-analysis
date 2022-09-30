"""
File: index.py

Description: a simple script for testing my Sankey API

Author: Brian Reicher
"""
import sankey


def main():
    return sankey.Sankey(src='Gender', targ='DecadeBorn', vals='counts', desired_columns=['BeginDate', 'Gender']).make_sankey()


if __name__ == '__main__':
    main()
