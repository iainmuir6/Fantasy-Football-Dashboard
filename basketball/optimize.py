# Iain Muir
# iam9ez

from fantasyClass import EspnApi
from bs4 import BeautifulSoup
import pandas as pd
import constants
import requests

client = EspnApi('fba')

week = 5
season = 2021
LEAGUE_ID = client.league_id
TEAM_ID = client.team_id

SWID = "{94FD803F-87FC-4BDC-BD80-3F87FCEBDCFC}"
ESPN_S2 = "AEA%2Fs7CAHybhPWiuG5cTGqmfaH2%2F%2FeUCDP5bTDB4j0hDCLGW58ieoYJCnEB9uxNNPrx1CRjc8cuCinM54m2mUnf" \
          "5PwfVmZ6Xup0Hx1GSpuVoHuTjibfHSbu%2FDM0Zp%2BDhDygZS7zUVRZ1ag7Dm%2F7S2zcys1Ywxf4Fj1mFVKOmnIygFM" \
          "V1a8LlMRy5W4ZpkvCvJzmQJTZcgfBncMmt1wh5IbsVWJwAm8ElISHA%2F9ooLplPppnKwIi1jbzeJv1UHIuh%2Bio%3D"

url = 'https://www.fantasypros.com/nba/projections/weekly-overall.php'
page = requests.get(url)

if page.status_code != 200:
    print(page.status_code)
    exit(code=0)

soup = BeautifulSoup(page.content, 'html.parser')
t = soup.find('table')

title = soup.find('div', class_='primary-heading-subheading pull-left').text.strip().split('\n')[0]
if str(week) not in title:
    print(title)
    exit(code=0)

t = t.tbody
data = [
    [stat.text if "(" not in stat.text else stat.text[:stat.text.find('(') - 1] for stat in player.find_all('td')] +
    [player['class'][0][-4:]]
    for player in t.find_all('tr')
]

df = pd.DataFrame(data, columns=['name', 'PTS', 'REB', 'AST', 'BLK', 'STL', 'FG&', 'FT%',
                                 '3PTM', 'GP', 'MIN', 'TO', 'playerID'])


roster = client.get_roster(TEAM_ID)
roster = df[df['name'].isin(roster['Name'])]

settings = client.league_settings()
scoring = {constants.FBA_STATS_MAP[str(item['statId'])]: float(item['points'])
           for item in settings['settings']['scoringSettings']['scoringItems']}

points = {'name': list(roster['name']),
          'games': list(roster['GP'])}

for k in scoring.keys():
    if k in ['FGA', 'FGM', 'FTA', 'FTM']:
        continue
    else:
        points[k] = list(roster[k].map(lambda x: float(x) * scoring[k]))

points = pd.DataFrame(data=points)
points['total'] = points.sum(axis=1)
points = points.sort_values(by='total')
print(points)
