import os
import json
import zipfile
import pandas as pd
from pathlib import Path
# from base_data_base import BaseDatabase
from cric_data_base import CricketDatabase

MATCH_DATA = ["tests_json", "odis_json", "t20s_json", "ipl_json"]

# -- Matches Table
matches_table = (
    "CREATE TABLE IF NOT EXISTS Matches ("
        "match_id INT PRIMARY KEY," # -- unique numeric ID
        "season VARCHAR(10),"
        "match_date DATE,"
        "team_type VARCHAR(15),"
        "city VARCHAR(50),"
        "venue VARCHAR(100),"
        "match_type VARCHAR(20),"
        "winner VARCHAR(50),"
        "win_by_runs INT,"
        "win_by_wickets INT,"
        "player_of_match VARCHAR(50),"
        "toss_winner VARCHAR(50),"
        "toss_decision VARCHAR(5),"
        "team1 VARCHAR(50),"
        "team2 VARCHAR(50)"
    ");"
)

# -- Players Table
players_table = (
    "CREATE TABLE Players ("
    "player_id VARCHAR(8),"
    "match_id INT,"
    "team VARCHAR(50),"
    "player VARCHAR(50),"
    "FOREIGN KEY (match_id) REFERENCES Matches(match_id)"
    ");"
)

# -- Innings Table
innings_table = (
    "CREATE TABLE IF NOT EXISTS Innings ("
        "inning_no INT,"
        "match_id INT,"
        "batting_team VARCHAR(50),"
        "PRIMARY KEY (match_id, inning_no),"
        "FOREIGN KEY (match_id) REFERENCES Matches(match_id)"
        ");"
)

# -- Deliveries Table
deliveries_table = (
    "CREATE TABLE Deliveries ("
    "delivery_id VARCHAR(5) PRIMARY KEY,"
    "match_id INT,"
    "inning_no INT,"
    "over_no VARCHAR(2),"
    "ball VARCHAR(2),"
    "batter VARCHAR(50),"
    "bowler VARCHAR(50),"
    "non_striker VARCHAR(50),"
    "runs_batter VARCHAR(3),"
    "runs_extras VARCHAR(3),"
    "runs_total VARCHAR(3),"
    "wicket_kind VARCHAR(20),"
    "player_out VARCHAR(50),"
    "fielder VARCHAR(50),"
    "FOREIGN KEY (match_id, inning_no) REFERENCES Innings(match_id, inning_no)"
    ");"
)

