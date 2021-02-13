from typing import Type
import webbrowser
from re import search
from itertools import chain
from rich import print

from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    track,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)

from requester import NewsHead

console = Console()

FETCHING = "[bold cyan]Fetching Headlines, please be patient...[/bold cyan]"


def event_loop():
    news_head = NewsHead()

    console.print("\n[bold cyan]=============================================[/bold cyan]")
    console.print("[bold dark_orange3]What headlines would you like me to fetch???[/bold dark_orange3]")
    console.print("[bold cyan]=============================================[/bold cyan]")

    cmd = "EMPTY"
    while cmd != "x" and cmd:
        cmd = input(
            "\nPlease select from the following: \n\n\r[N]YTimes headlines?\n\
                     \r[W]ashington Post headlines?\n\
                     \rThe [A]tlantic headlines?\n\
                     \r[P]olitico headlines?\n\
                     \r[WSJ]ournal headlines?\n\
                     \r[T]op Headlines\n\
                     \r[S]earch for phrase\n\
                     \rE[x]it\n\
                     \n\rSelect: "
        )
        cmd = cmd.lower().strip()

        if cmd == "n":
            print(FETCHING)
            # headlines, links = news_head.get_nytimes_headlines()
            # news_handler(headlines, links)

        elif cmd == "w":
            console.print(FETCHING)
            headlines, links = news_head.get_washpost_headlines()
            news_handler(headlines, links)

        elif cmd == "a":
            print(FETCHING)
            headlines, links = news_head.get_atlantic_headlines()
            news_handler(headlines, links)

        elif cmd == "wsj":
            print(FETCHING)
            headlines, links = news_head.get_wsj_headlines()
            news_handler(headlines, links)

        elif cmd == "p":
            print(FETCHING)
            headlines, links = news_head.get_politico_headlines()
            news_handler(headlines, links)

        elif cmd == "s":
            try:
                headlines, links = website_getter()
                web_searcher(headlines)
            except TypeError:
                pass

        elif cmd == "t":
            print(FETCHING)
            pol_headlines, pol_links = news_head.get_politico_headlines()
            atl_headlines, atl_links = news_head.get_atlantic_headlines()
            wash_headlines, wash_links = news_head.get_washpost_headlines()
            wsj_headlines, wsj_links = news_head.get_wsj_headlines()
            pol_links = pol_links[:3]
            atl_links = atl_links[:3]
            wash_links = wash_links[:3]
            wsj_links = wsj_links[:3]
            pol_headlines = pol_headlines[:3]
            atl_headlines = atl_headlines[:3]
            wash_headlines = wash_headlines[:3]
            wsj_headlines = wsj_headlines[:3]
            top_list = list(chain(pol_headlines, atl_headlines, wash_headlines, wsj_headlines))
            top_websites = list(chain(pol_links, atl_links, wash_links, wsj_links))

            top_headlines(top_list)
            top_links(top_websites)

        elif cmd != "x" and cmd:
            print(f"\n[bold dark_orange3]Sorry, I do not understand '{cmd}' command...[/bold dark_orange3]")

    print("\n[bold cyan]===========================================[/bold cyan]")
    print("[bold dark_orange3]All done, thanks for using News Header!!!!!![/bold dark_orange3]")
    print("[bold cyan]===========================================[/bold cyan]\n")


def news_handler(headlines, links):
    for i, j in enumerate(headlines, 1):
        print(f"{i}: {j}")
    articles_finder = input("\nDo any of these interest you Y/N?: ")
    articles_finder = articles_finder.lower().strip()

    if articles_finder == "y":
        try:
            article_number = int(input("Please select a number: "))
            webbrowser.open(links[article_number - 1])
        except IndexError as e:
            print(f"Sorry, {e}")
        except ValueError:
            print("Must be an integer...")
    elif articles_finder == "n":
        return
    else:
        print("Sorry, please select [Y] or [N]...")


def website_getter():
    _instance = NewsHead()
    website = input("Please select which website you'd like me to search through: ")
    website = website.lower().strip()
    
    if website == "n":
        print(FETCHING)
        headlines, links = _instance.get_nytimes_headlines()
        return headlines, links
    elif website == "w":
        print(FETCHING)
        headlines, links = _instance.get_washpost_headlines()
        return headlines, links
    elif website == "a":
        print(FETCHING)
        headlines, links = _instance.get_atlantic_headlines()
        return headlines, links
    elif website == "p":
        print(FETCHING)
        headlines, links = _instance.get_politico_headlines()
        return headlines, links
    elif website == "wsj":
        print(FETCHING)
        headlines, links = _instance.get_wsj_headlines()
        return headlines, links
    else:
        print("\n[bold dark_orange3]Sorry, that's not a website I can search. Please select a searchable website...[/bold dark_orange3]\n\r")
    


def top_headlines(top_list):
    for i, headlines in enumerate(top_list, 1):
        if i == 1:
            print("\n[bold cyan]Here are the top 3 Politico headlines: [/bold cyan]")
        elif i == 4:
            print("[bold cyan]Here are the top 3 Atlantic headlines: [/bold cyan]")
        elif i == 7:
            print("[bold cyan]Here are the top 3 Washington Post headlines: [/bold cyan]")
        elif i == 10:
            print("[bold cyan]Here are the top 3 WSJ headlines: [/bold cyan]")
        print(f"{i}: {headlines}")


def top_links(links):
    cmd = input("Do one of these articles interest you [Y]/[N]?  ")
    cmd = cmd.lower().strip()
    if cmd == "y":
        try:
            article = int(input("Please select which article you'd like to visit: "))
            webbrowser.open(links[article - 1])
        except IndexError as e:
            print(f"Error {e}")
        except ValueError:
            print("Must be an integer...")
    elif cmd == "n":
        return
    else:
        print("[/bold cyan]Please select [Y] or [N][/bold cyan]")


def web_searcher(headline):
    search_word = input("What key word would you like me to search for? ")
    search_word = search_word.strip()
    articles = []
    for word in headline:
        if search_word.upper() in word.upper():
            articles.append(word)
    if articles:
        print("[bold cyan]==================================================[/bold cyan]")
        print(f'\nHere is what I found containing "{search_word}": \n')
        for i, article in enumerate(articles, 1):
            print(f"{i}: {article}")
    else:
        print("\nSorry, I could not find any articles related to your search.")


def main():
    event_loop()


if __name__ == "__main__":
    main()
