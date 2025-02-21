import pandas as pd

from utils.estimate import estimate
from utils.parsing import prev_basho_date  # type: ignore


def count_kimarite(df_rikishi: pd.DataFrame, df_matches: pd.DataFrame) -> pd.DataFrame:
    """Returns a rikishi dataframe with move counts (kimarite win/loss)."""

    # Extract unique rikishi IDs
    df = df_rikishi[["id"]].copy()

    # Prepare winners data
    winners = df_matches.groupby(["winner_id", "kimarite"]).size().unstack(fill_value=0)
    winners.columns = [f"{kimarite}_win" for kimarite in winners.columns]
    winners.reset_index(inplace=True)

    # Prepare losers data
    df_matches["loser_id"] = df_matches.apply(lambda row: row["east_id"] if row["winner_id"] == row["west_id"] else row["west_id"], axis=1)
    losers = df_matches.groupby(["loser_id", "kimarite"]).size().unstack(fill_value=0)
    losers.columns = [f"{kimarite}_loss" for kimarite in losers.columns]
    losers.reset_index(inplace=True)

    # Merge winners and losers with rikishi DataFrame
    df = df.merge(winners, left_on="id", right_on="winner_id", how="left").drop(columns=["winner_id"])
    df = df.merge(losers, left_on="id", right_on="loser_id", how="left").drop(columns=["loser_id"])

    # Fill NaN values with 0 (for rikishi with no matches)
    df.fillna(0, inplace=True)

    return df


def add_winstreaks(df_matches: pd.DataFrame) -> pd.DataFrame:
    df_matches = df_matches.copy()  # Avoid modifying the original DataFrame

    east_streaks = []
    west_streaks = []

    for _, match in estimate(df_matches.iterrows(), title="Winstreak"):
        east_winstreak = rikishi_winstreak(df_matches, match, match["east_id"])
        west_winstreak = rikishi_winstreak(df_matches, match, match["west_id"])

        east_streaks.append(east_winstreak)
        west_streaks.append(west_winstreak)

    df_matches["east_winstreak"] = east_streaks
    df_matches["west_winstreak"] = west_streaks

    return df_matches


def rikishi_winstreak(df_matches: pd.DataFrame, match_row: pd.Series, rikishi_id: int) -> pd.DataFrame:
    date = match_row["basho_id"], match_row["day"]
    date = prev_basho_date(date)

    won_matches = df_matches.loc[df_matches["winner_id"] == rikishi_id]
    next_match = won_matches.loc[(won_matches["basho_id"] == date[0]) & (won_matches["day"] == date[1])]

    streak = 0

    while not next_match.empty and next_match["winner_id"].iloc[0] == rikishi_id:
        streak += 1

        date = prev_basho_date(date)
        next_match = won_matches.loc[(won_matches["basho_id"] == date[0]) & (won_matches["day"] == date[1])]
    
    return streak


def rikishi_stats(df_matches: pd.DataFrame) -> pd.DataFrame:

    def rikishi_wins_this_basho(basho_id, day, rikishi):
        df = df_matches.loc[df_matches['basho_id'] == basho_id]
        df = df.loc[df['day'] < day]
        return len(df[df['winner_id'] == rikishi])

    def rikishi_wins_last_2_years(basho_id, day, rikishi):
        basho_id = int(basho_id)
        basho_id_range = [str(i) for i in range(basho_id, basho_id - 12, -1)]
        # print(basho_id_range)
        df = df_matches.loc[df_matches['basho_id'].isin(basho_id_range)]
        return len(df[df['winner_id'] == rikishi])

    def ratio_to_opponent(P1, P2):
        df = df_matches.loc[((df_matches['east_rikishi_id'] == P1) & (df_matches['west_rikishi_id'] == P2)) |
                ((df_matches['east_rikishi_id'] == P2) & (df_matches['west_rikishi_id'] == P1))]
        # print(len(df))
        a = len(df.loc[df['winner_id'] == P1])
        b = len(df.loc[df['winner_id'] == P2])
        return a / (a + b)

    def winstreak(basho_id, day, rikishi):
        df = df_matches.loc[((df_matches['east_rikishi_id'] == rikishi) | (df_matches['east_rikishi_id'] == rikishi))]
        df_sorted = df.sort_values(by=['basho_id', 'day'], ascending=[False, False])
        current_row_index = df_sorted[(df_sorted['basho_id'] == basho_id) & (df_sorted['day'] == day)].index[0]
        df_filtered = df_sorted.loc[current_row_index:]
        wins = 0
        for index, i in enumerate(df_filtered['winner_id']):
            if i == rikishi:
                wins += 1
            if i != rikishi:
                return wins
            

    count = 0
    ass = {'basho_id':[], 'rikishi_wins_this_basho':[], 'rikishi_wins_last_2_years':[], 'ratio_to_opponent':[], 'winstreak':[]}
    df_out = pd.DataFrame(ass)

    for index, i in enumerate(df_matches['match_no']):
        # print(df_matches.loc[df_matches.index[index], 'basho_id'], df_matches.loc[df_matches.index[index], 'day'], df_matches.loc[df_matches.index[index], 'match_no'])
        # print(df_matches.loc[df_matches.index[index], 'east_rikishi_id'], df_matches.loc[df_matches.index[index], 'east_shikona'])
        # print(df_matches.loc[df_matches.index[index], 'west_rikishi_id'], df_matches.loc[df_matches.index[index], 'west_shikona'])
        e = df_matches.loc[df_matches.index[index], 'basho_id']
        a = rikishi_wins_this_basho(df_matches.loc[df_matches.index[index], 'basho_id'], df_matches.loc[df_matches.index[index], 'day'], df_matches.loc[df_matches.index[index], 'east_rikishi_id'])
        b = rikishi_wins_last_2_years(df_matches.loc[df_matches.index[index], 'basho_id'], df_matches.loc[df_matches.index[index], 'day'], df_matches.loc[df_matches.index[index], 'east_rikishi_id'])
        c = ratio_to_opponent(df_matches.loc[df_matches.index[index], 'east_rikishi_id'], df_matches.loc[df_matches.index[index], 'west_rikishi_id'])
        d = winstreak(df_matches.loc[df_matches.index[index], 'basho_id'], df_matches.loc[df_matches.index[index], 'day'], df_matches.loc[df_matches.index[index], 'east_rikishi_id'])
        
        
        df_out.loc[len(df_out.index)] = [e, a, b, c, d]
        count += 1
        if count > 10:
            break
    return df_out 
