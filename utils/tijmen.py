import random
import time
from database.queries import DfQueries
from utils.columns import count_kimarite
from utils.estimate import estimate
from utils.parsing import sumo_rank_to_value


def tijmens_tests() -> None:
    ...

    test_estimator()
    # test_counting()
    # test_rank_value()


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
    for _ in estimate(range(30), title="Testing"):
        x = random.random()
        print(x)
        time.sleep(x)
