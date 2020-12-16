"""
Iain Muir, iam9ez

Fantasy Football Classes
"""

import pandas as pd
import requests
import pickle
import time
import json
import os


class EspnApi:
    def __init__(self):
        self.swid = "{94FD803F-87FC-4BDC-BD80-3F87FCEBDCFC}"
        self.espn_s2 = "AEA%2Fs7CAHybhPWiuG5cTGqmfaH2%2F%2FeUCDP5bTDB4j0hDCLGW58ieoYJCnEB9uxNNPrx1CRjc8cuCinM54m2mUnf" \
                       "5PwfVmZ6Xup0Hx1GSpuVoHuTjibfHSbu%2FDM0Zp%2BDhDygZS7zUVRZ1ag7Dm%2F7S2zcys1Ywxf4Fj1mFVKOmnIygFM" \
                       "V1a8LlMRy5W4ZpkvCvJzmQJTZcgfBncMmt1wh5IbsVWJwAm8ElISHA%2F9ooLplPppnKwIi1jbzeJv1UHIuh%2Bio%3D"
        self.league_id = 1080747
        self.season = 2020
        self.week = requests.get(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(self.season) +
                                     '/segments/0/leagues/' + str(self.league_id) + '?view=mSettings',
                                 cookies={
                                     "SWID": self.swid,
                                     "espn_s2": self.espn_s2
                                 }).json()['scoringPeriodId']
        self.slot_codes = {
            0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE',
            6: 'TE', 7: 'OP',  8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',
            12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K',
            18: 'P', 19: 'HC', 20: 'BE', 21: 'IR', 22: '', 23: 'RB/WR/TE',
            24: '', 25: 'Rookie'
        }
        self.default_codes = {
            1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
        }
        self.team_ids = {
            -16018: "no"
        }

    def league_history(self):
        """
        :param self – NONE

        :return list of league_info dictionaries for each year active
        """
        history = requests.get(url="https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(self.league_id),
                               cookies={
                                   "SWID": self.swid,
                                   "espn_s2": self.espn_s2
                               }).json()
        return history

    def league_info(self):
        """
        :param self – NONE

        :return {['gameId', 'id', 'members', 'scoringPeriodId', 'seasonId', 'segmentId', 'settings', 'status', 'teams']}
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
        """
        info = requests.get(url="https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(self.season) +
                                "/segments/0/leagues/" + str(self.league_id),
                            cookies={
                                "SWID": self.swid,
                                "espn_s2": self.espn_s2
                            }).json()
        return info

    def league_settings(self):
        """
        :param self – {
                          'view': 'mSettings'
                      }

        :return {['draftDetail', 'gameId', 'id', 'scoringPeriodId', 'seasonId', 'segmentId', 'settings', 'status']}
                {'draftDetail':     {
                                        'drafted': boolean,
                                        'inProgress': boolean
                                    },
                 'gameId': int,
                 'id': League ID,
                 'scoringPeriodId': Current Week,
                 'seasonId': Year of Current Season,
                 'segmentId': int,
                 'settings':        dict_keys(['acquisitionSettings', 'draftSettings', 'financeSettings',
                                               'isCustomizable', 'isPublic', 'name', 'restrictionType',
                                               'rosterSettings', 'scheduleSettings','scoringSettings',
                                               'size', 'tradeSettings'])
                }
        """
        settings = requests.get(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(self.season) +
                                    '/segments/0/leagues/' + str(self.league_id) + '?view=mSettings',
                                cookies={
                                    "SWID": self.swid,
                                    "espn_s2": self.espn_s2
                                }).json()
        return settings

    def get_roster(self, team_id):
        """
        :param

        :return
        """
        team = requests.get(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(self.season) +
                                '/segments/0/leagues/' + str(self.league_id) + '?view=mRoster',
                            params={
                                'scoringPeriodId': self.week
                            },
                            cookies={
                                "SWID": self.swid,
                                "espn_s2": self.espn_s2
                            }).json()['teams'][team_id - 1]

        roster = [
            [
                p['playerPoolEntry']['player']['fullName'],
                p['playerId'],
                self.default_codes[p['playerPoolEntry']['player']['defaultPositionId']],
                self.slot_codes[p['lineupSlotId']],
                [round(stat['appliedTotal'], 2)
                 for stat in p['playerPoolEntry']['player']['stats']
                 if stat['scoringPeriodId'] == self.week and stat['statSourceId'] == 1][0],
                [round(stat['appliedTotal'], 2)
                 for stat in p['playerPoolEntry']['player']['stats']
                 if stat['scoringPeriodId'] == self.week and stat['statSourceId'] == 0]
            ]
            for p in team['roster']['entries']
        ]
        return pd.DataFrame(roster, columns=['Name', 'playerID', 'defaultPosition',
                                             'currentPosition', 'projected', 'actual'])

    def get_free_agents(self):
        """
        :param

        :return
        """
        filters = {"players":
                       {"filterStatus":
                            {"value": ["FREEAGENT", "WAIVERS"]},
                        # "filterSlotIds":{"value": slot_filter},
                        "limit": 50,
                        "sortPercOwned":
                            {"sortPriority": 1,
                             "sortAsc": False},
                        "sortDraftRanks": {"sortPriority": 100,
                                           "sortAsc": True,
                                           "value": "STANDARD"}}}
        headers = {'x-fantasy-filter': json.dumps(filters)}
        free_agents = requests.get(url='https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(self.season) +
                                       '/segments/0/leagues/' + str(self.league_id) + '?view=kona_player_info',
                                   params={
                                       'scoringPeriodId': self.week
                                   },
                                   cookies={
                                       "SWID": self.swid,
                                       "espn_s2": self.espn_s2
                                   },
                                   headers=headers).json()['players']
        free_agents = [
            [
                p['player']['fullName'],
                p['player']['id'],
                self.default_codes[p['player']['defaultPositionId']],
                round(p['player']['stats'][4 if len(p['player']['stats']) == 6 else 3]['appliedTotal'], 2)
            ]
            for p in free_agents
        ]
        return pd.DataFrame(free_agents, columns=['Name', 'playerID', 'defaultPosition', 'projected'])


