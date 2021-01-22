"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/espnFantasyFootball/fantasy_app.py
"""

import streamlit as st

try:
    import fba_app
    import ffl_app
except ModuleNotFoundError:
    from espnFantasyFootball import fba_app, ffl_app

import home


def launch():
    pages = {
        "Home": home,
        "Football": fba_app,
        "Basketball": ffl_app
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
