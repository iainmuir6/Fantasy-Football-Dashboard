"""
Iain Muir, iam9ez

Fantasy Football Classes

## TODO:
    • PFF Data
    • Lock players after they've played
    • Multi-page dashboard
    • if __name__ == '__main__':
    • constants file

"""

from secrets import SWID, ESPN_S2
import pandas as pd
import requests
import json

# import streamlit as st
# import pickle
# import time
# import sys
# import os


class EspnApi:
    def __init__(self, sport):
        self.swid = SWID
        self.espn_s2 = ESPN_S2
        self.sport = sport
        self.season = 2021

        if sport == 'ffl':
            self.league_id = 1080747
            self.team_id = 4
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
        elif sport == 'fba':
            self.league_id = 1359582180
            self.team_id = 5
            self.slot_codes = {
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
                # reverse
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
            self.default_codes = {
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
                # reverse
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

            PRO_TEAM_MAP = {
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

            STATS_MAP = {
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

            # ACTIVITY_MAP = {
            # }

            ACTIVITY_MAP = {
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

        else:
            print(sport)
            exit(code=0)

        self.week = requests.get(url='https://fantasy.espn.com/apis/v3/games/' + sport + '/seasons/' +
                                     str(self.season) + '/segments/0/leagues/' + str(self.league_id) +
                                     '?view=mSettings',
                                 cookies={
                                     "SWID": self.swid,
                                     "espn_s2": self.espn_s2
                                 }).json()['scoringPeriodId']

    def league_history(self):
        """
        :param self – NONE

        :return list of league_info dictionaries for each year active
        """
        history = requests.get(url="https://fantasy.espn.com/apis/v3/games/" + self.sport + "/leagueHistory/" +
                                   str(self.league_id),
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
        info = requests.get(url="https://fantasy.espn.com/apis/v3/games/" + self.sport + "/seasons/" +
                                str(self.season) + "/segments/0/leagues/" + str(self.league_id),
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
        settings = requests.get(url='https://fantasy.espn.com/apis/v3/games/' + self.sport + '/seasons/' +
                                    str(self.season) + '/segments/0/leagues/' + str(self.league_id) +
                                    '?view=mSettings',
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
        team = requests.get(url='https://fantasy.espn.com/apis/v3/games/' + self.
                            sport + '/seasons/' + str(self.season) + '/segments/0/leagues/' + str(self.league_id) +
                                '?view=mRoster',
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
                 if stat['scoringPeriodId'] == self.week and stat['statSourceId'] == 1],
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
        free_agents = requests.get(url='https://fantasy.espn.com/apis/v3/games/' + self.sport + '/seasons/' +
                                       str(self.season) + '/segments/0/leagues/' + str(self.league_id) +
                                       '?view=kona_player_info',
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


class LeagueMember:
    def __init__(self, name, team, swid, co):
        self.name = name
        self.team = team
        self.swid = swid
        self.co_coach = co


class Player:
    def __init__(self):
        pass


if __name__ == '__main__':
    client = EspnApi('ffl')
