import sys
import time
from api.enums import Division
from api.sumo import SumoAPI
from database.queries import DfQueries
from utils.columns import count_kimarite
from utils.estimate import estimate
from utils.parsing import sumo_rank_to_value


def tijmens_tests() -> None:
    ...

    # misc()
    test_estimator()
    # test_counting()
    # test_rank_value()
    # test_apis()


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
        
    for j in estimate(range(3), title="Testing 2"):
        for k in estimate(range(30), title="Testing 3", disable_terminal_chomp_chomp=False):
            x = 0.1
            print("a", "")
            time.sleep(x)
        for k in estimate(range(10), title="Testing 4", disable_terminal_chomp_chomp=True):
            print("b", "\n", "o")
            time.sleep(0.1)

