# import data
from api.enums import Division
from api.scraper import estimate_iterable, scrape_basho

# from api.sumo import SumoAPI
from database.queries import DfQueries
from database.session import init_db


def main():
    init_db(delete=False)

    df = DfQueries.basho_rikishi()
    # print(df.loc[df["special_prize"].notna()])
    print(df)

    # for i in estimate_iterable(range(2010, 2025), prefix="<===>"):
    #     for j in range(1, 12, 2):
    #         basho_id = f"{i}{j:0>{2}}"
    #         print(basho_id)
    #         if basho_id == "201103" or basho_id == "202005":
    #             continue
    #         scrape_basho(basho_id, Division.Makuuchi.value)


if __name__ == "__main__":
    main()
