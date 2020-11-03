
import webbrowser

from requester import NewsHead

FETCHING = "Fetching HEADlines, please be patient..."

def event_loop():
    news_head = NewsHead()

    print("\n==========")
    print("What headlines would you like me to fetch???")
    print("==========\n")

    cmd = "EMPTY"
    while cmd != "x" and cmd:
        cmd = input(
            "Please select from the following: \n\r[N]YTimes headlines?\n\
                     \n\r[W]ashington Post headlines?\n\
                     \n\rThe [A]tlantic headlines?\n\
                     \n\r[P]olitico headlines?\n\
                     \n\rE[x]it\n"
        )
        cmd = cmd.lower().strip()

        if cmd == "n":
            print(FETCHING)
            headlines, links = news_head.get_nytimes_headlines()
            news_handler(headlines, links)

        if cmd == "w":
            print(FETCHING)
            headlines, links = news_head.get_washpost_headlines()
            news_handler(headlines, links)

        if cmd == "a":
            print(FETCHING)
            headlines, links = news_head.get_atlantic_headlines()
            news_handler(headlines, links)

        if cmd == "p":
            print(FETCHING)
            headlines, links = news_head.get_politico_headlines()
            news_handler(headlines, links)
            
    print('\n===========================================')
    print("All done, thanks for using News Header!!!!!!")
    print('===========================================')

def news_handler(headlines, links):
    for i, j in enumerate(headlines, 1):
        print(f"{i}: {j}")
    articles_finder = input("Do any of these interest you Y/N?: ")
    articles_finder = articles_finder.lower().strip()
    if articles_finder == "y":
        article_number = int(input("Please select number: "))
        webbrowser.open(links[article_number - 1])
    elif articles_finder == "n":
        return
    else:
        print("Sorry, please select [Y] or [N]...")



def main():
    event_loop()


if __name__ == "__main__":
    main()

