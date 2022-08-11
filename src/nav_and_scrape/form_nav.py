import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class FormNavigator:
    """Navigates forms, gets all the links, sets links and provides MetaData/HTML to wordScraper"""

    def __init__(self, basic_link, website_page, driver_path, time_out, broswer_vis):

        self.basic_link = basic_link
        self.website_page = website_page
        self.current_link = basic_link + website_page
        self.driver_path = driver_path
        self.time_out = time_out
        self.link_stored = list()
        self.b_soup = None

        sel_service = Service(self.driver_path)
        option = webdriver.ChromeOptions()
        option.add_argument('--incognito')

        if not broswer_vis:
            option.add_argument("--headless")

        self.driver = webdriver.Chrome(service=sel_service, options=option)
        self.driver.get(f'{self.current_link}')

    def scroll_page(self, user_request="down", num_of_times="infinite"):

        # Scrolls page differently based on what type of page you are on

        time.sleep(self.time_out)
        at_bottom = None
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        if num_of_times == "infinite":

            while True:

                if user_request == "up":
                    self.driver.execute_script("window.scrollTo(0,0)")
                elif user_request == "down":
                    new_height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(self.time_out)
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if last_height == new_height:
                    at_bottom = True
                    break

                last_height = new_height


        else:

            count = 0
            new_height = ""

            while count != int(num_of_times):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.time_out)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                count += 1

            if last_height == new_height:
                at_bottom = True

        return at_bottom

    def get_page_html(self):

        # Gets HTML of specific page user is on

        self.b_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self.b_soup, self.basic_link, self.website_page

    def get_page_meta(self):

        # Gets page metadata, and returns it in dict format

        time_now = datetime.now()
        self.b_soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:

            info_u_list = self.b_soup.find("div", class_="topic-map")

            date_list = [date.get("title") for date in info_u_list.find_all("span", class_="relative-date") if
                         date.get("title") is not None][0:2]

            li_numbers = [num.text if num.text is not None and not (num.text[-1] == "k") else num.get("title")
                          for num in info_u_list.find_all("span", class_="number")]

            des_text = [decs.text for decs in info_u_list.find_all("h4") if decs.text is not None]
            meta_data_dict = {des_text[string]: (date_list + li_numbers)[string] for string in range(len(des_text))}

            if "likes" not in meta_data_dict and "like" not in meta_data_dict: meta_data_dict["likes"] = "0"
            if "links" not in meta_data_dict and "link" not in meta_data_dict: meta_data_dict["links"] = "0"

            meta_data_dict["date-scraped"] = time_now.strftime(f'%b %d, %Y %I:%M:%S %p')
            meta_data_dict["title"] = self.b_soup.find("a", class_="fancy-title").text.strip()

            return meta_data_dict

        except AttributeError:

            meta_data_dict = {'title': f'{self.b_soup.find("a", class_="fancy-title").text.strip()}',
                              'date-scraped': f"{time_now.strftime('%b %d, %Y %I:%M:%S %p')}",
                              'created': f'{self.b_soup.find("span", class_="relative-date").get("title")}',
                              'last reply': 'No-Date', 'replies': '0', 'views': 'Unknown', 'users': '1',
                              'likes': 'Unknown',
                              'links': 'Unknown'}

        return meta_data_dict

    def get_link(self):
        # gets all pages on link which will be needed for scraping

        for a_tag in self.b_soup.find_all("a"):

            try:
                a_tag = (a_tag.get("href")).rsplit('/', 1)[0]

                if a_tag.startswith("/t/") and a_tag.count("/") == 2:
                    a_tag += "/"
                    self.link_stored.append(a_tag)

            except AttributeError as a:
                continue

        self.link_stored = list(dict.fromkeys(self.link_stored))

    def get_num_of_link(self):
        # Returns number of links
        return len(self.link_stored)

    def remove_link(self, num):
        # removes links if to many are received

        for nu in range(0, num):
            self.link_stored.pop()

    def set_link(self, user_request):
        # Sets page link, and removes it from Set

        try:
            self.website_page = self.link_stored[0]
            self.current_link = self.basic_link + self.website_page
            self.driver.get(self.current_link)
            self.link_stored.pop(0)

            return self.current_link, user_request

        except IndexError:
            print("out of links!")
            quit()
