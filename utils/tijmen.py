import random
import sys
import time

# from pydantic import ValidationError
from api.enums import Division
from api.scraper import scramble_rikishi, scrape_all
from api.sumo import SumoAPI
from database.queries import DfQueries
from utils.columns import count_kimarite, rikishi_winstreak
from utils.estimate import estimate
from utils.parsing import next_basho_id, prev_basho_id, sumo_rank_to_value
import api.schemas as schema


def tijmens_tests() -> None:
    ...


    # misc()
    # test_estimator()
    # test_counting()
    # test_rank_value()
    # test_apis()
    # test_scraper()
    # test_rikishi_scrambler()
    test_winstreak()

    
def test_winstreak():
    df2 = DfQueries.matches()
    row = df2.loc[1]
    rikishi_id = row["winner_id"]
    # print(df2)
    rikishi_winstreak(df2, row, rikishi_id)


def test_rikishi_scrambler():
    rikishi_id = 215
    rikishi_id = 5727
    r = scramble_rikishi(rikishi_id, True, True, True)
    
    print(schema.ValidateRikishi.model_validate(r))
    # print(r.shikonaHistory[0])
    # try:
    #     print("oh yes!")
        
    # except ValidationError:
    #     print("oh no!")

    # print(r)
    # print(r.measurementHistory)
    # print(r.rankHistory)
    # print(r.shikonaHistory)


def test_scraper():
    scrape_all()


def misc():
    x = sys.stdout.write
    def write(s) -> None:
        s = "writeCall " + s
        x(s)
    
    y = sys.stdout.flush
    def flush() -> None:
        x("flushCall")
        y()

    sys.stdout.write = write
    sys.stdout.flush = flush
    print("hello!")
    print("hello2!")


def test_apis():
    api = SumoAPI()

    print(api.get_kimarite().records[0].count)
    print(api.get_rikishi(215))
    print(api.get_ranks(215).records[0].id)
    print(api.get_basho_banzuke("202303", Division.Makuuchi).record.east[0].losses)


def test_counting():
    df1 = DfQueries.rikishis()
    df2 = DfQueries.matches()

    df = count_kimarite(df1, df2)
    print(df[["id", "yorikiri_win", "yorikiri_loss"]])


def test_rank_value():
    df = DfQueries.basho_rikishi()

    df = df.drop('day', axis=1)
    df = df.drop('match_no', axis=1)
    df = df.drop('division', axis=1)
    df = df.drop('kimarite', axis=1)
    df = df.drop('east_weight', axis=1)
    df = df.drop('east_height', axis=1)
    df = df.drop('west_weight', axis=1)
    df = df.drop('west_height', axis=1)
    df = df.drop('winner_jp', axis=1)
    df = DfQueries.basho_matches()

    df["east_rank_value"] = df["east_rank"].apply(sumo_rank_to_value)
    df["west_rank_value"] = df["west_rank"].apply(sumo_rank_to_value)

    df = df.loc[df["east_rank_value"] > 9990]
    print(df)


def test_estimator():
    # for _ in estimate(range(30), title="Testing"):
    #     print("hi!")
    #     time.sleep(0.03)

    lim = 35
        
    for j in estimate(range(3), title="Testing 2", disable_terminal_chomp_chomp=False):
        for k in estimate(range(30), title="Testing 3"):
            lim -= 1
            x = random.random()
            print("a", x)
            if lim < 0:
                raise Exception(">:(")
            time.sleep(x)
        for k in estimate(range(10), title="Testing 4"):
            print("b", "\n", "o")
            time.sleep(0.1)

