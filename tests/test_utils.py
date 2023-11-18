import constants.constants as constants


def printTest(test_value, message=None, separation=False):
    # If needed a separation in the print can be printed
    if separation:
        print('-' * 25)

    # Get the correct color (green or red)
    RESULT_NATURE = constants.VALIDATE + 'OK!' if test_value else constants.FAIL + 'ERROR!'
    MESSAGE = '' if message is None else message + ': '
    print(MESSAGE + RESULT_NATURE + constants.NORMAL)

    # Return the value for continuity of unit tests
    return test_value
