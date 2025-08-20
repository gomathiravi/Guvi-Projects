import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# import plotly.express as px

# -------------------------
# 2. Load DataFrames from mysql database
# -------------------------
# import mysql.connector as sql
# import pandas as pd

# conn_mydb = sql.connect(
#     host = 'localhost',
#     user = 'root',
#     passwd = 'testsql2025'
# )
# cursor = conn_mydb.cursor()
# cursor.execute("CREATE DATABASE IF NOT EXISTS cricket_db;")
# print ("My SQL Connection established")
# cursor.execute("USE cricket_db;")
# matches = pd.read_sql_query("SELECT * FROM Matches;", conn_mydb)
# print (f"{matches.head(10)}")

# players = pd.read_sql_query("SELECT * FROM Players", conn_mydb)
# innings = pd.read_sql_query("SELECT * FROM Innings", conn_mydb)
# deliveries = pd.read_sql_query("SELECT * FROM Deliveries", conn_mydb)

def plot_matches(matches_df):
    # Matches per season

    plt.figure(figsize=(10,8))
    sns.countplot(data=matches_df, x="season", order=matches_df["season"].value_counts().index)
    plt.title("Number of Matches per Season")
    plt.xticks(rotation=85)
    plt.show()

def load_insights():

    # -------------------------
    # 1. Load the csv files
    # -------------------------
    matches_df = pd.read_csv('cric_data/matches.csv')
    deliveries_df = pd.read_csv('cric_data/deliveries.csv')
    innings_df = pd.read_csv('cric_data/innings.csv')
    players_df = pd.read_csv('cric_data/players.csv')

    print (f"{matches_df.head(10)}")
    print (f"{matches_df.value_counts("season")}")
    print (f"{matches_df.shape}")

    #1. Matches per season
    plot_matches(matches_df)

    print (f"{matches_df.shape}")

    # extract highest match of the matches
    count_player_of_match = matches_df["player_of_match"].value_counts()
    print (f"{count_player_of_match}")

    #extract 10 Player of the matches
    count_top_ten_player_of_match = matches_df["player_of_match"].value_counts()[0:10]
    print (f"{count_top_ten_player_of_match}")

    #extract list of top 10 Player of the matches Names Only
    name_top_ten_player_of_match = list(matches_df["player_of_match"].value_counts()[0:10].keys())
    print (f"{name_top_ten_player_of_match}")

    #2. creating a bar graph to visualize the data set
    plt.figure(figsize=(15,4))
    plt.bar(list(matches_df["player_of_match"].value_counts()[0:10].keys()), matches_df["player_of_match"].value_counts()[0:10], color="blue" )
    plt.title("Top 10 Player of Match")
    plt.xlabel("Players")
    plt.ylabel("Awards")
    plt.show()

    #calculate the hightest toss winners
    highest_toss_winners = matches_df["toss_winner"].value_counts()
    print (f"{highest_toss_winners}")

    #analyse the matches won by batting first
    batting_first = matches_df[matches_df["win_by_runs"] >0] ["win_by_runs"]
    batting_first.head(10)
    print (f"{batting_first.head(10)}")

    #3. creating a bar graph to view the winning by runs
    plt.figure(figsize=(5,6))
    plt.hist(batting_first)
    plt.title("Winning by Margins Graphs")
    plt.xlabel("Margin of runs")
    plt.ylabel("No. of Matches")
    plt.show()

    #get the count of winning matches and the names of the teams only
    winners_df = matches_df[matches_df["win_by_runs"] >0]
    winners = winners_df["winner"].value_counts()
    print (f"{winners}")

    #get the top 5 of winning matches and the names of the teams only
    winner_names = winners_df["winner"].value_counts()[0:5].keys()
    print (f"{winner_names}")

    #4. creating a graph for it.
    plt.figure(figsize=(14,6))
    plt.bar(winners_df["winner"].value_counts()[0:5].keys(), winners_df["winner"].value_counts()[0:5], color=["blue", "yellow", "red", "green", "orange"])
    plt.title("Highest no. of wins Graph")
    plt.xlabel("Teams")
    plt.ylabel("No. of Matches won")
    # plt.grid()
    plt.show()

    # analyze the teams who won while batting second
    batting_second = matches_df[matches_df["win_by_wickets"] >0]
    print (f"{batting_second.head(10)}")

    #5. creating a histogram for better analysis
    plt.figure(figsize=(4,4))
    plt.hist(batting_second["win_by_wickets"], bins=30)
    plt.title("winning by Margins Graph")
    plt.xlabel("Margin of wickets")
    plt.ylabel("No. of Matches")
    plt.show()

    # the top 5 teams who won the most matches while batting second
    count_top_five_teams = batting_second["win_by_wickets"].value_counts()[0:5]
    print (f"{count_top_five_teams}")

    #6. creating a Bar graph for who won the matches while batting second
    plt.figure(figsize=(12,7))
    plt.bar(list(batting_second["win_by_wickets"].value_counts()[0:5].keys()), list(batting_second["win_by_wickets"].value_counts()[0:5]), color=["blue", "yellow", "red", "green", "orange"])
    plt.title("won while batting second")
    plt.xlabel("Margin of Wickets")
    plt.ylabel("No. of Matches")
    plt.show()

    # toss decision percentage
    temp_series = matches_df["toss_decision"].value_counts()
    labels = (np.array(temp_series.index))
    sizes = (np.array((temp_series / temp_series.sum())*100))
    colors = ['gold', 'lightskyblue']
    #7. creating a pie chart on toss decision percentage
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Toss decision percentage")
    plt.show()

    #8. how this decision varied over time.
    plt.figure(figsize=(12,6))
    sns.countplot(x='season', hue='toss_decision', data=matches_df)
    plt.xticks(rotation='vertical')
    plt.show()

    #9. Top 10 match venues.
    venue_counts = matches_df['venue'].value_counts().head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=venue_counts.values, y=venue_counts.index, hue=venue_counts.index, palette="coolwarm", dodge=False, legend=False)
    plt.title("Top 10 Match Venues")
    plt.xlabel("Matches")
    plt.ylabel("Venue")
    plt.tight_layout()
    plt.show()

    #10. Top Run Scorers (Batsmen) Across Matches

    # Merge Deliveries with Players to ensure batter belongs to a team/match
    batting_df = deliveries_df.merge(players_df, left_on=["match_id", "batter"], right_on=["match_id", "player"], how="left")

    # Convert runs_batter to int (since schema had VARCHAR)
    batting_df["runs_batter"] = batting_df["runs_batter"].astype(int)

    # Aggregate runs per batter
    top_batters = batting_df.groupby("batter")["runs_batter"].sum().sort_values(ascending=False).head(10)

    # Plot
    plt.figure(figsize=(10,5))
    sns.barplot(x=top_batters.values, y=top_batters.index)
    plt.title("Top 10 Run Scorers (Across All Matches)")
    plt.xlabel("Runs Scored")
    plt.show()

    #11. Bowler with Most Wickets

    # Consider valid dismissals
    valid_wickets = deliveries_df[deliveries_df["wicket_kind"].notnull() & (deliveries_df["wicket_kind"] != "run out")]

    # Count wickets per bowler
    top_bowlers = valid_wickets.groupby("bowler")["wicket_kind"].count().sort_values(ascending=False).head(10)

    # Plot
    plt.figure(figsize=(10,5))
    sns.barplot(x=top_bowlers.values, y=top_bowlers.index)
    plt.title("Top 10 Bowlers by Wickets Taken")
    plt.xlabel("Wickets")
    plt.show()