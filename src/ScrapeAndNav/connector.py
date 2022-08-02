from src.main import *

formNav = formNavigator(basicLink=BASIC_LINK,
                        websitePage=WEBSITE_PAGE, driverPath=DRIVER_PATH, timeOut=TIME_OUT,
                        broswerVis=BROWSER_VISIBLE)

wordScraper = discourseWordScraper(basicLink=BASIC_LINK, websitePage=WEBSITE_PAGE, timeZone=TIME_ZONE,
                                   specificClasses=["cooked"])

numOfLink = formNav.getNumOfLink()

while NUM_OF_LINKS_NEEDED != numOfLink:
    formNav.scrollPage(numOfTimes="2")
    formNav.getPageHtml()
    formNav.getLink()
    numOfLink = formNav.getNumOfLink()

    if NUM_OF_LINKS_NEEDED < numOfLink:
        formNav.removeLink(numOfLink - NUM_OF_LINKS_NEEDED)
        break

while NUM_OF_LINKS_NEEDED != NUM_OF_FORM_SCRAPED:

    try:
        myData = []
        oldData = []

        formNav.setLink("/t/")
        formNav.scrollPage(userRequest="up")

        metaData = formNav.getPageMeta()

        numOfScroll = 0

        while True:

            data = formNav.getPageHtml()

            wordScraper.setVar(htmlData=str(data[0]), websitePage=data[2])
            html = wordScraper.getByClass()

            newData = [x for x in [i for i in
                                   html[0]] if x not in oldData]

            if numOfScroll == 0:
                myData.extend(wordScraper.validateInput(tempData=newData, typeCases=html[1], statsDict=metaData))

            else:
                myData.extend(wordScraper.validateInput(tempData=newData))

            oldData = newData

            if formNav.scrollPage(numOfTimes=1, userRequest="down"):

                wordScraper.saveCSV(finalInput=myData)
                NUM_OF_FORM_SCRAPED += 1
                break

            numOfScroll += 1

    except AttributeError:
        print("website Error (Deleted Post, bad connection, invalid post, etc)")
