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

# Auto run module
from nav_and_scrap import connector

# Number of forms needed to be scraped
num_of_links_needed = 50
# Number of forms already scraped and in CSV file
num_of_form_scraped = 0

# Form website link
basic_link = "https://forums.unrealengine.com"

# Form website specific category
website_page = "/c/development-discussion/programming-scripting/148"

# Path to the webdriver
driver_path = "C:/Users/dilsh/Downloads/chromedriver_win32/chromedriver.exe"

# time out needed between events, based on Wi-Fi
time_out = 0.5

# Timezone which data is being recorded 
time_zone = "MDT"

# Boolean which controls if the browser activities will be shown on screen on or not
browser_visible = False

if __name__ == "__main__":
    # function to start the connector between formNav and WordScraper

    connector.run_connector()
