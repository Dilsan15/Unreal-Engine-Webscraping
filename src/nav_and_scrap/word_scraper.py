import csv
import re
from bs4 import BeautifulSoup


class DiscourseWordScraper:

    def __init__(self, basic_link, website_page, time_zone, specific_classes):

        # Required information to run

        self.specific_classes = specific_classes
        self.basic_link = basic_link
        self.website_page = website_page
        self.time_zone = time_zone
        self.b_Soup = None

    def set_var(self, html_data, website_page):

        # Changes class self-variables

        self.b_Soup = BeautifulSoup(html_data.strip(), 'html.parser')
        self.website_page = website_page

    def get_by_class(self):

        # Gets elements based of class specified by user, returns a list of words and the class which was used

        temp_data = list()

        for class_txt in self.specific_classes:
            temp_data += self.b_Soup.find_all(class_=class_txt)

        return [re.split('[,.\s/]', x.text) for x in temp_data], self.specific_classes

    def validate_input(self, temp_data, type_cases=None, stats_dict=None):

        # Final formating for the input, to be converted into a one dimensional list, with all page words and data

        black_list = ["http", "img", "<p>"]  # <- NEEDS INPUT TO RUN
        regex = re.compile("[^a-zA-Z-/_']")
        final_input = list()

        for raw_sentence in temp_data:
            raw_input = ([regex.sub('', string.lower()) for string in raw_sentence])
            final_input.extend([string for string in raw_input if
                                any(blackTag in string for blackTag in black_list) is False and string != ""])

        if stats_dict is not None and type_cases is not None:
            final_input.insert(0, stats_dict["title"])
            final_input.insert(1, stats_dict["date-scraped"] + " MDT")
            final_input.insert(2, (self.basic_link + self.website_page))
            final_input.insert(3, stats_dict["created"] + " MDT")
            final_input.insert(4, stats_dict["last reply"] + " MDT")

            try:
                final_input.insert(5, stats_dict["replies"])
            except KeyError:
                final_input.insert(5, stats_dict["reply"])

            try:
                final_input.insert(6, stats_dict["views"])
            except KeyError:
                final_input.insert(6, stats_dict["view"])

            try:
                final_input.insert(7, stats_dict["users"])
            except KeyError:
                final_input.insert(7, stats_dict["user"])

            try:
                final_input.insert(8, stats_dict["likes"])
            except KeyError:
                final_input.insert(8, stats_dict["like"])

            try:
                final_input.insert(9, stats_dict["links"])
            except KeyError:
                final_input.insert(9, stats_dict["link"])

            final_input.insert(10, type_cases)

        return final_input

    def save_csv(self, final_input):

        # Saves final_input list to CSV

        with open('data_Collected/form_data_collected.csv', 'r', encoding="utf-8"), open(
                'data_Collected/form_data_collected.csv', 'a+', newline='', encoding="utf-8") as dfw:
            writer = csv.writer(dfw, delimiter=',')
            writer.writerow(final_input)
