# Iain Muir
# iam9ez

from fantasyClass import EspnApi, FantasyLeague
import streamlit as st
import pandas as pd
import pickle
import time
import sys
import os


def read_ppf_data(data, player_options):
    df = pd.read_csv(data)
    projected = []
    for name in player_options['Name']:
        try:
            projected.append(df.query('Name == "' + name.replace("/", "") + '"').values[0][5])
        except IndexError:
            projected.append(None)
    return projected


def dashboard(self):
    st.markdown(
        "<center> <img src='https://espnpressroom.com/us/files/2016/08/Fantasy-Football-App-LOGO-500x405.png' "
        "height='200' /> </center>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center';> Fantasy Lineup Optimization </h1>", unsafe_allow_html=True)
    old, new = st.beta_columns(2)
    old.markdown("<h3 style='text-align:center';> Current Lineup </h1>", unsafe_allow_html=True)
    new.markdown("<h3 style='text-align:center';> Optimized Lineup </h1>", unsafe_allow_html=True)

    roster_settings = {client.slot_codes[int(c)]: q for c, q in
                       client.league_settings()['settings']['rosterSettings']['lineupSlotCounts'].items() if q != 0}
    starters = self.roster.query('currentPosition != "BE"')
    roster = starters.drop(axis=1, labels=['currentPosition', 'actual'])
    free_agents = client.get_free_agents()
    fa_names = list(free_agents['Name'])
    options = roster.append(free_agents)

    if pff:
        pff_projections = read_ppf_data(sys.argv[1], options)
        options = options.join(pd.DataFrame({'pffProjections': pff_projections}))

    total = 0.0

    for position in ['QB', 'RB', 'WR', 'TE', 'RB/WR/TE', 'D/ST', 'K']:
        number = roster_settings[position]
        starters_pos = starters.query('currentPosition == "' + position + '"')
        condition = "defaultPosition == 'RB' | defaultPosition == 'WR' | defaultPosition == 'TE'" \
            if position == 'RB/WR/TE' \
            else "defaultPosition == '" + position + "'"

        best = options.query("defaultPosition == " + condition).sort_values(by='projected',
                                                                            ascending=False)[:number]
        total += best['projected'].sum()
        options = options.drop(labels=list(best.index), axis=0)

        for starter, optimized in zip(starters_pos.values, best.values):
            color1 = 'lightcoral' if starter[0] not in list(best['Name']) \
                else 'white'
            color2 = 'moccasin' if optimized[0] in fa_names \
                else 'lightgreen' if optimized[0] not in list(starters_pos['Name']) \
                else 'white'

            if position == 'D/ST':
                src1 = "https://a.espncdn.com/i/teamlogos/nfl/500/" + client.team_ids[starter[1]] + ".png"
                src2 = "https://a.espncdn.com/i/teamlogos/nfl/500/" + client.team_ids[optimized[1]] + ".png"
                height = '50'
            else:
                src1 = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/" + str(
                    starter[1]) + ".png&w=350&h=254"
                src2 = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/" + str(
                    optimized[1]) + ".png&w=350&h=254"
                height = '40'

            old.markdown(
                "<p style='text-align:left;background-color:" + color1 + ";'> <img src='" + src1 + "' height='" +
                height + "'/>  (" + starter[2] + ") <b>" + starter[0] + "</b>  <span style='float:right'> " +
                str(round(float(starter[-2]), 2)) + " </span></p>", unsafe_allow_html=True)
            new.markdown(
                "<p style='text-align:left;background-color:" + color2 + ";'> <img src='" + src2 + "' height='" +
                height + "'/>  (" + optimized[2] + ") <b>" + optimized[0] + "</b>  <span style='float:right'> " +
                str(round(float(optimized[-1]), 2)) + " </span></p>", unsafe_allow_html=True)

    old.markdown(
        "<p style='text-align:center;font-size:20px;'> <b> Total: " + str(round(starters['projected'].sum(), 2)) +
        "</b> </p>", unsafe_allow_html=True)
    new.markdown(
        "<p style='text-align:center;font-size:20px;'> <b> Total: " + str(round(total, 2)) +
        "</b> </p>", unsafe_allow_html=True)


if __name__ == '__main__':
    start = time.time()
    client = EspnApi()

    pff = False
    if len(sys.argv) > 1:
        pff = True

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
