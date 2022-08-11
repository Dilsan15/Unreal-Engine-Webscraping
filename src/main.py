"""

Process:

Main ------> Connector  ----> FormNav ------> Discourse Word Scraper ------> CSV File
                                (Looped)

Main: sets variables which will be used in the execution of project, runs connector
Connector: Controls FormNav and connects the word scraper and FormNav together
FormNav: Navigates pages, get links on pages, sets URL, Sends html data to wordscraper
Discourse Word Scraper: Gets HTML from form, parses it into individual words, and sends it to CSV File
CSV File: Includes page meta data (date posted, views, replies, etc) and individual words of multiple form pages

"""

# import connector and OS for env variables
import os

from connector import connector_logic

# Number of forms needed to be scraped
num_of_links_needed = 700

# Form website link
basic_link = "https://forums.unrealengine.com"

# Link to a specific category
website_page = "/c/development-discussion/asset-creation/151"

# Path to the webdriver, saved as env
driver_path = os.environ["DRIVER_PATH"]  # Todo("CHANGE THIS TO UR PATH! so it
# looks like driver_path = 'YOUR STRING' ")

# time out needed between events, based on Wi-Fi and PC performance
time_out = 0.5

# Timezone which data is being recorded 
time_zone = "MDT"

# Boolean which controls if the browser activities will be shown on screen on or not
browser_visible = True

if __name__ == "__main__":
    # function to start the connector between formNav and WordScraper
    connector_logic.run_connector(num_of_links_needed, basic_link, website_page, driver_path, time_out, time_zone,
                                  browser_visible)
