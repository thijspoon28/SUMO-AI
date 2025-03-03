from utils import columns
from utils.queries import DfQueries


df_matches = DfQueries().matches()


df_matches = columns.fightertype(df_matches)
print(df_matches)
print(df_matches.columns)