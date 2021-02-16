from typing import Type
import webbrowser
from itertools import chain
import asyncio
import time
import concurrent.futures

from colorama import init, Fore
from rich.progress import Progress

# from helper.Requester import NewsHead
from helper.AsyncRequester import NewsHead


FETCHING = "\nFetching Headlines, please be patient...\n"

news = NewsHead()
loop = asyncio.get_event_loop()


def event_loop():

    print("\n=============================================")
    print("What headlines would you like me to fetch???")
    print("=============================================")

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
            # headlines, links = news.get_nytimes_headlines()
            # news_handler(headlines, links)

        elif cmd == "w":
            print(FETCHING)
            headlines, links = loop.run_until_complete(news.get_washpost_headlines())
            news_handler(headlines, links)

        elif cmd == "a":
            print(FETCHING)
            headlines, links = loop.run_until_complete(news.get_atlantic_headlines())
            news_handler(headlines, links)

        elif cmd == "wsj":
            print(FETCHING)
            headlines, links = loop.run_until_complete(news.get_wsj_headlines())
            news_handler(headlines, links)

        elif cmd == "p":
            print(FETCHING)
            headlines, links = loop.run_until_complete(news.get_politico_headlines())
            news_handler(headlines, links)

        elif cmd == "s":
            try:
                headlines, links = website_getter()
                web_searcher(headlines)
            except TypeError:
                pass

        elif cmd == "t":
            print(FETCHING)
            try:
                pol, atl, wsj, wash = loop.run_until_complete(async_web_getter())
            except Exception as e:
                pass
            finally:
                loop.close()

            pol_headlines, pol_links = slicer(pol)
            atl_headlines, atl_links = slicer(atl)
            wsj_headlines, wsj_links = slicer(wsj)
            wash_headlines, wash_links = slicer(wash)

            top_list = list(
                chain(pol_headlines, atl_headlines, wash_headlines, wsj_headlines)
            )
            top_websites = list(
                chain(pol_links, atl_links, wash_links, wsj_links)
            )

            top_headlines(top_list)
            top_links(top_websites)

        elif not cmd:
            cmd = " "
            print("\nNo command given! Please select from the available list...")

        elif cmd != "x" and cmd:
            print(
                f"\nSorry, I do not understand '{cmd}' command...[/bold dark_orange3]"
            )

    print("\n===========================================")
    print("All done, thanks for using News Header!!!!!!")
    print("===========================================\n")


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
    website = input("Please select which website you'd like me to search through: ")
    website = website.lower().strip()

    if website == "n":
        print(FETCHING)
        headlines, links = loop.run_until_complete(news.get_nytimes_headlines())
        return headlines, links
    elif website == "w":
        print(FETCHING)
        headlines, links = loop.run_until_complete(news.get_washpost_headlines())
        return headlines, links
    elif website == "a":
        print(FETCHING)
        headlines, links = loop.run_until_complete(news.get_atlantic_headlines())
        return headlines, links
    elif website == "p":
        print(FETCHING)
        headlines, links = loop.run_until_complete(news.get_politico_headlines())
        return headlines, links
    elif website == "wsj":
        print(FETCHING)
        headlines, links = loop.run_until_complete(news.get_wsj_headlines())
        return headlines, links
    else:
        print(
            "\nSorry, that's not a website I can search. Please select a searchable website...\n\r"
        )


def top_headlines(top_list):
    for i, headlines in enumerate(top_list, 1):
        if i == 1:
            print("\nHere are the top 3 Politico headlines: ")
        elif i == 4:
            print("Here are the top 3 Atlantic headlines: ")
        elif i == 7:
            print("Here are the top 3 Washington Post headlines: ")
        elif i == 10:
            print("Here are the top 3 WSJ headlines:")
        print(Fore.CYAN + f"{i}: {headlines}")


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
        print("==================================================")
        print(f'\nHere is what I found containing "{search_word}": \n')
        for i, article in enumerate(articles, 1):
            print(f"{i}: {article}")
    else:
        print("\nSorry, I could not find any articles related to your search.")


async def async_web_getter():
    input_coroutines = [
        news.get_politico_headlines(),
        news.get_atlantic_headlines(),
        news.get_wsj_headlines(),
        news.get_washpost_headlines(),
    ]
    pol, atl, wsj, wash = await asyncio.wait_for(
        asyncio.gather(*input_coroutines, return_exceptions=True), timeout=25
    )
    return pol, atl, wsj, wash


def slicer(results):
    headlines, lists = results[0], results[1]
    headlines, lists = headlines[:3], lists[:3]
    return headlines, lists


def main():
    event_loop()


if __name__ == "__main__":
    main()
