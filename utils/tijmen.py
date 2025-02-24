import random
import sys
import time

# from pydantic import ValidationError
from external_api.enums import Division
from external_api.scraper import scramble_rikishi, scrape_all, scrape_basho
from external_api.sumo import SumoAPI
from database.queries import DfQueries
from utils.columns import add_winstreaks, count_kimarite, get_wins, top_moves
from utils.estimate import estimate
from utils.parsing import sumo_rank_to_value
import external_api.schemas as schema


def tijmens_tests() -> None:
    ...

    # api = SumoAPI()
    # kim = api.get_kimarite(ascending=False)

    # for idx, i in enumerate(kim.records):
    #     print(f'{idx+1}: "{i.kimarite}",')

    # misc()
    # test_estimator()
    # test_counting()
    # test_rank_value()
    # test_apis()
    # test_scrape_bashos()
    # test_scraper()
    # test_rikishi_scrambler()
    # test_winstreak()
    # test_ratios()
    test_move_count()


def test_move_count():
    df = DfQueries.matches()
    
    # df = df.loc[(df["east_id"] == 3363) | (df["west_id"] == 3363)]
    # df = df.sort_values(["basho_id", "day"], ascending=True)
    # df = df.iloc[0:50]
    df = df.drop(columns=["division", "match_no", "east_rank", "west_rank", "winner_jp", "east_shikona", "west_shikona"])
    print(df)

    print(len(df))
    df = top_moves(df, 1)

    # df = mark_winner(df)
    # df = df.loc[(df["east_id"] == 3363) | (df["west_id"] == 3363)]
    print()
    # print(df.to_string())
    print(df)

    
def test_ratios():
    df = DfQueries.matches()
    
    # bashos = ['199411', '199505', '199507', '199511', '199601', '199605', '199703', '199709',
    #           '199711', '199801', '199803', '199805', '199807', '199809', '199811', '199901',
    #           '199903', '199905', '199907', '199909', '199911', '200001', '200003', '200005',
    #           '200007', '200009', '200011', '200101', '200103', '200105', '200107', '200109',
    #           '200111', '200201', '200203', '200205', '200207', '200209', '200211', '200301',
    #           '200303', '200305', '200307', '200309', '200311', '200401', '200403', '200405',
    #           '200407', '200409', '200411', '200501', '200503', '200505', '200507', '200509',
    #           '200511', '200601', '200603', '200605', '200607', '200609', '200611', '200701',
    #           '200703', '200705', '200707', '200709', '200711', '200801', '200803', '200805',
    #           '200807', '200809', '200811', '200901', '200903', '200905', '200907', '200909',
    #           '200911', '201001', '201003', '201005', '201007', '201009', '201011', '201101',
    #           '201105', '201107', '201109', '201111', '201201', '201203', '201205', '201207',
    #           '201209', '201211', '201301', '201303', '201305', '201307', '201309', '201311',
    #           '201401', '201403', '201405', '201407', '201409', '201411', '201501', '201503',
    #           '201505', '201507', '201509', '201511', '201601', '201603', '201605', '201607',
    #           '201609', '201611', '201701', '201703', '201705', '201707', '201709', '201711',
    #           '201801', '201803', '201805', '201807', '201809', '201811', '201901', '201903',
    #           '201905', '201907', '201909', '201911', '202001', '202003', '202007', '202009',
    #           '202011', '202101', '202103', '202105', '202107', '202109', '202111', '202201',
    #           '202203', '202205', '202207', '202209', '202211', '202301', '202303', '202305',
    #           '202307', '202309', '202311', '202401', '202403', '202405', '202407', '202409',
    #           '202411', '202501']
    
    # allowed = ['201401', '201403', '201405', '201407', '201409', '201411', '201501', '201503',
    #           '201505', '201507', '201509', '201511']

    # df = df.loc[df["basho_id"].isin(allowed)]
    # df = df.iloc[0:100]
    df = df.drop(columns=["division", "match_no", "east_rank", "west_rank", "winner_jp", "kimarite"])
    print(df)

    df = get_wins(df)
    df = df.sort_values(["basho_id", "day"], ascending=True)
    # df = df.loc[(df["east_id"] == 3363) | (df["west_id"] == 3363)]
    print()
    # print(df.to_string())
    print(df)
    

def test_winstreak():
    df = DfQueries.matches()
    
    # bashos = ['199411', '199505', '199507', '199511', '199601', '199605', '199703', '199709',
    #           '199711', '199801', '199803', '199805', '199807', '199809', '199811', '199901',
    #           '199903', '199905', '199907', '199909', '199911', '200001', '200003', '200005',
    #           '200007', '200009', '200011', '200101', '200103', '200105', '200107', '200109',
    #           '200111', '200201', '200203', '200205', '200207', '200209', '200211', '200301',
    #           '200303', '200305', '200307', '200309', '200311', '200401', '200403', '200405',
    #           '200407', '200409', '200411', '200501', '200503', '200505', '200507', '200509',
    #           '200511', '200601', '200603', '200605', '200607', '200609', '200611', '200701',
    #           '200703', '200705', '200707', '200709', '200711', '200801', '200803', '200805',
    #           '200807', '200809', '200811', '200901', '200903', '200905', '200907', '200909',
    #           '200911', '201001', '201003', '201005', '201007', '201009', '201011', '201101',
    #           '201105', '201107', '201109', '201111', '201201', '201203', '201205', '201207',
    #           '201209', '201211', '201301', '201303', '201305', '201307', '201309', '201311',
    #           '201401', '201403', '201405', '201407', '201409', '201411', '201501', '201503',
    #           '201505', '201507', '201509', '201511', '201601', '201603', '201605', '201607',
    #           '201609', '201611', '201701', '201703', '201705', '201707', '201709', '201711',
    #           '201801', '201803', '201805', '201807', '201809', '201811', '201901', '201903',
    #           '201905', '201907', '201909', '201911', '202001', '202003', '202007', '202009',
    #           '202011', '202101', '202103', '202105', '202107', '202109', '202111', '202201',
    #           '202203', '202205', '202207', '202209', '202211', '202301', '202303', '202305',
    #           '202307', '202309', '202311', '202401', '202403', '202405', '202407', '202409',
    #           '202411', '202501']
    
    # allowed = ['201401', '201403', '201405', '201407', '201409', '201411', '201501', '201503',
    #           '201505', '201507', '201509', '201511']

    # df = df.loc[df["basho_id"].isin(allowed)]
    # df = df.iloc[0:100]
    df = df.drop(columns=["division", "match_no", "east_rank", "west_rank", "winner_jp", "kimarite"])
    print(df)

    df = add_winstreaks(df)
    df = df.sort_values(["basho_id", "day"], ascending=True)
    # df = df.loc[(df["east_id"] == 3363) | (df["west_id"] == 3363)]
    print()
    # print(df.to_string())
    print(df)


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

def test_scrape_bashos():
    s = 2010
    e = 2015

    
    for i in estimate(range(s, e), title="Basho's"):
        for j in estimate(range(1, 12, 2), title="Month"):
            basho_id = f"{i}{j:0>{2}}"
            print(basho_id)

            if basho_id == "201103" or basho_id == "202005":
                continue
            
            scrape_basho(basho_id, Division.Makuuchi.value)



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

