import pandas as pd
import time
import re

from nba_api.stats.endpoints import *
from nba_api.stats.static import *
from nba_api.stats.endpoints import leaguegamefinder

from icecream import ic

import constants.constants as constants


def getPlayerID(playerName):
    for player in players.players:
        if playerName in player:
            return player[0]  # If player is found
    if constants.VERBOSE:
        print(constants.FAIL + 'ERROR /!\\ Invalid Player Name')
    return None  # If player is not found


def getTeamID(teamAbbreviation):
    for team in teams.teams:
        if teamAbbreviation in team:
            return team[0]  # If team is found
    if constants.VERBOSE:
        print(constants.FAIL + 'ERROR /!\\ Invalid Team Acronym')
    return None  # If team is not found


def getTSPlus(playerID, seasonID):
    # TS% formula: PTS / (2 * (FGA + 0.44 * FTA))
    # TS+ formula: 100 * TS% / TSl%
    # (TSl% is the TS% of the league /!\ NOT THE AVERAGE TS%)

    # Be sure the season is in string format (to allow calling with int)
    seasonID = str(seasonID)

    # Season formatting if the value is incorrect
    # (but in the following format : if just 2018 is given, 2018-19 will be written)
    if '-' not in seasonID and len(seasonID) == 4:
        seasonID += '-' + str(int(seasonID[-2:]) + 1)[-2:]

    # If format was not expected
    elif ('-' not in seasonID and len(seasonID) != 4) or ('-' in seasonID and len(seasonID) != 7):
        if constants.VERBOSE:
            print(constants.FAIL + 'ERROR /!\\ Season format unexpected' + constants.NORMAL + ' season used : '
                  + seasonID + ' but expected : XXXX-XX or XXXX with X a number between 0 and 9')
        return None

    try:
        # Get the player career stats
        datePlayer = playercareerstats.PlayerCareerStats(getPlayerID(playerID)).get_data_frames()[0]
    except Exception as e:
        ic(e)   # Debug the exception
        return

    # Only keep the useful stats for the TS+ formula
    datePlayer = datePlayer.filter(items=['FGA', 'FTA', 'PTS', 'SEASON_ID'])
    datePlayer = datePlayer.where(datePlayer.SEASON_ID == seasonID).dropna().reset_index(drop=True)

    # Number of teams the player played for in this season
    nbTeamsInSeason = len(datePlayer.PTS)

    if nbTeamsInSeason > 1:
        for team in range(nbTeamsInSeason, 1, -1):  # Starting by the last index
            # If player played in several teams in this year: concatenate all the stats
            datePlayer.PTS[0] += datePlayer.PTS[team]
            datePlayer.FGA[0] += datePlayer.FGA[team]
            datePlayer.FTA[0] += datePlayer.FTA[team]

            # Drop the last line of the dataframe
            datePlayer.drop(team)

    elif nbTeamsInSeason < 1:
        # If player wasn't on the league during this season
        if constants.VERBOSE:
            print(constants.FAIL + 'KEY ERROR /!\\' + constants.NORMAL + ' player did not play on ' + seasonID)
        return None

    # Compute the player TS%
    personalTSPercentage = datePlayer.PTS[0] / (2 * (datePlayer.FGA[0] + 0.44 * datePlayer.FTA[0]))

    try:
        # Get the league data for the current season
        leagueData = leaguedashplayerstats.LeagueDashPlayerStats(season=seasonID).get_data_frames()[0]
    except Exception as e:
        ic(e)   # Debug the exception
        return

    # Only keep the useful stats for the TS+ formula
    leagueData = leagueData.filter(items=['FGA', 'FTA', 'PTS'])
    nbPlayer = len(leagueData.PTS)

    # Calculate the various averages required for the TS% formula
    average = {'PTS': 0, 'FGA': 0, 'FTA': 0}
    for p in range(nbPlayer):
        average['PTS'] += leagueData.PTS[p]
        average['FGA'] += leagueData.FGA[p]
        average['FTA'] += leagueData.FTA[p]

    leagueAverageTSPercentage = average['PTS'] / (2 * (average['FGA'] + 0.44 * average['FTA']))

    # Compute the final result
    TSPlus = 100 * personalTSPercentage / leagueAverageTSPercentage

    return TSPlus


def shotChartData(playerID, gameID):
    # Initialisation of the two dataframe for the two types of shoots
    positionsMade = pd.DataFrame(columns=['x', 'y', 'type'])
    positionsMiss = pd.DataFrame(columns=['x', 'y', 'type'])

    try:
        # API request for the data
        gameDataPlayByPlay = playbyplayv3.PlayByPlayV3(gameID).get_data_frames()[0]
    except Exception as e:
        ic(e)
        return None

    # Keep: actionType to differentiate missed and made shot
    #       personId to select only one player
    #       xLegacy and yLegacy to get the shot positions
    gameDataPlayByPlay = gameDataPlayByPlay.filter(items=['actionType', 'personId', 'xLegacy', 'yLegacy'])

    # Keep only action that are missed or made shot
    gameDataPlayByPlay = gameDataPlayByPlay.where((gameDataPlayByPlay['actionType'] == 'Made Shot') |
                                                  (gameDataPlayByPlay['actionType'] == 'Missed Shot'))\
        .where(gameDataPlayByPlay['personId'] == playerID).dropna().reset_index(drop=True)

    # Split missed and made shot
    dataForMadeShot = gameDataPlayByPlay.where(gameDataPlayByPlay['actionType'] == 'Made Shot')\
        .dropna().reset_index(drop=True)
    dataForMissedShot = gameDataPlayByPlay.where(gameDataPlayByPlay['actionType'] == 'Missed Shot')\
        .dropna().reset_index(drop=True)

    # Putting made values in the previously created dataframe to make easy the concatenation
    positionsMade['x'] = dataForMadeShot['xLegacy']
    positionsMade['y'] = dataForMadeShot['yLegacy'] * -1  # *-1 because the image is 180° turned
    positionsMade['type'] = dataForMadeShot['actionType']

    # Putting missed values in the previously created dataframe to make easy the concatenation
    positionsMiss['x'] = dataForMissedShot['xLegacy']
    positionsMiss['y'] = dataForMissedShot['yLegacy'] * -1  # *-1 because the image is 180° turned
    positionsMiss['type'] = dataForMissedShot['actionType']

    # Concatenate the final values for plotting
    shotPlot = pd.concat([positionsMade.assign(dataset='Made'), positionsMiss.assign(dataset='Missed')])\
        .filter(items=['x', 'y', 'type']).reset_index(drop=True)

    ic(shotPlot)

    return shotPlot


