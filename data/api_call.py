import requests
import datetime
import time 

def make_api_call(date, max_tries=2, timeout=5):
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
    elo_data : str
        The output from the API call in a string format
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
            output = requests.get(str(elo_url))
            output.raise_for_status()
            elo_data = output.text
            return elo_data
        except requests.exceptions.HTTPError as error_http:
            print("HTTP Error")
            print(error_http.args[0])
        except requests.exceptions.ReadTimeout as error_time:
            print("Time out error")
        except requests.exceptions.ConnectionError as error_conn:
            print("Connection error")
        except requests.exceptions.RequestException as error_ex:
            print("Exception request")
            wait = timeout
            time.sleep(wait)
            attempt += 1
    raise RuntimeError(f"Failed to fetch data after {max_tries} attempts.")

