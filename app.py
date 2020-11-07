
import webbrowser
from re import search

from requester import NewsHead

FETCHING = "Fetching Headlines, please be patient..."


def event_loop():
    news_head = NewsHead()

    print("\n==========================================")
    print("What headlines would you like me to fetch???")
    print("==========================================")

    cmd = "EMPTY"
    while cmd != "x" and cmd:
        cmd = input(
            "\nPlease select from the following: \n\n\r[N]YTimes headlines?\n\
                     \r[W]ashington Post headlines?\n\
                     \rThe [A]tlantic headlines?\n\
                     \r[P]olitico headlines?\n\
                     \r[S]earch for phrase\n\
                     \rE[x]it\n\
                     \n\rSelect: "
        )
        cmd = cmd.lower().strip()

        if cmd == "n":
            print(FETCHING)
            headlines, links = news_head.get_nytimes_headlines()
            news_handler(headlines, links)

        elif cmd == "w":
            print(FETCHING)
            headlines, links = news_head.get_washpost_headlines()
            news_handler(headlines, links)

        elif cmd == "a":
            print(FETCHING)
            headlines, links = news_head.get_atlantic_headlines()
            news_handler(headlines, links)

        elif cmd == "p":
            print(FETCHING)
            headlines, links = news_head.get_politico_headlines()
            news_handler(headlines, links)

        elif cmd == "s":
            headlines, links = website_getter()
            web_searcher(headlines)

        elif cmd != "x" and cmd:
            print(f"\nSorry, I do not understand {cmd} command...")

    print("\n===========================================")
    print("All done, thanks for using News Header!!!!!!")
    print("===========================================")


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
    if website == "w":
        print(FETCHING)
        headlines, links = _instance.get_washpost_headlines()
        return headlines, links
    if website == "a":
        print(FETCHING)
        headlines, links = _instance.get_atlantic_headlines()
        return headlines, links
    if website == "p":
        print(FETCHING)
        headlines, links = _instance.get_politico_headlines()
        return headlines, links
    else:
        print("Sorry, that's not a website I can search")


def web_searcher(headline):
    search_word = input("What key word would you like me to search for? ")
    search_word = search_word.strip()
    articles = []
    for word in headline:
        if search_word in word:
            articles.append(word)
    if articles:
        print('==================================================')
        print(f'\nHere is what I found containing "{search_word}": \n')
        for i, article in enumerate(articles, 1):
            print(f'{i}: {article}')
    else:
        print('\nSorry, I could not find any articles related to your search. Please remember they are case sensitive')





def main():
    event_loop()


if __name__ == "__main__":
    main()
