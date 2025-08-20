import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from urllib.parse import urljoin, urlparse
import os
import requests

MATCH_TYPES = ["Test matches", "One-day internationals", "T20 internationals", "Indian Premier League"]

class Scrape_Data:
    def __init__(self, url):
        self.web_url = url
        self.driver = webdriver.Chrome('')  # Optional argument, if not specified will search path.
        self.driver.get(self.web_url)
        time.sleep(5) # Let the user actually see something!

    def close_webDriver(self):
        # Close the browser after the task is done
        self.driver.quit()

    def download_files(self, links, download_dir):
        os.makedirs(download_dir, exist_ok=True)

        # Filter and download files in .zip format
        for url in links:
            if url.lower().endswith(".zip"):
                response = requests.get(url)
                if response.status_code == 200:
                    filename = os.path.basename(urlparse(url).path)
                    filepath = os.path.join(download_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {url}")

    def extract_dt_dd_links(self):
        # Find the dropdown list box using its class name: 'selectnav'
        listBox = self.driver.find_element(By.XPATH, "//select[@class='selectnav']")
        print(f"List Box: {listBox.text}")

        # Select the dropdown list box using the Select class
        # and select the option with visible text "Match data" and navigate to it.
        dd = Select(listBox)
        dd.select_by_visible_text("Match data")

        time.sleep(5) # Let the user actually see something!

        # Simulate key press (e.g., scrolling down the page)
        body = self.driver.find_element(By.TAG_NAME, "body")
        for i in range(2):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Wait for the page to load after scrolling

        # Find all <dt> elements
        dt_elements = self.driver.find_elements(By.TAG_NAME, "dt")

        absolute_href = None
        target_hrefs = []

        for match_type in MATCH_TYPES:
            for dt in dt_elements:
                if dt.text.strip() == match_type:
                    # Find the next sibling <dd>
                    dd = dt.find_element(By.XPATH, "following-sibling::dd[1]")

                    # Find <a> inside that <dd>
                    link = dd.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    absolute_href = urljoin(self.web_url, href)
                    # print(f"Found href for '{match_type}': {absolute_href}")
                    target_hrefs.append(absolute_href)
                    break
        # print(f"Target Hrefs: {target_hrefs}")
        return target_hrefs