# import data
from api.enums import Division
from api.sumo import SumoAPI


def main():
    api = SumoAPI()

    # rikishis = api.get_rikishis()
    # rikishi_id = rikishis.records[0].id

    # rikishi = api.get_rikishi(rikishi_id)

    basho = api.get_basho_banzuke("202303", Division.Sandanme)

    print(basho)


if __name__ == "__main__":
    main()
