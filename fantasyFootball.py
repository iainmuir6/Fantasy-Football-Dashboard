"""
Iain Muir, iam9ez

Explore ESPN Fantasy Football API

API SUMMARY:

url = https://fantasy.espn.com/apis/v3/games/ffl/seasons/<SEASON>/segments/0/leagues/<LEAGUE_ID>
response = requests.get(url,
                        params=
                            {
                                view: mSettings,
                                view: mMatchup,
                                view: mMatchupScore,
                                scoringPeriodId: week
                            }
                        cookies=
                            {
                                SWID: {<ESPN ID>}
                                espn_s2: '<cookie string>'
                            }

----------------------------------------- Empty Parameters -----------------------------------------

dict_keys(['gameId', 'id', 'members', 'scoringPeriodId', 'seasonId', 'segmentId', 'settings', 'status', 'teams'])
{'members':  [   {
                    'displayName': ESPN User ID,
                    'id': ESPN SWID,
                    'isLeagueManager': boolean
                 }, ...
             ],
 'settings': {
                 'name': League Name
             }
 'teams':    [   {
                    'abbrev': Team Abbreviation,
                    'id': Team ID (1- # of teams),
                    'location': Team Name Pt. 1,
                    'nickname': Team Name Pt. 2,
                    'owners': ['{SWID}', '{SWID}']
                 }, ...
             ], ...
}

----------------------------------------- mSettings Parameter -----------------------------------------
                                        {
                                            'view': 'mSettings'
                                        }

dict_keys(['draftDetail', 'gameId', 'id', 'scoringPeriodId', 'seasonId', 'segmentId', 'settings', 'status'])
{'draftDetail':     {
                        'drafted': boolean,
                        'inProgress': boolean
                    },
 'gameId': int,
 'id': League ID,
 'scoringPeriodId': Current Week,
 'seasonId': Year of Current Season,
 'segmentId': int,
 'settings':        dict_keys(['acquisitionSettings', 'draftSettings', 'financeSettings', 'isCustomizable',
                               'isPublic', 'name', 'restrictionType', 'rosterSettings', 'scheduleSettings',
                               'scoringSettings', 'size', 'tradeSettings'])
}

----------------------------------------- mMatchup Parameter -----------------------------------------
                                {
                                    'view': 'mMatchup',
                                    'scoringPeriodId': week     – optional
                                }


dict_keys(['draftDetail', 'gameId', 'id', 'schedule', 'scoringPeriodId', 'seasonId', 'segmentId', 'status', 'teams'])

{'id': 4,
 'roster': {
                'appliedStatTotal': 69.92,
                 'entries': [{
                                'acquisitionDate': 1597541974161,
                                'acquisitionType': 'DRAFT',
                                'injuryStatus': 'NORMAL',
                                'lineupSlotId': 20,
                                'pendingTransactionIds': None,
                                'playerId': 3117251,
                                'playerPoolEntry': {
                                                        'appliedStatTotal': 0.0,
                                                        'id': 3117251,
                                                        'keeperValue': 1,
                                                        'keeperValueFuture': 1,
                                                        'lineupLocked': False,
                                                        'onTeamId': 4,
                                                        'player': {
                                                                        'active': True,
                                                                        'defaultPositionId': 2,
                                                                        'droppable': False,
                                                                        'eligibleSlots': [2, 3, 23, 7, 20, 21],
                                                                        'firstName': 'Christian',
                                                                        'fullName': 'Christian McCaffrey',
                                                                        'id': 3117251,
                                                                        'injured': False,
                                                                        'injuryStatus': 'DOUBTFUL',
                                                                        'lastName': 'McCaffrey',
                                                                        'lastNewsDate': 1607711569000,
                                                                        'proTeamId': 29,
                                                                        'rankings': {'0': [{
                                                                                                'auctionValue': 0,
                                                                                                'rank': 1,
                                                                                                'rankSourceId': 7,
                                                                                                'rankType': 'STANDARD',
                                                                                                'slotId': 2
                                                                                            }, ...]
                                                                        'stats': [{
                                                                                        'appliedAverage': season avg,
                                                                                        'appliedStats': {
                                                                                                            code: #
                                                                                                        }
                                                                                        'scoringPeriodId': week
                                                                                        'seasonId': year
                                                                                        'statSourceId': 0 – actual
                                                                                                        1 - projected
                                                                                  }, ...]

----------------------------------------- mMatchupScore Parameter -----------------------------------------
                                {
                                    'view': 'mMatchupScore',
                                    'scoringPeriodId': week     – optional
                                }

dict_keys(['draftDetail', 'gameId', 'id', 'schedule', 'scoringPeriodId', 'seasonId', 'segmentId', 'status'])

-----------------------------------------------------------------------------------------------------------

TO DO LIST
    • Team Abbreviations Dictionary {id: abbrev}
    • Player Info
    • Free Agents
"""

