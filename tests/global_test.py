import constants.constants as constants
from test_utils import printTest

from nba_api_utils_test import runNBAUtilsTest


def runTest():
    constants.VERBOSE = False
    constants.ERROR_VERBOSE = False

    testResult = True

    testResult &= printTest(runNBAUtilsTest(), message='NBA Utils Functions', separation=True)

    constants.ERROR_VERBOSE = True

    return testResult


if __name__ == '__main__':
    printTest(runTest(), message=constants.CYAN + 'All Tests', separation=True)
