import src.nba_api_utils as nba_utils
import constants.constants as constants
import validation_constants_test as validation_values

from icecream import ic

from test_utils import printTest


def testIDGetters():
    test = True

    # Reference values were get on nba.com
    # Test on stats values are done on previous season to keep tests stable
    test &= printTest(nba_utils.getPlayerID('Jimmy Butler') == 202710, message='Get Player ID')
    test &= printTest(nba_utils.getPlayerID('Kilian Vincent') is None, message='Get Player ID with wrong name')
    test &= printTest(nba_utils.getTeamID('IND') == 1610612754, message='Get Team ID')
    test &= printTest(nba_utils.getTeamID('CPB') is None, message='Get Team ID with wrong acronym')
    test &= printTest(abs(round(nba_utils.getTSPlus('Jimmy Butler', 2019)) - 104) <= 1, message='Get TS+')
    test &= printTest(nba_utils.getTSPlus('Jimmy Butler', '201920') is None, message='Get TS+ handling wrong format')
    test &= printTest(nba_utils.getTSPlus('Jimmy Butler', '1995') is None,
                      message='Get TS+ handling season not played by player')
    test &= printTest(nba_utils.getTSPlus('Kilian Vincent', 2019) is None, message='Get TS+ handling wrong player')

    # Return the value for continuity of unit tests
    return test


def testGetListsValues():
    test = True

    # Reference values were get on nba.com
    # Test on stats values are done on previous season to keep tests stable
    test &= printTest(nba_utils.shotChartData(nba_utils.getPlayerID('Jimmy Butler'), '0022300200')
                      .compare(validation_values.VALIDATE_SHOT_MAP).empty, message='Get Shot Map', separation=True)

    test &= printTest(nba_utils.shotChartData(nba_utils.getPlayerID('Jimmy Butler'), 'A0022300200') is None,
                      message='Get Shot Map with wrong ID')

    test &= printTest(nba_utils.getTeamGames(nba_utils.getTeamID('BOS'),
                                             ['2023-11-15', '2023-11-14', '2023-11-13', '2023-11-12', '2023-11-11'])
                      == validation_values.VALIDATE_GAME_DATE_LIST,
                      message='Get Team Games (dates with games and other dates without game)')

    test &= printTest(nba_utils.getTeamGames(nba_utils.getTeamID('TEAM'), ['2023-11-15', '2023-11-14', '2023-11-13',
                                                                           '2023-11-12', '2023-11-11']) is None,
                      message='Get Team Games without wrong team ID')

    test &= printTest(nba_utils.getTeamGames(nba_utils.getTeamID('BOS'), ['11-15-2023', '11-14-2023', '11-13-2023',
                                                                          '11-12-2023', '11-11-2023']) is None,
                      message='Get Team Games without wrong format dates')

    test &= printTest(nba_utils.getDateGames('2023-11-16') == validation_values.VALIDATE_DATE_GAMES_LIST,
                      message='Get Date Games')

    test &= printTest(nba_utils.getDateGames('11-16') is None,
                      message='Get Date Games with wrong date')

    test &= printTest(nba_utils.getPlayerStats('Jimmy Butler', ['PTS', 'DREB'], dropCurrentSeason=True)
                      .compare(validation_values.VALIDATE_PLAYER_STATS).empty, message='Get Player Stats')

    test &= printTest(nba_utils.getPlayerStats('Jimmy Butler', ['PTS', 'DREB', 'GOALS'], dropCurrentSeason=True)
                      .compare(validation_values.VALIDATE_PLAYER_STATS).empty,
                      message='Get Player Stats with wrong stats')

    test &= printTest(nba_utils.getPlayerStats('Jimmy Butler', [], dropCurrentSeason=True)
                      .empty, message='Get Player Stats with no stats')

    test &= printTest(nba_utils.getPlayerStats('Kilian Vincent', ['PTS', 'DREB'], dropCurrentSeason=True)
                      is None, message='Get Player Stats with wrong player')

    return test


def runNBAUtilsTest():
    ic.disable()  # To avoid usual debug ic printing if a tests require an error to tests the behavior
    constants.ERROR_VERBOSE = False  # To avoid usual error printing if a tests require an error to tests the behavior

    # Boolean tests continuity flag
    test = True

    # Unit tests
    test &= printTest(testIDGetters(), message='ID Getters', separation=True)
    test &= printTest(testGetListsValues(), message='List Values Getters', separation=True)

    ic.enable()  # Allow again debug ic printing
    constants.ERROR_VERBOSE = True  # Allow again error printing

    # Return the final test value
    return test


if __name__ == '__main__':
    # Final nba_utils tests result
    runNBAUtilsTest()
