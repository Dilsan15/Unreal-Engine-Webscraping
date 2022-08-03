from src.main import *
from src.nav_and_scrap import form_nav
from src.nav_and_scrap import word_scraper

# Initiate both classes, which will have variables changed later

formNav = form_nav.FormNavigator(basic_link=basic_link,
                                 website_page=website_page, driver_path=driver_path, time_out=time_out,
                                 broswer_vis=browser_visible)

wordScraper = word_scraper.DiscourseWordScraper(basic_link=basic_link, website_page=website_page, time_zone=time_zone,
                                                specific_classes=["cooked"])


# Gets appropiate number of links from webpage

numOfLink = formNav.get_num_of_link()

while num_of_links_needed != numOfLink:
    formNav.scroll_page(num_of_times="2")
    formNav.get_page_html()
    formNav.get_link()
    numOfLink = formNav.get_num_of_link()

    if num_of_links_needed < numOfLink:
        formNav.remove_link(numOfLink - num_of_links_needed)
        break

# While loop which grabs HTML data, gets the content needed out of it, and saves it to CSV file. Breaks when all link
# stored are used.

while num_of_links_needed != num_of_form_scraped:

    try:
        my_data = []
        old_data = []

        formNav.set_link("/t/")
        formNav.scroll_page(user_request="up")

        meta_data = formNav.get_page_meta()

        num_of_scroll = 0

        while True:

            data = formNav.get_page_html()

            wordScraper.set_var(html_data=str(data[0]), website_page=data[2])
            html = wordScraper.get_by_class()

            new_data = [x for x in [i for i in
                                    html[0]] if x not in old_data]

            if num_of_scroll == 0:
                my_data.extend(wordScraper.validate_input(temp_data=new_data, type_cases=html[1], stats_dict=meta_data))

            else:
                my_data.extend(wordScraper.validate_input(temp_data=new_data))

            oldData = new_data

            if formNav.scroll_page(num_of_times=1, user_request="down"):
                wordScraper.save_csv(final_input=my_data)
                num_of_form_scraped += 1
                break

            num_of_scroll += 1

    except AttributeError:

        # Epic not removing deleted form links off of there website Error handled

        print("website Error (Deleted Post, bad connection, invalid post, etc)")
