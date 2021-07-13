<img src="https://media.pff.com/2018/06/PFFBall_Black-e1530132578167.png" width="100"><img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width="200"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/ESPN_wordmark.svg" width="250">

# ESPN Fantasy Football

## Description
Aims to combine the ESPN API, Pro Football Focus Data, and the Streamlit dashboard library to create an interactive 
platform that optimizes your roster and analyzes your fantasy league. This project may be expanded to look into
the fantasy basketball portion of the API.

###### Pro Football Focus
[Pro Football Focus](https://www.pff.com/) is a website that focuses on thorough analysis of the National Football League and NCAA Division-I football in the United States.

###### Streamlit
Powered by [Streamlit](https://docs.streamlit.io/en/stable/index.html). See the 
[documentation](https://docs.streamlit.io/en/stable/api.html) for more details on its application. Installation:

```
$ pip install streamlit
>>> import streamlit as st
```

###### ESPN API
Hidden API to [ESPN.com](http://espn.go.com/) with a variety of undocumented endpoints

Endpoint Examples:
```
url = https://fantasy.espn.com/apis/v3/games/ffl/seasons/<SEASON>/segments/0/leagues/<LEAGUE_ID>
response = requests.get(
    url,
    params={
        view: mSettings, mMatchup, mMatchupScore
        scoringPeriodId: week
    },
    cookies={
        SWID: {<ESPN ID>}
        espn_s2: '<cookie string>'
    }
)                            
```
