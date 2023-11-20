import constants.constants as constants
import pandas as pd

import src.nba_api_utils as nba_utils


class NBATool:
    def __init__(self):
        if constants.VERBOSE:
            print('NBA Tool ' + constants.VALIDATE + 'instantiated' + constants.NORMAL)

        # Will store all the stats asked by the user
        self._nbatool__wantedStats = []

        # Will store all the results of the requests
        self._nbatool__resultData = pd.DataFrame()

        # Set the equivalence between the wanted stat and the function that will compute it
        # This implementation might seem using useless steps but it will make sens when some stats will require other
        # functions to be called than getPlayerStat
        self._nbatool__statsFunction = {
            'PTS': nba_utils.getPlayerStat,
            'AST': nba_utils.getPlayerStat,
            'MIN': nba_utils.getPlayerStat,
            'FGM': nba_utils.getPlayerStat,
            'FGA': nba_utils.getPlayerStat,
            'FG_PCT': nba_utils.getPlayerStat,
            'FG3M': nba_utils.getPlayerStat,
            'FG3A': nba_utils.getPlayerStat,
            'FG3_PCT': nba_utils.getPlayerStat,
            'FTM': nba_utils.getPlayerStat,
            'FTA': nba_utils.getPlayerStat,
            'FT_PCT': nba_utils.getPlayerStat,
            'OREB': nba_utils.getPlayerStat,
            'DREB': nba_utils.getPlayerStat,
            'REB': nba_utils.getPlayerStat,
            'STL': nba_utils.getPlayerStat,
            'BLK': nba_utils.getPlayerStat,
            'TOV': nba_utils.getPlayerStat,
            'PF': nba_utils.getPlayerStat,
            'PLUS_MINUS': nba_utils.getPlayerStat
        }

        # Repartition of the supported statistics among the used APIs
        self._nbatool__supportedStats = self._nbatool__statsFunction.keys()

    def getPlayerStats(self, player, stats, gamesList):
        # If the given player is not an int
        if not isinstance(player, int):
            # Try to get the ID
            playerID = nba_utils.getPlayerID(player)
        else:
            playerID = player  # Maybe verifying the ID?

        # Only keep the supported stats
        self._nbatool__wantedStats = [stat for stat in stats if
                                      (stat is not None and stat in self._nbatool__supportedStats)]

        # Call all the functions
        for stat in self._nbatool__wantedStats:
            self._nbatool__resultData[stat] = self._nbatool__statsFunction[stat](playerID, gamesList, stat)

        return self._nbatool__resultData
