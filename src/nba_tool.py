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
        self._nbatool__statsFunction = {
            'PTS': nba_utils.getPlayerPTS,
            'AST': nba_utils.getPlayerAST
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
            self._nbatool__resultData[stat] = self._nbatool__statsFunction[stat](playerID, gamesList)

        return self._nbatool__resultData
