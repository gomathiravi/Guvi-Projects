# Guvi-Projects
Projects at GUVI

*** Cricket Match Data Analysis
This project was built as part of training at GUVI.
This project is to Analysis Cricket Match Data set. The project is provide various insights about Matches, Players, Match Wons metrics, Deliveries etc.

***** Data Set Management
Each of the classes handle the following:

** Scrape_Data Class:

* scrape for download the data set from the webpage "https://cricsheet.org/"
* Following 4 Match data's in json format are downloaded:
  * "Test matches", "One-day internationals", "T20 internationals", "Indian Premier League"

** DataParser Class:

* Unzip the downloaded files in the directory /downloaded_jsons
* Parse for each of json files within each of the folders unzipped.
* The parsed data are grouped into following:
  * Matches, Players, Innings and Deliveries
* Saved the above grouped data in the folder /cric_data in csv format.

** CricketDatabase class:
* Derived from the BaseDatabase class
* Connects to the MySQL Database and creates cricket_db
* Reads all the data in the cvs files and save them into relevant tables in the cricker_db:
  * Matches.csv -- Matches
  * Players.csv -- Players
  * Innings.csv -- Innings
  * Deliveries.csv -- Deliveries

** cric_data_plot.py
* defines all the functions relating to plot various graphs using the above tables / csv files.

* Cricket Match Data Visualization
    1. Matches per season
    2. Top 10 Player of Match
    3. Winning by Margin of Runs
    4. Highest number of wins by teams
    5. Winning by Margin wickets
    6. Toss Decision Percentage
    7. Top 10 Match Venues
    8. How Toss decision varied over time
    9. Top 10 Runs Scored
    10. Top 10 Bowlers by Wickets Taken

### Project Structure
## File Descriptions

### `main.py`
- Entry point for Running the application
  - **To Scrape and download data**
  - **Unzip and parse the data set**
  - **save the cricket match data in <given filename> with .csv file**
  - **Create tables and store all the Cricket dat in the given table name**
  - **Close the data base connection**
  - **Use the csv file for visualization**

### `base_data_base.py`
- Contains `BaseDatabase` class:
  - Initializes database
  - Creates necessary tables
  - Provides method for executing SQL queries

## Requirements

- Python
- matplotlib.pyplot
- pandas
- mysql
- seaborn
- selenium
- os
- requests

## Usage

Run the app using:

```bash
python3 run main.py
