import webbrowser
import asyncio

from colorama import init, Fore

from getters.AsyncRequester import NewsHead

init()
news = NewsHead()
loop = asyncio.get_event_loop()


FETCHING = "\nFetching Headlines, please be patient...\n"

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
        print("Please select [Y] or [N]")


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