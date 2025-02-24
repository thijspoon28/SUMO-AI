


from database.queries import DfQueries
from core.helpers.utils.columns import count_kimarite


def thijs_tests() -> None:
    df_rikishi = DfQueries.rikishis()
    df_matches = DfQueries.matches()


    print(count_kimarite(df_rikishi, df_matches))
