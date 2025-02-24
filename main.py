import os

from dotenv import load_dotenv

load_dotenv()

from external_api.enums import Division  # noqa: E402
from external_api.scraper import scrape_basho  # noqa: E402
from database.session import init_db  # noqa: E402
from utils.estimate import estimate, manager  # noqa: E402
from utils.tijmen import tijmens_tests  # noqa: E402
from utils.thijs import thijs_tests  # noqa: E402


def main():
    init_db(delete=False)


    if os.getenv("USER") == "TIJMEN":
        tijmens_tests()
        return

    if os.getenv("USER") == "THIJS":
        thijs_tests()
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        manager.handle_exc(exc)
