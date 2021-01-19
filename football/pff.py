# Iain Muir
# iam9ez

import pandas as pd

week = 16
file = '/Users/iainmuir/Desktop/week-rankings-export.csv'
pff = pd.read_csv(file)
if pff.columns[13] != 'w' + str(week):
    print("WRONG PFF FILE")
    exit(0)

positions = ['WR', 'DST']

for pos in positions:
    options = pff.query('Position == "' + pos + '"')
    options = options[['Name', 'Position', 'Proj Pts', 'expertConsensus', 'Opponent']]
    print(options[:25])
