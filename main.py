from icecream import ic

from src.nba_tool import NBATool
import constants.constants as constants


def main():
    constants.VERBOSE = True
    nbaTool = NBATool()

    # Use example
    ic(nbaTool.getPlayerStats('Tyrese Haliburton', ['PTS', 'AST', 'TOV', 'PLUS_MINUS'],
                              ['NOV 19, 2023', 'NOV 14, 2023', 'NOV 12, 2023']))


if __name__ == '__main__':
    main()