from secrets import SWID, ESPN_S2
import streamlit as st
import pandas as pd
import requests
import time

# League of Extraordinary Gentlemen
swid = SWID
espn_s2 = ESPN_S2

slot_codes = {
    0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE',
    6: 'TE', 7: 'OP',  8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',
    12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K',
    18: 'P', 19: 'HC', 20: 'BE', 21: 'IR', 22: '', 23: 'RB/WR/TE'
}
default_codes = {
    1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
}
teamIDs = {
    -16018: "no"
}

leagueID = 1080747
season = 2020

start = time.time()

url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(season) + '/segments/0/leagues/' + str(leagueID) + \
      '?view=mRoster'
response0 = requests.get(url,
                         cookies={"SWID": swid, "espn_s2": espn_s2}).json()

# --------------------------- LEAGUE INFO ---------------------------
url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(season) + "/segments/0/leagues/" + str(leagueID)
response1 = requests.get(url,
                         cookies={"SWID": swid, "espn_s2": espn_s2}).json()

print(response1)
exit(0)

leagueInfo = {}
owners_dict = {}

for member in response1['members']:
    owners_dict[member['id']] = member['displayName']

for team in response1['teams']:
    leagueInfo[team['id']] = {'playerName1': owners_dict[team['owners'][0]],
                              'playerName2': owners_dict[team['owners'][1]] if len(team['owners']) == 2 else "N/A",
                              'teamName': team['location'] + " " + team['nickname'],
                              'abbreviation': team['abbrev'],
                              'ownerIDs': team['owners']}

df = pd.DataFrame(list(leagueInfo.values()),
                  columns=['playerName1', 'playerName2', 'teamName', 'abbreviation', 'ownerIDs'])
df.name = response1['settings']['name']

url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(season) + '/segments/0/leagues/' + str(leagueID) + \
      '?view=mSettings'
response2 = requests.get(url,
                         cookies={"SWID": swid, "espn_s2": espn_s2}).json()

rosterSettings = {}
for code, quantity in response2['settings']['rosterSettings']['lineupSlotCounts'].items():
    code = int(code)
    quantity = int(quantity)
    if quantity != 0:
        rosterSettings[slot_codes[code]] = quantity

# --------------------------- WEEKLY DATA ---------------------------

week = response1['scoringPeriodId']

url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(season) + '/segments/0/leagues/' + str(leagueID) + \
      '?view=mMatchup&view=mMatchupScore'

response3 = requests.get(url,
                         params={'scoringPeriodId': week},
                         cookies={"SWID": swid, "espn_s2": espn_s2}).json()

data = []

for team in response3['teams']:
    teamID = team['id']

    if leagueInfo[teamID]['ownerIDs'][0] != swid:
        continue

    # Source: https://stmorse.github.io/journal/espn-fantasy-projections.html
    # Modified: Iain Muir
    for p in team['roster']['entries']:
        name = p['playerPoolEntry']['player']['fullName']
        position = default_codes[p['playerPoolEntry']['player']['defaultPositionId']]
        current = slot_codes[p['lineupSlotId']]
        player_id = p['playerId']

        projected, actual = None, None
        for i, stat in enumerate(p['playerPoolEntry']['player']['stats']):
            print(len(stat))
            if stat['scoringPeriodId'] != week:
                continue
            if stat['statSourceId'] == 0:
                print("Actual", i)
                actual = stat['appliedTotal']
            elif stat['statSourceId'] == 1:
                print("Projected", i)
                projected = stat['appliedTotal']
            print()

        data.append([
            name, player_id, position, current, projected, actual
        ])

    data = pd.DataFrame(data,
                        columns=['Player', 'ID', 'Pos', 'currentPos', 'Proj', 'Actual'])