def getTeamGames(teamID, dates):
    gamesID = []

    # Verifying the team ID and dates non-nullity
    if teamID is None:
        if constants.VERBOSE:
            print(constants.FAIL + 'ERROR /!\\ Invalid Team ID')
        return None
    elif dates is None:
        if constants.VERBOSE:
            print(constants.FAIL + 'ERROR /!\\ Invalid Dates List')
        return None

    # Verifying dates format
    for date in dates:
        if not re.match('^\\d{4}-\\d{2}-\\d{2}$', date):
            if constants.VERBOSE:
                print(constants.FAIL + 'ERROR /!\\ Wrong date format!' + constants.NORMAL + ' Expected YYYY-MM-DD')
            return None

    try:
        # Delay to not spam
        time.sleep(constants.DELAY)
        allGamesList = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamID)
    except Exception as e:
        ic(e)  # Debug the exception
        return

    # Keep only games IDs and dates on a dataframe
    gamesData = allGamesList.get_data_frames()[0]
    gamesData = gamesData.filter(items=['GAME_ID', 'GAME_DATE'])

    # Nullification of all the non-wanted games
    for index, date in enumerate(gamesData.GAME_DATE):
        if date not in dates:
            gamesData.GAME_ID[index] = None

    # Put all the non-null values on the gamesID array
    for game in gamesData.GAME_ID:
        if game not in gamesID and game is not None:
            gamesID.append(game)

    return gamesID


def getDateGames(wantedDate):
    gamesID = []

    # Verifying date format
    if not re.match('^\\d{4}-\\d{2}-\\d{2}$', wantedDate):
        if constants.VERBOSE:
            print(constants.FAIL + 'ERROR /!\\ Wrong date format!' + constants.NORMAL + ' Expected YYYY-MM-DD')
        return None

    # Checking all teams
    for team in constants.TEAM_ABBREVIATIONS:
        teamID = getTeamID(team)
        try:
            time.sleep(constants.DELAY)
            allGamesList = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamID)
        except Exception as e:
            ic(e)
            return None

        # Keeping only IDs and dates where the date is the wanted one
        gamesData = allGamesList.get_data_frames()[0]
        gamesData = gamesData.filter(items=['GAME_ID', 'GAME_DATE']).where(gamesData.GAME_DATE == wantedDate) \
            .dropna().reset_index(drop=True)

        # Formatting the returned data structure with only games IDs
        for game in gamesData.GAME_ID:
            if game not in gamesID:
                gamesID.append(game)

    return gamesID


def getPlayerStats(playerName, stats, dropCurrentSeason=False):
    try:
        # Request all the player career stats
        career = playercareerstats.PlayerCareerStats(getPlayerID(playerName))
    except Exception as e:
        ic(e)  # Debug the exception
        return None

    dataframe = career.get_data_frames()[0]

    # Keep only asked stats
    dataframe = dataframe.filter(items=stats)

    ic(dataframe)

    # If only finished seasons are wanted
    if dropCurrentSeason:
        dataframe.drop(dataframe.index[-1], axis=0, inplace=True)

    ic(dataframe)

    return dataframe


def getGapData(gameSeed):
    try:
        time.sleep(0.5)
        game = playbyplay.PlayByPlay(gameSeed)
        team = playbyplayv3.PlayByPlayV3(gameSeed)
    except Exception as e:
        ic(e)
        return

    tm = []

    d_t = team.get_data_frames()[0].filter(items=['teamTricode'])
    tm.append(str(d_t.teamTricode[1]))
    d_t = d_t.mask(d_t == tm[0]).dropna().reset_index(drop=True)
    tm.append(str(d_t.teamTricode[1]))

    data = game.get_data_frames()[0].filter(items=['PCTIMESTRING', 'PERIOD', 'SCOREMARGIN']).dropna().reset_index(
        drop=True)

    qt_duration = 720
    t = 0
    for _ in data['PCTIMESTRING']:
        data.loc[t, 'PCTIMESTRING'] = int(data['PERIOD'][t]) * qt_duration - \
                                      (int(data['PCTIMESTRING'][t].split(':')[0]) * 60 +
                                       int(data['PCTIMESTRING'][t].split(':')[1]))

        if data['SCOREMARGIN'][t] == 'TIE':
            data.loc[t, 'SCOREMARGIN'] = '0'
        t += 1

    data = data.filter(items=['PCTIMESTRING', 'SCOREMARGIN']).rename(
        columns={'PCTIMESTRING': 'Time', 'SCOREMARGIN': 'Gap'})

    data['Time'] = data['Time'].astype(float)
    data['Gap'] = data['Gap'].astype(float)

    return data, tm
