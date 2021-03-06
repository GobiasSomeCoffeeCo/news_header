import re
from typing import List

import bs4
from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from rich import print
from rich.progress import track
# import tqdm



class NewsHead:
    def __init__(self):
        pass

        # self.links = []
        # self.headlines = []

    # TODO: A lot of DRY code. See about making it one function and passing in a dict or JSON?
    # TODO: NYTimes headline feature broken
    
    def get_nytimes_headlines(self):
        resp = requests.get("https://www.nytimes.com/")
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        headline = soup.find_all("h2", class_="css-1ayculb e1voiwgp0")
        a_tags = soup.find_all('div', class_='css-6p6lnl')
        links = []
        headlines = []
        for article in headline:
        #     link = article.a.get("href")
            article = article.text
            headlines.append(article)
            # links.append(link)
        for tag in a_tags:
            tag = tag.a.get('href')
            links.append(tag)
        return headlines, links

    def get_washpost_headlines(self) -> List:
        resp = requests.get("https://www.washingtonpost.com/")
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        headline = soup.find_all("h2", class_=(re.compile("headline")), limit=12)
        links = []
        headlines = []
        try:
            for article in headline:
                link = article.a.get("href")
                article = article.text.replace(u"\xa0", u" ")
                headlines.append(article)
                links.append(link)
        except AttributeError:
            pass
        return headlines, links

    def get_atlantic_headlines(self) -> List:
        resp = requests.get("https://www.theatlantic.com/")
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        headline = soup.find_all("a", class_=(re.compile("hed-link")))
        links = []
        headlines = []  # [main_headline]
        try:
            for article in headline:
                link = article.get("href")
                article = article.text
                headlines.append(article)
                links.append(link)
        except AttributeError:
            pass
        return headlines, links

    def get_politico_headlines(self) -> List:
        resp = requests.get("https://www.politico.com/")
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        headline = soup.find_all("h3", class_="headline")
        links = []
        headlines = []
        try:
            for article in headline:
                link = article.a.get("href")
                article = article.text
                article = re.sub(r"\s+", " ", article)
                headlines.append(article)
                links.append(link)
        except AttributeError:
            pass
        return headlines, links

    def get_wsj_headlines(self) -> List:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        resp = requests.get("https://www.wsj.com/", headers=headers)
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        headline = soup.find_all("h3", class_=(re.compile("WSJTheme--headline")), limit=20)
        links = []
        headlines = []
        try:
            for article in headline:
                link = article.a.get("href")
                article = article.text
                links.append(link)
                headlines.append(article)
        except AttributeError:
            pass
        return headlines, links

# news = NewsHead()
# x, y = news.get_nytimes_headlines()
# print(x, y)
