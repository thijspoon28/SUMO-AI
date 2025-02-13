# import data
from api.sumo import SumoAPI


def main():
    api = SumoAPI()

    print(api.get_rikishis())


if __name__ == "__main__":
    main()
