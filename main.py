from form_nav import *
from word_scraper import *

if __name__ == "__main__":
    formNav = formNavigator(basicLink="https://forums.unrealengine.com",
                            websitePage="/c/development-discussion/programming-scripting/148")

    startPageData = formNav.getPageHtml()
    wordScraper = discourseWordScraper(basicLink=startPageData[1], websitePage=startPageData[2], specificTags=["p"])

    numIter = 0

    while numIter != 110:

        formNav.scrollPage(numOfTimes="3")
        formNav.getPageHtml()
        formNav.getLink()

        if numIter >= 10:

            myData = []
            oldData = []

            formNav.setLink("/t/")
            formNav.scrollPage(userRequest="up")

            metaData = formNav.getPageMeta()

            while True:

                data = formNav.getPageHtml()

                wordScraper.setVar(htmlData=str(data[0]), websitePage=data[2])
                html = wordScraper.getByTag()

                newData = [i for i in wordScraper.validateInput(tempData=html[0], typeCases=html[1], statsDict=metaData) if
                           i not in oldData]
                myData.extend(newData)

                oldData = newData

                if formNav.scrollPage(numOfTimes=1, userRequest="down"):
                    wordScraper.saveCSV(finalInput=myData)
                    break

