from data import api_call
from func import eosp_functions

try:
    elo_df = api_call.make_api_call("2025-01-01")
    print("Successful API call")
except:
    print("Unsuccessful API call. Getting data locally.")
    elo_df = api_call.get_local_data()

fixture = eosp_functions.get_fixture_list(elo_df, country='ENG', level=1)

# Custom League or European Super League ;)
# teams = ["Arsenal","Chelsea","Liverpool","Man City","Man United","Tottenham"]
# fixture = eosp_functions.get_fixture_list(elo_df, custom=True, custom_teams=teams)

agg_team_points, fixtures_points = eosp_functions.expected_points(elo_df, fixture)
agg_team_points.to_csv("Expected_Points.csv", sep=",", header=True, index=False)