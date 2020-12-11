"""
Iain Muir, iam9ez

Fantasy Football Classes
"""

from datetime import datetime
import requests


class EspnApi:
    def __init__(self):
        self.swid = "{94FD803F-87FC-4BDC-BD80-3F87FCEBDCFC}"
        self.espn_s2 = "AEA%2Fs7CAHybhPWiuG5cTGqmfaH2%2F%2FeUCDP5bTDB4j0hDCLGW58ieoYJCnEB9uxNNPrx1CRjc8cuCinM54m2mUnf" \
                       "5PwfVmZ6Xup0Hx1GSpuVoHuTjibfHSbu%2FDM0Zp%2BDhDygZS7zUVRZ1ag7Dm%2F7S2zcys1Ywxf4Fj1mFVKOmnIygFM" \
                       "V1a8LlMRy5W4ZpkvCvJzmQJTZcgfBncMmt1wh5IbsVWJwAm8ElISHA%2F9ooLplPppnKwIi1jbzeJv1UHIuh%2Bio%3D"
        self.league_id = 1080747
        self.season = 2020
        self.slot_codes = {
            0: 'QB', 1: 'TQB', 2: 'RB', 3: 'RB/WR', 4: 'WR', 5: 'WR/TE',
            6: 'TE', 7: 'OP',  8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',
            12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST', 17: 'K',
            18: 'P', 19: 'HC', 20: 'BE', 21: 'IR', 22: '', 23: 'RB/WR/TE'
        }
        self.default_codes = {
            1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
        }
        self.team_ids = {
            -16018: "no"
        }

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
                                "espn_s2": self.espn_s2}
                            ).json()
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


class FantasyLeague:
    def __init__(self):
        self.name = client.league_info()['settings']['name']
        self.members = {member['id']: member['displayName'] for member in client.league_info()['members']}
        self.teams = {team['id']: {'name1': self.members[team['owners'][0]],
                                   'name2': self.members[team['owners'][1]] if len(team['owners']) == 2 else "n/a",
                                   'teamName': team['location'] + " " + team['nickname'],
                                   'abbreviation': team['abbrev'],
                                   'ownerIDs': team['owners']} for team in client.league_info()['teams']}


class FantasyTeam:
    def __init__(self):
        self.name = ''
        self.owner = ''
        self.roster = ''


class LeagueMember:
    def __init__(self):
        self.name = ''
        self.team = ''
        self.swid = ''


client = EspnApi()
