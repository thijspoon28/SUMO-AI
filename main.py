# import data
from api.sumo import SumoAPI


def main():
    api = SumoAPI()

    rikishis = api.get_rikishis()
    rikishi_id = rikishis.records[0].id

    print(rikishi_id)


if __name__ == "__main__":
    main()
