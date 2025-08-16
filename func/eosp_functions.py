##############################################################
##                                                          ##
##  Various functions for calcualtion End of Season Points  ##
##                                                          ##
##############################################################

 # Libraries

import pandas as pd

# Functions
def get_fixture_list(data, country=None, level=None, custom=False, custom_teams=None):
    """
    Calls the Club ELO API and returns the data. It checks if the provided date
    is valid and re-attmepts the API 2 more times, if there was an 
    exception. 

    Parameters
    ----------
    date : str
        A representing the date to use for the API call 

    country : str
        Maximum number of tries to call the API

    level : int
        Level to indicate the tier of football league 

    custom : boolean
        Set to True if you want a custom league

    custom_teams : list
        A list of teams to form a custom league 
        
    Returns
    -------
    elo_data : str
        The output from the API call in a string format
    """

    if custom==True:
        try:
            if custom_teams and isinstance(custom_teams, list):
                team_fixtures = create_fixture_list(set(custom_teams))
        except:
            raise TypeError("Please provide a valid list of teams.")
    else:
        league_df = data[(data['Country'] == country) & (data['Level'] == level)]
        teams = list(league_df['Club'])
        team_fixtures = create_fixture_list(set(teams))

    return team_fixtures
    
    

def create_fixture_list(list_of_teams):
    """
    Creates a round robin home and away for each team 

    Parameters
    ----------
    list_of_teams : list
        A list of teams to create the fixtures for
        
    Returns
    -------
    fixtures : list
        A list of fixtures of all the teams passed in. Each have a round robin
    """

    fixtures = []
    for home in list_of_teams:
        for away in list_of_teams:
            if home == away:
                continue
            fixtures.append((home, away))

    return fixtures


def expected_points(data, fixtures):

    fixtures_points = []

    for home_club, away_club in fixtures:
        home_elo = float(data[data['Club'] == home_club]['Elo'].iloc[0])
        away_elo = float(data[data['Club'] == away_club]['Elo'].iloc[0])
        
        home_elo += 100

        dr = home_elo - away_elo
        home_win = 1 / (1 + 10 ** (-dr / 400))
        away_win = 1 - home_win

        home_points = round((home_win * 3), 2)
        away_points = round((away_win * 3), 2)

        fixture_points_home = ["H", home_club, home_points]
        fixture_points_away = ["A", away_club, away_points]

        fixtures_points.append(fixture_points_home)
        fixtures_points.append(fixture_points_away)

    agg_fixtures_points = pd.DataFrame(fixtures_points, columns=["Home/Away", "Club", "Expected Points"])
    agg_team_points = agg_fixtures_points.groupby('Club')['Expected Points'].sum().reset_index()

    agg_team_points = agg_team_points.sort_values(by='Expected Points', ascending=False).reset_index(drop=True)

    return agg_team_points, fixtures_points