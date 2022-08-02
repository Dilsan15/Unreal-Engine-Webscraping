import csv
import re

from bs4 import BeautifulSoup


class discourseWordScraper:

    def __init__(self, basicLink, websitePage, specificTags=None):

        self.specificTags = specificTags
        self.basicLink = basicLink
        self.websitePage = websitePage

        self.specificClasses = specificClasses

        self.bSoup = None

    def setVar(self, htmlData, websitePage):
        self.bSoup = BeautifulSoup(htmlData.strip(), 'html.parser')
        self.websitePage = websitePage

    def getByTag(self):

        tempData = list()

        for tagTxt in self.specificTags:
            tempData += self.bSoup.find_all(tagTxt)

        return ([x.text.split('[,.\s]') for x in tempData], self.specificTags)

    def validateInput(self, tempData, typeCases, statsDict):

        blackList = ["http", "img", "<p>"]  # <- NEEDS INPUT TO RUN
        regex = re.compile("[^a-zA-Z-/_']")
        finalInput = list()

        for rawSentence in tempData:
            rawInput = ([regex.sub('', string.lower()) for string in rawSentence])
            finalInput.extend([string for string in rawInput if
                               any(blackTag in string for blackTag in blackList) is False and string != ""])

        finalInput.insert(0, statsDict["title"])
        finalInput.insert(1, statsDict["date-scraped"] + "MDT")
        finalInput.insert(2, (self.basicLink + self.websitePage))
        finalInput.insert(3, statsDict["created"] + "MDT")
        finalInput.insert(4, statsDict["last reply"] + "MDT")

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

        with open('Data_Collected/data_collected.csv', 'r', encoding="utf-8") as dfr, open(
                'Data_Collected/data_collected.csv', 'a+',
                newline='',
                encoding="utf-8") as dfw:
            writer = csv.writer(dfw, delimiter=',')

            writer.writerow(finalInput)
