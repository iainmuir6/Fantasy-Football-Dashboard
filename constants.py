"""
Iain Muir, iam9ez

"""

# ------------ FOOTBALL ------------
FFL_LEAGUE_ID = 1080747
FFL_TEAM_ID = 4
FFL_POS_CODES = {
    0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE',
    6: 'TE', 7: 'OP',  8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',
    12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K',
    18: 'P', 19: 'HC', 20: 'BE', 21: 'IR', 22: '', 23: 'RB/WR/TE',
    24: '', 25: 'Rookie'
}
FFL_DEFAULT_CODES = {
    1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
}
FFL_TEAM_MAP = {
    -16001: "atl",
    -16002: "buf",
    -16003: "chi",
    -16004: "cin",
    -16005: "cle",
    -16006: "dal",
    -16007: "den",
    -16008: "det",
    -16009: "gb",
    -16010: "ten",
    -16011: "ind",
    -16012: "kc",
    -16013: "lv",
    -16014: "lar",
    -16015: 'mia',
    -16016: "min",
    -16017: "ne",
    -16018: "no",
    -16019: "nyg",
    -16020: "nyj",
    -16021: "phi",
    -16022: "ari",
    -16023: "pit",
    -16024: "lac",
    -16025: "sf",
    -16026: "sea",
    -16027: "tb",
    -16028: "wsh",
    -16029: "car",
    -16030: "jax",
    -16033: 'bal',
    -16034: 'hou',
}

# ------------ BASKETBALL ------------
FBA_LEAGUE_ID = 1359582180
FBA_TEAM_ID = 5
FBA_POS_CODES = {
    0: 'PG',
    1: 'SG',
    2: 'SF',
    3: 'PF',
    4: 'C',
    5: 'G',
    6: 'F',
    7: 'SG/SF',
    8: 'G/F',
    9: 'PF/C',
    10: 'F/C',
    11: 'UT',
    12: 'BE',
    13: 'IR',
    14: '',
    15: 'Rookie',

    'PG': 0,
    'SG': 1,
    'SF': 2,
    'PF': 3,
    'C': 4,
    'G': 5,
    'F': 6,
    'SG/SF': 7,
    'G/F': 8,
    'PF/C': 9,
    'F/C': 10,
    'UT': 11,
    'BE': 12,
    'IR': 13,
    'Rookie': 15
}

FBA_TEAM_MAP = {
    0: 'FA',
    1: 'ATL',
    2: 'BOS',
    3: 'NOP',
    4: 'CHI',
    5: 'CLE',
    6: 'DAL',
    7: 'DEN',
    8: 'DET',
    9: 'GSW',
    10: 'HOU',
    11: 'IND',
    12: 'LAC',
    13: 'LAL',
    14: 'MIA',
    15: 'MIL',
    16: 'MIN',
    17: 'BKN',
    18: 'NYK',
    19: 'ORL',
    20: 'PHL',
    21: 'PHO',
    22: 'POR',
    23: 'SAC',
    24: 'SAS',
    25: 'OKC',
    26: 'UTA',
    27: 'WAS',
    28: 'TOR',
    29: 'MEM',
    30: 'CHA',
}

FBA_STATS_MAP = {
    '0': 'PTS',
    '1': 'BLK',
    '2': 'STL',
    '3': 'AST',
    '4': 'OREB',
    '5': 'DREB',
    '6': 'REB',
    '7': '',
    '8': '',
    '9': 'PF',
    '10': '',
    '11': 'TO',
    '12': '',
    '13': 'FGM',
    '14': 'FGA',
    '15': 'FTM',
    '16': 'FTA',
    '17': '3PTM',
    '18': '3PTA',
    '19': 'FG%',
    '20': 'FT%',
    '21': '3PT%',
    '22': '',
    '23': '',
    '24': '',
    '25': '',
    '26': '',
    '27': '',
    '28': 'MPG',
    '29': '',
    '30': '',
    '31': '',
    '32': '',
    '33': '',
    '34': '',
    '35': '',
    '36': '',
    '37': '',
    '38': '',
    '39': '',
    '40': 'MIN',
    '41': 'GP',
    '42': '',
    '43': '',
    '44': '',
    '45': '',
}

FBA_ACTIVITY_MAP = {
    178: 'FA ADDED',
    180: 'WAIVER ADDED',
    179: 'DROPPED',
    181: 'DROPPED',
    239: 'DROPPED',
    244: 'TRADED',
    'FA': 178,
    'WAIVER': 180,
    'TRADED': 244
}