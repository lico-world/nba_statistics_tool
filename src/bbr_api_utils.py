from time import sleep
from urllib.request import urlopen

import constants.constants as constants


def getPlayerStat(playerID, gameList, stat):
    url = 'https://www.basketball-reference.com/players/h/halibty01.html'
    try:
        html = urlopen(url)
        sleep(constants.DELAY)
    except Exception as e:
        if constants.ERROR_VERBOSE:
            print(constants.WARNING, 'WARNING /!\\ request at ', constants.NORMAL, url)
