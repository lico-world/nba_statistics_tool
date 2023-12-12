from icecream import ic

from src.nba_tool import NBATool
import constants.constants as constants

import src.bbr_api_utils as bbr


def main():
    constants.VERBOSE = True
    nbaTool = NBATool()

    # Use example
    # ic(nbaTool.getPlayerStats('Tyrese Haliburton', ['PTS', 'AST', 'TOV', 'PLUS_MINUS'],
    #                           ['NOV 19, 2023', 'NOV 14, 2023', 'NOV 12, 2023']))

    ic(bbr.getPlayerStat('Alperen Sengun', 'TS'))


if __name__ == '__main__':
    main()
