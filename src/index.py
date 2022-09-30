import sankey


def main():
    sankey.Sankey(src='Nationality', targ='DecadeBorn').make_sankey()


if __name__ == '__main__':
    main()