class DataParser:
    def __init__(self, directory):
        self.directory = directory
        self.matches_list = []
        self.teams_list = []
        self.players_list = []
        self.innings_list = []
        self.deliveries_list = []

    def parse_directory(self):
        with os.scandir(self.directory) as entries:
            for entry in entries:
                if entry.is_dir():
                    is_dir_parsed = False
                    for folder_name in MATCH_DATA:
                        if entry.name == folder_name:
                            # print(f"Parsing directory: {entry.path}")
                            self.parse_files(entry.path)
                            is_dir_parsed = True
                            break

                    if not is_dir_parsed:
                        print(f"Skipping non-directory: {entry.path}")

    def unzip_files(self):
        with os.scandir(self.directory) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.zip'):
                    unzipped_file = False
                    print(f"Found zip file: {entry.name} and path: {entry.path}")
                    # Check if the zip file matches any of the match data folders
                    extract_to_file_name = os.path.splitext(entry.name)[0]
                    for folder in MATCH_DATA:
                        if extract_to_file_name == folder:
                            extract_to_file_name = os.path.join(self.directory, folder)
                            print(f"Extracting to: {extract_to_file_name}")
                            # Extract the folder name from the zip file name
                            print(f"Unzipping file: {entry.name}")
                            # unzip the file
                            with zipfile.ZipFile(entry.path, 'r') as zipObject:
                                zipObject.extractall(extract_to_file_name)
                                print(f"Extracted to: {extract_to_file_name}")
                            unzipped_file = True
                            break

                    if not unzipped_file:
                        print(f"Skipping file: {entry.name} as it does not match any folder names.")
                else:
                    print(f"Skipping non-zip file: {entry.name}")

    def parse_files(self, directory):
        if not os.path.isdir(directory):
            raise ValueError("Provided path is not a directory.")

        with os.scandir(directory) as entries:
            for entry in entries:
                # print(f"Processing entry: {entry.name} at {entry.path}")
                if entry.is_file():
                    # print(entry.name)
                    if entry.name.endswith('.json'):
                        # parsed_data = self.parse_json_normalize(entry.path)
                        parsed_data = self.parse_json(entry.path)
                        self.matches_list.append(parsed_data["match"])
                        # self.teams_list.append(parsed_data["teams"])
                        self.players_list.append(parsed_data["players"])
                        self.innings_list.append(parsed_data["innings"])
                        self.deliveries_list.append(parsed_data["deliveries"])
                    else:
                        print(f"Skipping non-JSON file: {entry.name}")

    def parse_json(self, filePath):
        # if not os.path.exists(filePath):
        #     raise FileNotFoundError(f"The file {filePath} does not exist.")

        with open(filePath, 'r') as file:
            # data = file.read()
            json_data = json.load(file)

            # Extract match info
            info = json_data["info"]
            match_id = Path(filePath).stem

            # return match_id
            match_df = pd.DataFrame([{
                "match_id": match_id,
                "season": info.get("season", "unknown"),
                "match_date": pd.to_datetime(info["dates"][0]).date(),
                "city": info.get("city", "unknown"),
                "venue": info.get("venue", "unknown"),
                "match_type": info.get("match_type", "unknown"),
                "winner": info.get("outcome", {}).get("winner", "unknown"),
                "toss_winner": info.get("toss", {}).get("winner", "unknown"),
                "toss_decision": info.get("toss", {}).get("decision", "unknown"),
                "win_by_runs": info["outcome"]["by"].get("runs", 0) if "by" in info["outcome"] else 0,
                "win_by_wickets": info["outcome"]["by"].get("wickets", 0) if "by" in info["outcome"] else 0,
                "player_of_match": info["player_of_match"][0] if info.get("player_of_match") else "NA",
                "team1": info["teams"][0],
                "team2": info["teams"][1],
                "team_type": info.get("team_type", "unknown")
            }])
            # Extract players, innings, and deliveries

            # Players
            player_idx = -1
            if 'registry' in info:
                registry = info.get("registry")
                if 'people' in registry:
                    people = registry.get("people")
            else:
                player_idx = 1

            players_data = []
            for team, players in info["players"].items():
                for p in players:
                    players_data.append({
                        "player_id": str(player_idx) if player_idx != -1 else people.get(p, ""),
                        "match_id": match_id,
                        "team": team,
                        "player": p
                    })
                    players_df = pd.DataFrame(players_data)

            # Innings + Deliveries
            innings_data, deliveries_data = [], []
            for in_idx, inning in enumerate(json_data["innings"], start=1):
                innings_data.append({
                    "match_id": match_id,
                    "inning_no": in_idx,
                    "batting_team": inning["team"]
                })

                for over in inning["overs"]:
                    over_num = over["over"]
                    for ball_idx, delivery in enumerate(over["deliveries"], start=1):
                        deliveries_data.append({
                            "delivery_id": str(in_idx) + "_" + str(over_num) + "_" + str(ball_idx),
                            "match_id": match_id,
                            "inning_no": in_idx,
                            "over_no": over_num,
                            "ball": ball_idx,
                            "batter": delivery["batter"],
                            "bowler": delivery["bowler"],
                            "non_striker": delivery["non_striker"],
                            "runs_batter": delivery["runs"]["batter"],
                            "runs_extras": delivery["runs"]["extras"],
                            "runs_total": delivery["runs"]["total"],
                            "wicket_kind": delivery.get("wickets", [{}])[0].get("kind") if "wickets" in delivery else "NA",
                            "player_out": delivery.get("wickets", [{}])[0].get("player_out") if "wickets" in delivery else "NA",
                            "fielder": delivery.get("wickets", [{}])[0].get("fielders", [{}])[0].get("name") if "wickets" in delivery and "fielders" in delivery["wickets"][0] else "NA"
                        })

            innings_df = pd.DataFrame(innings_data)
            deliveries_df = pd.DataFrame(deliveries_data)

            return {
                "match": match_df,
                # "teams": teams_df,
                "players": players_df,
                "innings": innings_df,
                "deliveries": deliveries_df
            }

    def save_to_csv(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        pd.concat(self.matches_list).to_csv(os.path.join(output_dir, "matches.csv"), index=False)
        # pd.concat(self.teams_list).to_csv(os.path.join(output_dir, "teams.csv"), index=False)
        pd.concat(self.players_list).to_csv(os.path.join(output_dir, "players.csv"), index=False)
        pd.concat(self.innings_list).to_csv(os.path.join(output_dir, "innings.csv"), index=False)
        pd.concat(self.deliveries_list).to_csv(os.path.join(output_dir, "deliveries.csv"), index=False)

    def clean_dataframe(self, df):
        # print(f"{df.info()}")
        # print (f"{df.isna().any()}")
        # print (f"{df.isna().any().sum()}")
        df.drop_duplicates(inplace=True)              # Remove duplicates
        df.dropna(how="all", inplace=True)              # Drop empty rows
        # df.fillna(value={"player_of_match": ""}, inplace=True) if "player_of_match" in df.columns else df

        # Fill NaN for text columns with empty string
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].fillna("")

        # Fill NaN for numeric columns with 0
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].fillna(0)

        # print (f"{df.isna().any()}")
        # print (f"{df.isna().any().sum()}")
        return df

    def save_to_db(self):
        cricketDB = CricketDatabase()
        DIRECTORY = "cric_data"

        # with os.scandir(DIRECTORY) as entries:
        #     for entry in entries:
        #         print(f"Processing entry: {entry.name} at {entry.path}")
        #         if entry.is_file():
        #             if entry.name.endswith('.csv'):
        #                 # data_df = pd.read_csv(entry.path)
        #                 print (f"{entry.path}")
        #                 filepath = os.path.join(DIRECTORY, "matches.csv")
        #                 data_df = pd.read_csv(filepath)
        #                 # data_df = pd.read_csv(entry.path)
        #                 data_df = self.clean_dataframe(data_df)
        #                 cricketDB.save_to_db(data_df, "Matches", "matches_table")
        #                 # table_name = Path(entry.path).stem
        #                 # print (f"table Name: ------ {table_name.title()}")
        #                 # cricketDB.save_to_db(data_df, table_name.title(), table_name + "_table")
        #                 break

        file_name = os.path.join(DIRECTORY, "matches.csv")
        data_df = pd.read_csv(file_name)
        data_df = self.clean_dataframe(data_df)
        cricketDB.save_to_db(data_df, "Matches", matches_table)

        file_name = os.path.join(DIRECTORY, "players.csv")
        data_df = pd.read_csv(file_name)
        data_df = self.clean_dataframe(data_df)
        cricketDB.save_to_db(data_df, "Players", players_table)

        file_name = os.path.join(DIRECTORY, "innings.csv")
        data_df = pd.read_csv(file_name)
        data_df = self.clean_dataframe(data_df)
        cricketDB.save_to_db(data_df, "Innings", innings_table)

        file_name = os.path.join(DIRECTORY, "deliveries.csv")
        data_df = pd.read_csv(file_name)
        data_df = self.clean_dataframe(data_df)
        cricketDB.save_to_db(data_df, "Deliveries", deliveries_table)