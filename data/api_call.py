##############################################################
##                                                          ##
##  Various functions for getting API data                  ##
##                                                          ##
##############################################################

 # Libraries
import requests
import datetime
import time 
import pandas as pd
import os
from io import StringIO


# Functions
def make_api_call(date, max_tries=2, backoff_factor=1):
    """
    Calls the Club ELO API and returns the data. It checks if the provided date
    is valid and re-attmepts the API 2 more times, if there was an 
    exception. 

    Parameters
    ----------
    date : str
        A representing the date to use for the API call 

    max_tries : int
        Maximum number of tries to call the API

    timeout : int
        A representing the date to use for the API call 
        
    Returns
    -------
    elo_data : Dataframe
        The output from the API call in a Dataframe
    """

    elo_url = "http://api.clubelo.com/"

    try:
        datetime.date.fromisoformat(date)
        print("Date in correct format")
    except ValueError as e:
        raise ValueError(f"{date} is in incorrect date format, should be YYYY-MM-DD.")

    elo_url = elo_url + date

    attempt = 0
    while attempt <max_tries:
        try:
            output = requests.get(str(elo_url), timeout=30)
            output.raise_for_status()
            elo_data = output.text
            
            if not isinstance(elo_data, str):
                raise ValueError("Malformed API response: expected str")
            
            elo_data = StringIO(elo_data)           
            elo_df = pd.read_csv(elo_data, sep=",") 

            return elo_df
        except requests.exceptions.HTTPError as error_http:
            print("HTTP Error")
            print(error_http.args[0])
        except requests.exceptions.ReadTimeout as error_time:
            print("Time out error")
        except requests.exceptions.ConnectionError as error_conn:
            print("Connection error")
        except requests.exceptions.RequestException as error_ex:
            print("Exception request")

            wait = backoff_factor * (2 ** attempt)
            print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)
            attempt += 1

    raise RuntimeError(f"Failed to fetch data after {max_tries} attempts.")


def get_local_data():
    """
    Gets the local copy of the ELO API data and returns it as a dataframe.

    Parameters
    ----------
    
        
    Returns
    -------
    elo_data : Dataframe
        The output from the API call in a Dataframe
    """
    
    cwd = os.getcwd()
    path = os.path.join(cwd, 'data', 'fallback_elo_data.csv')

    elo_df = pd.read_csv(path, sep=",")

    return elo_df