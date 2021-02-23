from itertools import chain
import asyncio

from colorama import init, Fore

from getters.AsyncRequester import NewsHead
from lib.helpers import (
    news_handler,
    website_getter,
    top_headlines,
    top_links,
    web_searcher,
    async_web_getter,
    slicer,
)

init()

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
            print(
                "\nWorking on getting NYTimes feature to properly function... Please utilize one of the other websites!"
            )
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
            top_websites = list(chain(pol_links, atl_links, wash_links, wsj_links))

            top_headlines(top_list)
            top_links(top_websites)

        elif not cmd:
            cmd = " "
            print("\nNo command given! Please select from the available list...")

        elif cmd != "x" and cmd:
            print(f"\nSorry, I do not understand '{cmd}' command...")

    print("\n===========================================")
    print("All done, thanks for using News Header!!!!!!")
    print("===========================================\n")


def main():
    event_loop()


if __name__ == "__main__":
    main()
