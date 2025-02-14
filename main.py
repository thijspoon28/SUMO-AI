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

    # rikishis_stats = api.get_rikishi_stats(218)
    # print(rikishis_stats)

    kimarite = api.get_kimarite()
    # print(kimarite)
    print(sum([i.count for i in kimarite.records]))

    # kimarite_detail = api.get_kimarite_detail('oshidashi', scrape=True)
    # # print(kimarite_detail.records[10])
    # print(kimarite_detail.total)
    # print(len(kimarite_detail.records))


    

if __name__ == "__main__":
    main()
