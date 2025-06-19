import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

USERNAME = "shruthahegde_BIVNbn"
ACCESS_KEY = "eWHgcm43bPSXAay5Qw2q"
BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

capabilities_list = [
    {
        "browserName": "Chrome",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "El Pais Chrome Test"
    },
    {
        "browserName": "Firefox",
        "os": "OS X",
        "osVersion": "Monterey",
        "sessionName": "El Pais Firefox Test"
    },
    {
        "browserName": "Edge",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "El Pais Edge Test"
    },
    {
        "deviceName": "iPhone 14",
        "realMobile": "true",
        "osVersion": "16",
        "sessionName": "El Pais iPhone Test"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "osVersion": "12.0",
        "sessionName": "El Pais Android Test"
    }
]

def getOpinionPageUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    navs = soup.find_all("nav")
    for nav in navs:
        opinion_link = nav.find("a", string="Opinión")
        if opinion_link:
            return opinion_link["href"]

def printFiveTopOpinionArticles(opinionPageUrl):
    response = requests.get(opinionPageUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    main_tag = soup.find("main")
    articles = main_tag.find_all("article")

    articleNameList = []
    articleLinkList = []
    printedHeaders = []
    for article in articles:
        h2 = article.find("h2")
        if not h2 or not h2.find("a"):
            continue
        articleLink = h2.find("a")["href"]
        articleName = h2.text.strip()
        articleNameList.append(articleName)
        articleLinkList.append(articleLink)

    count = 0
    for i in range(len(articleLinkList)):
        articleLink = articleLinkList[i]
        articleName = articleNameList[i]
        response = requests.get(articleLink)
        soup = BeautifulSoup(response.text, "html.parser")
        mainContent = soup.find("article", id="main-content")
        if mainContent:
            contentDiv = mainContent.find("div", class_="a_c clearfix")
            if contentDiv:
                paras = contentDiv.find_all("p")
                if paras:
                    printedHeaders.append(articleName)
                    print(f"{count+1}) {articleName} : {articleLink}")
                    for p in paras:
                        print(p.text.strip())
                    count += 1
        if count == 5:
            return printedHeaders

def getTranslatedArticleHeaders(printedHeaders):
    translatedTitles = []
    print("\n Translated Titles:")
    for printedHeader in printedHeaders:
        response = callGoogleTranslate(printedHeader).json().get("trans")
        translatedTitles.append(response)
        print(response)
    return translatedTitles

def callGoogleTranslate(text):
    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
    header = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "google-translate113.p.rapidapi.com",
        "x-rapidapi-key": "ae3fff85d4msh8cda2e10c127ca0p1bf655jsnb64878fed31c"
    }
    data = {
        "from": "es",
        "to": "en",
        "text": text
    }
    return requests.post(url, json=data, headers=header)

def printRepeatedWordsCounter(titles):
    print("\n Repeated words from translated titles:")
    words = []
    wordMap = {}
    for title in titles:
        words.extend(title.lower().split())
    sanitizedWords = sanitizeWords(words)
    for word in sanitizedWords:
        wordMap[word] = wordMap.get(word, 0) + 1
    for word, count in wordMap.items():
        if count > 1:
            print(f"{word} : {count}")

def sanitizeWords(words):
    return [''.join(c for c in word if c.isalpha()) for word in words if ''.join(c for c in word if c.isalpha())]

def run_browserstack_test(cap):
    print(f"\n Starting test: {cap.get('browserName', cap.get('deviceName'))}")

    # Setup Options object and set capabilities
    options = ChromeOptions()
    for key, value in cap.items():
        if key in ["browserName", "deviceName"]:
            continue
        options.set_capability(f"bstack:options", cap)

    if "browserName" in cap:
        options.set_capability("browserName", cap["browserName"])
    else:
        options.set_capability("deviceName", cap["deviceName"])

    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )

    try:
        driver.get("https://elpais.com")
        time.sleep(3)
        opinion_url = getOpinionPageUrl("https://elpais.com")
        printedHeaders = printFiveTopOpinionArticles(opinion_url)
        translatedTitles = getTranslatedArticleHeaders(printedHeaders)
        printRepeatedWordsCounter(translatedTitles)
    except Exception as e:
        print(f" Error during test: {e}")
    finally:
        driver.quit()
def main():
    websiteUrl = "https://elpais.com"
    opinionUrl = getOpinionPageUrl(websiteUrl)
    printedHeaders = printFiveTopOpinionArticles(opinionUrl)
    translatedTitles = getTranslatedArticleHeaders(printedHeaders)
    printRepeatedWordsCounter(translatedTitles)
    return translatedTitles 
def main():
    for cap in capabilities_list:
        run_browserstack_test(cap)

if __name__ == "__main__":
    main()
