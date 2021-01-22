"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/espnFantasyFootball/app.py
"""

import streamlit as st

import basketball
import football
import home


def launch():
    pages = {
        "Home": home,
        "Football": football,
        "Basketball": basketball
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
