import pandas as pd
# from api.enums import Division
# from api.scraper import estimate_iterable, scrape_basho

from database.queries import DfQueries
from database.session import init_db
from utils.parsing import sumo_rank_to_value


def main():
    init_db(delete=False)

    df = DfQueries.basho_matches()
    df = df.drop('day', axis=1)
    df = df.drop('match_no', axis=1)
    df = df.drop('division', axis=1)
    df = df.drop('kimarite', axis=1)
    df = df.drop('east_weight', axis=1)
    df = df.drop('east_height', axis=1)
    df = df.drop('west_weight', axis=1)
    df = df.drop('west_height', axis=1)
    df = df.drop('winner_jp', axis=1)

    df["east_rank_value"] = df["east_rank"].apply(sumo_rank_to_value)
    df["west_rank_value"] = df["west_rank"].apply(sumo_rank_to_value)

    # df = df.loc[df["east_rank_value"] > 9990]

    print(df)
    # print(df.to_string())


    # for i in estimate_iterable(range(2010, 2025), prefix="<===>"):
    #     for j in range(1, 12, 2):
    #         basho_id = f"{i}{j:0>{2}}"
    #         print(basho_id)
    #         if basho_id == "201103" or basho_id == "202005":
    #             continue
    #         scrape_basho(basho_id, Division.Makuuchi.value)


if __name__ == "__main__":
    main()
