"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/espnFantasyFootball/fantasy_app.py
"""

import streamlit as st

try:
    from espnFantasyFootball import fantasy_home, fba_app, ffl_app
except ModuleNotFoundError:
    import fba_app
    import ffl_app
    import fantasy_home


def launch():
    pages = {
        "Home": fantasy_home,
        "Football": fba_app,
        "Basketball": ffl_app
    }

    st.sidebar.title("Fantasy Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
