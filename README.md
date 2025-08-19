# Football End of Season Points calculator

Calculates the end of season points (EOSP) 

## Setup & Running the Football ELO API Code

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)

## Getting the Code

You can get the code in two ways:

### 1. Clone from Git

If you have Git installed, open a terminal and run:

```sh
git clone vishalj7/football_eosp
cd Football-ELO
```

### 2. Download as ZIP

If you don’t have Git, you can download the project as a ZIP file:

- Click the green "Code" button at the top of the repository page.
- Select "Download ZIP".
- Extract the ZIP file to your desired location.
- Using 

### Install Dependencies

Open a terminal or powershell in the project root and run:

```sh
pip install -r requirements.txt
```

### Running the API Call

To code in powershell or bash run the following command, make sure you're in the FOOTBALL ELO folder if not already:

```sh
python main.py --date <YYYY-MM-DD > --country 'ENG' --level 1 
```
This will create a fixture list and expected points for the English Premier League.

For a custom league or European Super League `;)` , please run the following:
```sh
python main.py --date <YYYY-MM-DD > --custom True --custom_team Arsenal Chelsea Liverpool "Man City" "Man United" Tottenham
```



### High-Level Architectural Choices

There are two ways and it depends on how much can be expanded/added and what would require access? Would it be the code or just the results.

#### Option 1 - Rather than creating a single script that does everything, I have used a more pragmatic approach and one that is often used to ensure a robust code base that is realiable and can easily be expanded on. 

The way I've designed it is to keep components modular so data scripts are kept in a single folder (ingestion), functions for calcaulting and modifying data in another folder (transformations). If down the line, a new calculation is required, these functions can be added to the folder which can be then used in main script. 

This also allows reusability and tests can easliy be written as they are stateless. 

#### Option 2 - Cloud to be used if its just the results. It might be overkill if this data is only really required to calculate the end of season points.

I would move this to the cloud and use something like Azure Logic Apps that can make API calls automatically on a schedule and then drop the outputs into a storage container. 

This would be kept as raw data, a copy can be sent to a SQL database, then using something like Azure Function Apps to run the code that calculates the expected points after the API file has been dropped. A blog trigger can be used to detect when a file or a specific file name and type comes into the storage container, triggering the Function Apps code to run automatically and then sending the results to a SQL database where users can have access to the expected points as well as the raw data if validation is required. The SQL can be setup to be 3 layers, bronze where raw data is kept, silver where any transformation happen and finally the gold layer where the calculations, new attributes are added and end-users such as Data Scientists can access this data.


### Unit Tests

I didn't get time to implement the unit test but I would create a test plan where I would state the test, what I'm expecting the outcome to be of a test and the actual results. Prior to running the tests, I would create dummy data for the test cases.

Below is a high-level style of some tests:

1. test_date_format
data - 2025-01-01
expected outcome API call successful
actual outcome - tbc

data - 2035-01-01
Ideally, I would add logic to ensure future dates arent accepted
expected outcome API call unsuccessful
actual outcome - tbc

2. test_expected_points
data - 4 teams and has an ELO of team a 1000, team b 750, team c 500 and team d 250
expected outcome team a with the most points and team d with the least. I would acutally calculate the points using these ELOs and then use that as the expected outcome
actual outcome - tbc

Note - there are many more tests to add such as the custom league, checking the fixtures


### Key Assumptions

- The API has a fixed schema and always returns a ELO for each team
- Format of the date (YYYY-MM-DD) accepted by the API does not change
- Local ELO data file does not move from `data/fallback_elo_data.csv`
- Teams are unqiue and all have a `Country` and `Level`
- Teams for custom league are present within the ELO dataset and the name passed into the call is spelt the same as in the ELO data i.e Manchester United is passed as Man United
- There is no missing data in the ELO
- There is no calculation for a draw so teams only have a win probability
- Timeout is fixed to 30 seconds