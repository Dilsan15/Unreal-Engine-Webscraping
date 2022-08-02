import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class formNavigator:

    def __init__(self, basicLink, websitePage, driverPath, timeOut, broswerVis):

        self.basicLink = basicLink
        self.websitePage = websitePage
        self.currentLink = basicLink + websitePage

        self.driverPath = driverPath
        self.timeOut = timeOut

        self.linksStored = list()

        self.bSoup = None

        selService = Service(self.driverPath)

        option = webdriver.ChromeOptions()
        option.add_argument('--incognito')
        if not(broswerVis): option.add_argument("--headless")

        self.driver = webdriver.Chrome(service=selService, options=option)
        self.driver.get(f'{self.currentLink}')

    def scrollPage(self, userRequest="down", numOfTimes="infinite"):

        time.sleep(self.timeOut)
        atBottom = None
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        if numOfTimes == "infinite":

            while True:

                if userRequest == "up":
                    self.driver.execute_script("window.scrollTo(0,0)")
                elif userRequest == "down":
                    new_height = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(self.timeOut)

                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if last_height == new_height:
                    atBottom = True
                    break

                last_height = new_height

        else:

            count = 0

            while count != int(numOfTimes):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.timeOut)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                count += 1

            if last_height == new_height:
                atBottom = True

            else:
                last_height = new_height

        return atBottom

    def refreshPage(self):
        self.driver.refresh()

    def getPageHtml(self):

        with open("Data_Collected/html_stored.txt", "r+", encoding='utf-8') as htmlPage:
            htmlPage.write(self.driver.page_source)

        self.bSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self.bSoup, self.basicLink, self.websitePage

    def getPageMeta(self):

        now = datetime.now()
        self.bSoup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:

            infoUList = self.bSoup.find("div", class_="topic-map")

            dateList = [date.get("title") for date in infoUList.find_all("span", class_="relative-date") if
                        date.get("title") is not None][0:2]

            liNumbers = [num.text if num.text is not None and not (num.text[-1] == "k") else num.get("title")
                         for num in infoUList.find_all("span", class_="number")]

            desText = [decs.text for decs in infoUList.find_all("h4") if decs.text is not None]
            metaDataDict = {desText[string]: (dateList + liNumbers)[string] for string in range(len(desText))}

            if "likes" not in metaDataDict and "like" not in metaDataDict: metaDataDict["likes"] = "0"
            if "links" not in metaDataDict and "link" not in metaDataDict: metaDataDict["links"] = "0"

            metaDataDict["date-scraped"] = now.strftime(f'%b %d, %Y %I:%M:%S %p')
            metaDataDict["title"] = self.bSoup.find("a", class_="fancy-title").text.strip()

            return metaDataDict

        except AttributeError:

            metaDataDict = {'title': f'{self.bSoup.find("a", class_="fancy-title").text.strip()}',
                            'date-scraped': f"{now.strftime('%b %d, %Y %I:%M:%S %p')}",
                            'created': f'{self.bSoup.find("span", class_="relative-date").get("title")}',
                            'last reply': 'No-Date', 'replies': '0', 'views': 'Unknown', 'users': '1',
                            'likes': 'Unknown',
                            'links': 'Unknown'}

            return metaDataDict

    def getLink(self):

        for aTag in self.bSoup.find_all("a"):

            try:
                aTag = (aTag.get("href")).rsplit('/', 1)[0]

                if aTag.startswith("/t/") and aTag.count("/") == 2:
                    aTag += "/"
                    self.linksStored.append(aTag)

            except AttributeError as a:
                continue

        self.linksStored = list(dict.fromkeys(self.linksStored))

    def getNumOfLink(self):
        return len(self.linksStored)

    def removeLink(self, num):

        for nu in range(0, num):
            self.linksStored.pop()

    def setLink(self, userRequest):

        self.websitePage = self.linksStored[0]
        self.currentLink = self.basicLink + self.websitePage
        self.driver.get(self.currentLink)

        self.linksStored.pop(0)

        return self.currentLink, userRequest