starters = data.query('currentPos != "BE"')
starters['currentPos'] = pd.Categorical(starters['currentPos'], ['QB', 'RB', 'WR', 'TE', 'RB/WR/TE', 'D/ST', 'K'])
starters = starters.sort_values(by=['currentPos', 'Proj'], ascending=[True, False])

# --------------------------- OPTIMIZED LINEUP ---------------------------

optimized = []

for pos, num in rosterSettings.items():
    if pos == "BE":
        continue
    elif pos == "RB/WR/TE":
        options = data.query("Pos == 'RB' | Pos == 'WR' | Pos == 'TE'")
    else:
        options = data.query("Pos == '" + pos + "'")
    options = options.sort_values(by="Proj", ascending=False)[:num]
    data = data.drop(labels=list(options.index), axis=0)

    for player in options.values:
        player = list(player)
        if (starters['Player'] == player[0]).any():
            player.append(False)
        else:
            player[3] = player[2]
            player.append(True)
        optimized.append(player)

exit(0)

optimized = pd.DataFrame(optimized,
                         columns=['Player', 'ID', 'Pos', 'currentPos', 'Status', 'Proj', 'Actual', 'New'])
optimized['currentPos'] = pd.Categorical(optimized['currentPos'], ['QB', 'RB', 'WR', 'TE', 'RB/WR/TE', 'D/ST', 'K'])
optimized = optimized.sort_values(by=['currentPos', 'Proj'], ascending=[True, False])

starters['Old'] = [False if (optimized['Player'] == list(starter)[0]).any() else True for starter in starters.values]
print(starters)

# --------------------------- STREAMLIT DASHBOARD ---------------------------

st.markdown("<center> <img src='https://espnpressroom.com/us/files/2016/08/Fantasy-Football-App-LOGO-500x405.png' "
            "height='200' /> </center>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center';> Fantasy Lineup Optimization </h1>", unsafe_allow_html=True)
old, new = st.beta_columns(2)
old.markdown("<h3 style='text-align:center';> Current Lineup </h1>", unsafe_allow_html=True)
new.markdown("<h3 style='text-align:center';> Optimized Lineup </h1>", unsafe_allow_html=True)

for p1, p2 in zip(starters.values, optimized.values):
    if p1[2] == 'D/ST':
        src1 = "https://a.espncdn.com/i/teamlogos/nfl/500/" + teamIDs[p1[1]] + ".png"
        src2 = "https://a.espncdn.com/i/teamlogos/nfl/500/" + teamIDs[p2[1]] + ".png"
        height = '50'
    else:
        src1 = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/" + str(p1[1]) + ".png&w=350&h=254"
        src2 = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/" + str(p2[1]) + ".png&w=350&h=254"
        height = '40'

    color1 = 'white'
    color2 = 'white'
    if p1[-1]:
        color1 = 'lightcoral'
    if p2[-1]:
        color2 = 'lightgreen'

    old.markdown("<p style='text-align:left;background-color:" + color1 + ";'> <img src='" + src1 + "' height='" +
                 height + "'/>  (" + p1[2] + ") <b>" + p1[0] + "</b>  -  " + str(round(p1[-3], 2)) + " </p>",
                 unsafe_allow_html=True)
    new.markdown("<p style='text-align:left;background-color:" + color2 + ";'> <img src='" + src2 + "' height='" +
                 height + "'/>  (" + p2[2] + ") <b>" + p2[0] + "</b>  -  " + str(round(p2[-3], 2)) + " </p>",
                 unsafe_allow_html=True)


old.markdown("<p style='text-align:center;font-size:20px;'> <b> Total: " + str(round(starters['Proj'].sum(), 2)) +
             "</b> </p>", unsafe_allow_html=True)
new.markdown("<p style='text-align:center;font-size:20px;'> <b> Total: " + str(round(optimized['Proj'].sum(), 2)) +
             "</b> </p>", unsafe_allow_html=True)

print("   --- Finished in %s seconds ---  " % round(time.time() - start, 4))
