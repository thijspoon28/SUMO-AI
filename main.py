# import data
from api.enums import Division
from api.scraper import scrape_basho
from api.sumo import SumoAPI
from database.session import init_db


def main():
    init_db(delete=True)
    for i in range(2010, 2025):
            for j in range(1, 12, 2):
                basho_id = f"{i}{j:0>{2}}"
                print(basho_id)
                if basho_id == 201103 or basho_id == 202007:
                    continue
                scrape_basho(basho_id, Division.Makuuchi.value)


    # api = SumoAPI()

    # rikishis = api.get_rikishis(scrape=True)
    # print(len(rikishis.records))
    # active_Rikishi = []
    # for i in rikishis.records:
    #     active_Rikishi.append(i.shikonaEn)
    # print(active_Rikishi)

    # rikishi_id = rikishis.records[0].id

    # print(rikishi_id)

    # rikishi = api.get_rikishi(218)
    # print(rikishi)

    # rikishis_stats = api.get_rikishi_stats(218)
    # print(rikishis_stats)

    # kimarite = api.get_kimarite()
    # # print(kimarite)
    # print(kimarite)
    # print(sum([i.count for i in kimarite.records]))

    # kimarite_detail = api.get_kimarite_detail('oshidashi')
    # print(kimarite_detail.records[999])
    # print(kimarite_detail.total)
    # print(len(kimarite_detail.records))

    # rikishi_matches = api.get_rikishi_matches(218)
    # print(rikishi_matches)
    # basho = api.get_basho(196011)
    # print(basho.specialPrizes)
    # print(basho.yusho)
    # print()

    # basho_banzuke = api.get_basho_banzuke(196011, 'Makuuchi')
    # print(basho_banzuke)

    # a = api.get_ranks(216)
    # print(len(a))
    
    # b = api.get_measurements(216)
    # print(len(b))

    # c = api.get_shikonas(216)
    # print(len(c))

    # x = api.get_rikishi(2, ranks=True)
    # print(len(x.rankHistory))

    # x = api.get_ranks(2)
    # print(len(x))

    ### ERROR
    # basho_torkikumi = api.get_basho_torikumi(196011, 'Makuuchi', 10)
    # print(basho_torkikumi)
    #ranking / results of the bashi
    # basho_banzuke = api.get_basho_banzuke(201111, 'Makuuchi')
    # print(basho_banzuke)
    
    # matches on a given day
    # basho_torkikumi = api.get_basho_torikumi(196011, 'Makuuchi', 10)
    # print(basho_torkikumi)

    # basho = api.get_basho(199011)
    # print(basho.specialPrizes)

    

if __name__ == "__main__":
    main()
