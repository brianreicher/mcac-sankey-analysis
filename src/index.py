import sankey


def main():
    return sankey.Sankey(src='Nationality', targ='DecadeBorn', vals='count', desired_columns=['Nationality', 'BeginDate']).make_sankey()


if __name__ == '__main__':
    main()
