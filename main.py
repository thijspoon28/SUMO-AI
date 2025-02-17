import os

from dotenv import load_dotenv
load_dotenv()

from api.enums import Division  # noqa: E402
from api.scraper import scrape_basho  # noqa: E402
from database.session import init_db  # noqa: E402
from utils.estimate import estimate  # noqa: E402
from utils.tijmen import tijmens_tests  # noqa: E402


def main():
    init_db(delete=False)


    if os.getenv("USER") == "TIJMEN":
        tijmens_tests()
        return


    for i in estimate(range(2010, 2025), title="Basho's"):
        for j in estimate(range(1, 12, 2), title="Month"):
            basho_id = f"{i}{j:0>{2}}"
            print("\n",basho_id)

            if basho_id == "201103" or basho_id == "202005":
                continue
            
            scrape_basho(basho_id, Division.Makuuchi.value)


if __name__ == "__main__":
    main()
