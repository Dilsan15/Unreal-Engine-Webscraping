from nav_and_scrape import *

"""Connector uses methods from both classes to accomplish task of scraping multiple forms autonmously"""


def run_connector(num_of_links_needed, basic_link, website_page, driver_path, time_out, time_zone, browser_visible):
    # Initiate both classes, which will have variables changed later

    f_nav = FormNavigator(basic_link=basic_link,
                          website_page=website_page, driver_path=driver_path, time_out=time_out,
                          broswer_vis=browser_visible)

    w_scrape = DiscourseWordScraper(basic_link=basic_link, website_page=website_page,
                                    time_zone=time_zone,
                                    specific_classes=["cooked"])

    # Gets appropriate number of links from webpage

    num_of_link = f_nav.get_num_of_link()
    num_of_form_scraped = 0

    while num_of_links_needed > num_of_link:
        f_nav.scroll_page(num_of_times="2")
        f_nav.get_page_html()
        f_nav.get_link()
        num_of_link = f_nav.get_num_of_link()

        if num_of_links_needed < num_of_link:
            f_nav.remove_link(num_of_link - num_of_links_needed)
            break

    # While loop which grabs HTML data, gets the content needed out of it, and saves it to CSV file. Breaks when all
    # link stored are used.

    while num_of_links_needed != num_of_form_scraped:

        try:
            word_list = []
            old_data = []

            f_nav.set_link("/t/")
            f_nav.scroll_page(user_request="up")

            meta_data = f_nav.get_page_meta()


            while True:

                data = f_nav.get_page_html()

                w_scrape.set_var(html_data=str(data[0]), website_page=data[2])
                html_class = w_scrape.get_by_class()
                new_data = [sentence for sentence in [class_list for class_list in
                                                      html_class[0]] if sentence not in old_data]

                old_data.extend(new_data)
                word_list.extend(new_data)

                if f_nav.scroll_page(num_of_times=1, user_request="down"):
                    w_scrape.save_csv(final_input=w_scrape.validate_input(temp_data=word_list, type_cases=html_class[1],
                                                                          stats_dict=meta_data))
                    num_of_form_scraped += 1
                    break

        except AttributeError:

            # Epic not removing deleted form links off of their website Error handled
            print("website Error (Deleted Post, bad connection, invalid post, etc)")
