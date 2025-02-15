# import data
from api.enums import Division
from api.scraper import scrape_basho
from api.sumo import SumoAPI
from database.session import init_db


def main():
    # init_db(delete=True)
    # scrape_basho("196001", Division.Makuuchi.value)

    for i in range(1958, 2025):
        for j in range(1, 12, 2):
            basho_id = f"{i}{j:0>{2}}"
            print(basho_id)
    

if __name__ == "__main__":
    main()
