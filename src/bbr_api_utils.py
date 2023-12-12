import math

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver  # Selenium needed because dynamic webpages
from selenium.webdriver.chrome.options import Options
from icecream import ic
from io import StringIO, BytesIO

import constants.constants as constants

# Used to select data in the dataframe
statType = {
    'TS': 'Shooting %'
}

# Used to get the good table in the webpage source code
statTable = {
    'TS': 'adj_shooting'
}


def getPlayerStat(playerName, stat):
    # URL construction
    familyName = playerName.split()[1].lower()
    firstLetterFamN = familyName[0]
    firstLettersFirN = playerName[0:2].lower()
    url = 'https://www.basketball-reference.com/players/' + firstLetterFamN + '/' + familyName[:5]\
          + firstLettersFirN + '01.html'

    try:
        option = Options()
        option.add_argument('--headless')  # To avoid opening the browser

        driver: webdriver.Chrome = webdriver.Chrome(options=option)
        driver.get(url)

        html = driver.page_source  # Get the source code of the page
    except Exception as e:
        if constants.ERROR_VERBOSE:
            print(constants.WARNING, 'WARNING /!\\ request at ', constants.NORMAL, url)
        return None

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.select_one('table#' + statTable[stat])
    table = pd.read_html(StringIO(str(div)))[0][statType[stat]][stat]

    result = []
    for t in table:
        if t is None or math.isnan(t):
            break
        result.append(t)

    driver.quit()

    return result