class FantasyLeague:
    def __init__(self):
        self.name = client.league_info()['settings']['name']
        self.members = {member['id']: member['displayName'] for member in client.league_info()['members']}
        self.teams = [{team['id']: {'names': [self.members[swid] for swid in team['owners']],
                                    'ownerIDs': team['owners'],
                                    'teamName': team['location'] + " " + team['nickname'],
                                    'abbreviation': team['abbrev']
                                    }} for team in client.league_info()['teams']]
        self.teamObjects = []
        self.memberObjects = []
        for team in self.teams:
            tm_id, info = list(team.keys())[0], list(team.values())[0]
            self.teamObjects.append(FantasyTeam(tm_id, info))
            for name, swid in zip(info['names'], info['ownerIDs']):
                self.memberObjects.append(LeagueMember(name, info['teamName'], swid, len(info['names']) != 1))

        self.roster_settings = {client.slot_codes[int(code)]: quantity
                                for code, quantity
                                in client.league_settings()['settings']['rosterSettings']['lineupSlotCounts'].items()}

    def update_teams(self):
        for i, team in enumerate(self.teamObjects):
            team.roster = client.get_roster(i+1)


class FantasyTeam:
    def __init__(self, team_id, team_info):
        self.id = team_id
        self.name = team_info['teamName']
        self.owners = team_info['names']
        self.roster = client.get_roster(team_id)

    def dashboard(self):
        roster_settings = {client.slot_codes[int(c)]: q for c, q in
                           client.league_settings()['settings']['rosterSettings']['lineupSlotCounts'].items() if q != 0}
        options = self.roster.drop(axis=1, labels=['currentPosition', 'actual']).append(client.get_free_agents()). \
            reset_index().drop(axis=1, labels='index')
        for position, number in roster_settings.items():
            if position == "BE":
                continue
            else:
                print(options.query('defaultPosition == "' + position + '"').sort_values(by='projected',
                                                                                         ascending=False).head(number))


class LeagueMember:
    def __init__(self, name, team, swid, co):
        self.name = name
        self.team = team
        self.swid = swid
        self.co_coach = co


class Player:
    def __init__(self):
        pass


client = EspnApi()

start = time.time()

league_name = client.league_info()['settings']['name']
if not os.path.exists("/Users/iainmuir/PycharmProjects/Desktop/espnFantasyFootball/leaguePickles/" +
                      league_name + ".pickle"):
    league = FantasyLeague()
    pickle.dump(league, open("/Users/iainmuir/PycharmProjects/Desktop/espnFantasyFootball/leaguePickles/" +
                             league_name + ".pickle", 'wb'))
    print("League Created:", league_name)


else:
    league = pickle.load(open("/Users/iainmuir/PycharmProjects/Desktop/espnFantasyFootball/leaguePickles/" +
                         league_name + ".pickle", 'rb'))
    # league.update_teams()

    league.teamObjects[4].dashboard()

    pickle.dump(league, open("/Users/iainmuir/PycharmProjects/Desktop/espnFantasyFootball/leaguePickles/" +
                             league_name + ".pickle", 'wb'))

print("   --- Finished in %s seconds ---  " % round(time.time() - start, 4))
