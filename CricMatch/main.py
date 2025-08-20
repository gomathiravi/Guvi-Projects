from cric_data_scrapper import Scrape_Data as Scraper
from cric_data_parser import DataParser
# from cric_data_base import CricketDatabase
import cric_data_plot as cd_plot

DOWNLOAD_DIR = "downloaded_jsons"
WEBPAGE_URL = "https://cricsheet.org/"

if __name__ == "__main__":

    # Run the scrapper code to download cricket data set from the given web page
    scraper = Scraper(WEBPAGE_URL)
    links = scraper.extract_dt_dd_links()
    scraper.download_files(links, DOWNLOAD_DIR)
    scraper.close_webDriver()
    print(f"All files downloaded to {DOWNLOAD_DIR}")

    # run the data parser to unzip
    parser = DataParser(DOWNLOAD_DIR)
    parser.unzip_files()

    # parser to parse the directories for reading all the json files into dataFrames
    parser.parse_directory()
    parser.save_to_csv("cric_data")

    # Initialize the cricket database and store the parsed data deliveries, innings, matches, players, and teams
    # into the tables in the database
    parser.save_to_db()

    # class to plot various insights referring the parsed data sets.
    cd_plot.load_insights()