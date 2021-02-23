from logging import error
import re
from typing import List

import httpx
from httpx import Response
import bs4



class NewsHead:
    def __init__(self):
        pass

        # self.links = []
        # self.headlines = []

    # TODO: A lot of DRY code. See about making it one function and passing in a dict or JSON?
    # TODO: NYTimes headline feature broken
    
    async def get_nytimes_headlines(self) -> List:
        async with httpx.AsyncClient(timeout=None) as client:
            resp: Response = await client.get("https://www.nytimes.com/")
            if resp.status_code != 200:
                raise error(resp.text)
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
            print("Collected data for NYTimes...", flush=True)
            return headlines, links

    async def get_washpost_headlines(self) -> List:
        async with httpx.AsyncClient(timeout=None) as client:
            resp: Response = await client.get("https://www.washingtonpost.com/")
            if resp.status_code != 200:
                raise error(resp.text)
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
            print("Collected data for Washington Post...", flush=True)
            return headlines, links

    async def get_atlantic_headlines(self) -> List:
        async with httpx.AsyncClient(timeout=None) as client:
            resp: Response = await client.get("https://www.theatlantic.com/")
            if resp.status_code != 200:
                raise error(resp.text)
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
            print("Collected data for The Atlantic...", flush=True)
            return headlines, links

    async def get_politico_headlines(self) -> List:
        async with httpx.AsyncClient(timeout=None) as client:
            resp: Response = await client.get("https://www.politico.com/")
            if resp.status_code != 200:
                raise error(resp.text)
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
            print("Collected data for Politico...", flush=True)
            return headlines, links

    async def get_wsj_headlines(self) -> List:
        async with httpx.AsyncClient() as client:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            resp: Response = await client.get("https://www.wsj.com/", headers=headers)
            if resp.status_code != 200:
                raise error(resp.text)
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
            print("Collected data for WSJ...", flush=True)
            return headlines, links

    

