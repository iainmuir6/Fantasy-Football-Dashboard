"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/espnFantasyFootball/fantasy_app.py
"""

import streamlit as st

try:
    import fba_app
    import ffl_app
    import home
except ModuleNotFoundError:
    from espnFantasyFootball import fba_app, ffl_app, home


def launch():
    pages = {
        "Home": home,
        "Football": fba_app,
        "Basketball": ffl_app
    }

    st.sidebar.title("Fantasy Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
