DELAY = 0.5  # Delay to avoid being considered as spam by the API
BASE_COLOR = '#414a54'

# Colors used to adapt data visualization to the desired teams (primary and secondary color)
TEAM_COLORS = {'CHA': ['#00788C', '#1D1160'],
               'BOS': ['#007A33', '#FFFFFF'],
               'IND': ['#FDBB30', '#002D62'],
               'CLE': ['#860038', '#FDBB30'],
               'MIA': ['#98002E', '#F9A01B'],
               'ORL': ['#C4CED4', '#0077C0'],
               'TOR': ['#B4975A', '#CE1141'],
               'MIL': ['#00471B', '#EEE1C6'],
               'PHI': ['#006BB6', '#ED174C'],
               'CHI': ['#CE1141', '#000000'],
               'BKN': ['#FFFFFF', '#000000'],
               'DET': ['#1D42BA', '#C8102E'],
               'WAS': ['#002B5C', '#E31837'],
               'NYK': ['#F58426', '#006BB6'],
               'ATL': ['#FFFFFF', '#C8102E'],
               'DAL': ['#00538C', '#002B5E'],
               'NOP': ['#85714D', '#0C2340'],
               'PHX': ['#1D1160', '#E56020'],
               'SAC': ['#5A2D81', '#63727A'],
               'DEN': ['#FEC524', '#0E2240'],
               'LAC': ['#C8102E', '#1D428A'],
               'OKC': ['#EF3B24', '#007AC1'],
               'MIN': ['#0C2340', '#78BE20'],
               'HOU': ['#CE1141', '#000000'],
               'LAL': ['#FDB927', '#552583'],
               'POR': ['#000000', '#E03A3E'],
               'UTA': ['#002B5C', '#F9A01B'],
               'GSW': ['#FFC72C', '#1D428A'],
               'MEM': ['#5D76A9', '#12173F'],
               'SAS': ['#C4CED4', '#000000']}

# Team abbreviations used to refer to teams in an intelligible way
TEAM_ABBREVIATIONS = ['CHA',
                      'BOS',
                      'IND',
                      'CLE',
                      'MIA',
                      'ORL',
                      'TOR',
                      'MIL',
                      'PHI',
                      'CHI',
                      'BKN',
                      'DET',
                      'WAS',
                      'NYK',
                      'ATL',
                      'DAL',
                      'NOP',
                      'PHX',
                      'SAC',
                      'DEN',
                      'LAC',
                      'OKC',
                      'MIN',
                      'HOU',
                      'LAL',
                      'POR',
                      'UTA',
                      'GSW',
                      'MEM',
                      'SAS']

FAIL = '\033[91m'       # Code to print in green
WARNING = '\033[33m'    # Code to print in orange
VALIDATE = '\033[92m'   # Code to print in red
NORMAL = '\033[0m'      # Code to print in white
CYAN = '\033[96m'       # Code to print in cyan

ERROR_VERBOSE = True  # Flag to know if we need to print errors or not (useful for tests)
VERBOSE = False  # Flag to know if we need to print extra information or not (useful for tests)
