import csv
import re

from bs4 import BeautifulSoup


class discourseWordScraper:

    def __init__(self, basicLink, websitePage, timeZone,specificClasses=None):

        self.specificClasses = specificClasses
        self.basicLink = basicLink
        self.websitePage = websitePage

        self.timeZone = timeZone

        self.bSoup = None

    def setVar(self, htmlData, websitePage):
        self.bSoup = BeautifulSoup(htmlData.strip(), 'html.parser')
        self.websitePage = websitePage

    def getByClass(self):

        tempData = list()

        for classTxt in self.specificClasses:
            tempData += self.bSoup.find_all(class_=classTxt)

        return ([re.split('[,.\s/]', x.text) for x in tempData], self.specificClasses)

    def validateInput(self, tempData, typeCases=None, statsDict=None):

        blackList = ["http", "img", "<p>"]  # <- NEEDS INPUT TO RUN
        regex = re.compile("[^a-zA-Z-/_']")
        finalInput = list()

        for rawSentence in tempData:
            rawInput = ([regex.sub('', string.lower()) for string in rawSentence])
            finalInput.extend([string for string in rawInput if
                               any(blackTag in string for blackTag in blackList) is False and string != ""])

        if statsDict is not None and typeCases is not None:
            finalInput.insert(0, statsDict["title"])
            finalInput.insert(1, statsDict["date-scraped"] + " MDT")
            finalInput.insert(2, (self.basicLink + self.websitePage))
            finalInput.insert(3, statsDict["created"] + " MDT")
            finalInput.insert(4, statsDict["last reply"] + " MDT")

            try:
                finalInput.insert(5, statsDict["replies"])
            except:
                finalInput.insert(5, statsDict["reply"])

            try:
                finalInput.insert(6, statsDict["views"])
            except:
                finalInput.insert(6, statsDict["view"])

            try:
                finalInput.insert(7, statsDict["users"])
            except:
                finalInput.insert(7, statsDict["user"])

            try:
                finalInput.insert(8, statsDict["likes"])
            except:
                finalInput.insert(8, statsDict["like"])

            try:
                finalInput.insert(9, statsDict["links"])
            except:
                finalInput.insert(9, statsDict["link"])

            finalInput.insert(10, typeCases)

        return finalInput

    def saveCSV(self, finalInput):

        with open('../../Data_Collected/data_collected.csv', 'r', encoding="utf-8") as dfr, open(
                '../../Data_Collected/data_collected.csv', 'a+', newline='',
                encoding="utf-8") as dfw:
            writer = csv.writer(dfw, delimiter=',')
            reader = csv.reader(dfr)

            writer.writerow(finalInput)
