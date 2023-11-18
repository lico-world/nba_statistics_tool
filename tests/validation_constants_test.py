import pandas as pd

VALIDATE_SHOT_MAP = pd.DataFrame(columns=['x', 'y', 'type'])
VALIDATE_SHOT_MAP.x = [-6.0, -233.0, -59.0, 89.0, 227.0, 5.0, 13.0, 74.0, 10.0, 15.0, 96.0, -6.0, -218.0, -114.0,
                       -107.0, 47.0, -6.0, 241.0, -9.0]
VALIDATE_SHOT_MAP.y = [-11.0, -75.0, -6.0, -0.0, -133.0, -79.0, -58.0, -59.0, -220.0, -1.0, 7.0, -4.0, -131.0, -233.0,
                       -16.0, -3.0, -45.0, -114.0, -38.0]
VALIDATE_SHOT_MAP.type = ['Made Shot'] * 12 + ['Missed Shot'] * 7

VALIDATE_GAME_DATE_LIST = ['0022300194', '0022300188', '0022300174']
VALIDATE_DATE_GAMES_LIST = ['0022300200', '0022300201']

VALIDATE_PLAYER_STATS = pd.DataFrame(columns=['PTS', 'DREB'])
VALIDATE_PLAYER_STATS.PTS = [109, 705, 878, 1301, 1399, 1816, 1307, 213, 1002, 1215, 1157, 1116, 1219, 1466]
VALIDATE_PLAYER_STATS.DREB = [33, 192, 243, 265, 279, 341, 235, 36, 185, 221, 280, 265, 234, 234]
