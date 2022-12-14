import csv
import re

from bs4 import BeautifulSoup


class DiscourseWordScraper:
    """Scrapes the HTML provided by the FormNav, and presents it in a CSV file along with Metadata"""

    def __init__(self, basic_link, website_page, time_zone, specific_classes):

        # Required information to run

        self.specific_classes = specific_classes
        self.basic_link = basic_link
        self.website_page = website_page
        self.time_zone = " " + time_zone
        self.b_Soup = None

    def set_var(self, html_data, website_page):

        # Changes class self-variables, which will be used later. Also gets rid of certain tags on the page

        self.b_Soup = BeautifulSoup(html_data.strip(), 'html.parser')
        self.website_page = website_page

        for tag in self.b_Soup(["blockquote", "img", "aside", "a"]):
            tag.decompose()

    def get_by_class(self):

        # Gets elements based of class specified by user, returns a list of words and the class which was used

        temp_data = list()

        for class_txt in self.specific_classes:
            temp_data += self.b_Soup.find_all(class_=class_txt)

        return [re.split('[,.\s/]', x.text) for x in temp_data], self.specific_classes

    def validate_input(self, temp_data, type_cases=None, stats_dict=None):

        # Final formatting for the input, to be converted into a one dimensional list, with all page words and data

        black_list = ["kb"]  # <- NEEDS INPUT TO RUN
        regex = re.compile("[^a-zA-Z-/_']")
        text_input = list()

        for raw_sentence in temp_data:
            raw_input = ([regex.sub('', raw_word.lower()) for raw_word in raw_sentence])
            text_input.extend([word for word in raw_input if
                               any(blackTag in word for blackTag in black_list) is False and word != ""])

        meta_input = list()

        if stats_dict is not None and type_cases is not None:
            meta_input.insert(0, stats_dict["title"])
            meta_input.insert(1, stats_dict["date-scraped"] + self.time_zone)
            meta_input.insert(2, (self.basic_link + self.website_page))
            meta_input.insert(3, stats_dict["created"] + self.time_zone)
            meta_input.insert(4, stats_dict["last reply"] + self.time_zone)

            try:
                meta_input.insert(5, stats_dict["replies"])
            except KeyError:
                meta_input.insert(5, stats_dict["reply"])

            try:
                meta_input.insert(6, stats_dict["views"])
            except KeyError:
                meta_input.insert(6, stats_dict["view"])

            try:
                meta_input.insert(7, stats_dict["users"])
            except KeyError:
                meta_input.insert(7, stats_dict["user"])

            try:
                meta_input.insert(8, stats_dict["likes"])
            except KeyError:
                meta_input.insert(8, stats_dict["like"])

            try:
                meta_input.insert(9, stats_dict["links"])
            except KeyError:
                meta_input.insert(9, stats_dict["link"])

            meta_input.insert(10, type_cases)

        finalInput = meta_input.copy()
        finalInput.append(text_input)

        return finalInput

    def save_csv(self, final_input):

        # Saves final_input list to CSV

        with open('data_collected/form_data_collected.csv', 'r', encoding="utf-8"), open(
                'data_collected/form_data_collected.csv', 'a+', newline='', encoding="utf-8") as dfw:
            writer = csv.writer(dfw, delimiter=',')
            writer.writerow(final_input)
