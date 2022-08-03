from Src.main import *
from form_nav import *
from word_scraper import *

formNav = FormNavigator(basic_link=basic_link,
                        website_page=website_page, driver_path=driver_path, time_out=time_out,
                        broswer_vis=browser_visible)

wordScraper = DiscourseWordScraper(basic_link=basic_link, website_page=website_page, time_zone=time_zone,
                                   specific_classes=["cooked"])

numOfLink = formNav.get_num_of_link()

while num_of_links_needed != numOfLink:
    formNav.scroll_page(num_of_times="2")
    formNav.get_page_html()
    formNav.get_link()
    numOfLink = formNav.get_num_of_link()

    if num_of_links_needed < numOfLink:
        formNav.remove_link(numOfLink - num_of_links_needed)
        break

while num_of_links_needed != num_of_form_scraped:

    try:
        myData = []
        oldData = []

        formNav.set_link("/t/")
        formNav.scroll_page(user_request="up")

        metaData = formNav.get_page_meta()

        numOfScroll = 0

        while True:

            data = formNav.get_page_html()

            wordScraper.set_var(html_data=str(data[0]), website_page=data[2])
            html = wordScraper.get_by_class()

            newData = [x for x in [i for i in
                                   html[0]] if x not in oldData]

            if numOfScroll == 0:
                myData.extend(wordScraper.validate_input(temp_data=newData, type_cases=html[1], stats_dict=metaData))

            else:
                myData.extend(wordScraper.validate_input(temp_data=newData))

            oldData = newData

            if formNav.scroll_page(num_of_times=1, user_request="down"):
                wordScraper.save_CSV(final_input=myData)
                num_of_form_scraped += 1
                break

            numOfScroll += 1

    except AttributeError:
        print("website Error (Deleted Post, bad connection, invalid post, etc)")
