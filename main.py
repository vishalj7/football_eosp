##############################################################
##                                                          ##
##  main.py                                                 ##
##                                                          ##
##############################################################

 # Libraries
import argparse
from data import api_call
from func import eosp_functions

def main():

    parser = argparse.ArgumentParser(description="Football End of Season Points Calculator")
    parser.add_argument('--date', type=str, default="2025-01-01", help="Date for ELO API call (YYYY-MM-DD)")
    parser.add_argument('--country', type=str, default=None, help="Country code for league (e.g., ENG)")
    parser.add_argument('--level', type=int, default=None, help="League level (e.g., 1 for Preimer League)")
    parser.add_argument('--custom', type=bool, default=False, help="True for custom league")
    parser.add_argument('--custom_team', nargs='+', type=str, default=None, help="List of custom teams as strings")
    args = parser.parse_args()
    args = parser.parse_args()

    # Attempt to get data from API, if unsuccessful, get local data file
    try:
        elo_df = api_call.make_api_call("2025-01-01")
        print("Successful API call")
    except:
        print("Unsuccessful API call. Getting data locally.")
        elo_df = api_call.get_local_data()

    # Returns a fixture list for the Premier League
    fixture = eosp_functions.get_fixture_list(elo_df, country=args.country, level=args.level, custom=args.custom, custom_teams=args.custom_team)

    # Calculates the expected points for each team in the league and saves the results to a CSV file
    agg_team_points, fixtures_points = eosp_functions.expected_points(elo_df, fixture)
    agg_team_points.to_csv("Expected_Points.csv", sep=",", header=True, index=False)

if __name__ == "__main__":
    main()