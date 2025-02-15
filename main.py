# import data
from api.sumo import SumoAPI


def main():
    api = SumoAPI()

    # rikishis = api.get_rikishis()
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

    kimarite = api.get_kimarite()
    # print(kimarite)
    print(sum([i.count for i in kimarite.records]))

    # kimarite_detail = api.get_kimarite_detail('oshidashi')
    # print(kimarite_detail.records[999])
    # print(kimarite_detail.total)
    # print(len(kimarite_detail.records))

    # rikishi_matches = api.get_rikishi_matches(218)
    # print(rikishi_matches)

    # basho_banzuke = api.get_basho_banzuke(196011, 'Makuuchi')
    # print(basho_banzuke)

    ### ERROR
    basho_torkikumi = api.get_basho_torikumi(196011, 'Makuuchi', 10)
    print(basho_torkikumi)

    

if __name__ == "__main__":
    main()
