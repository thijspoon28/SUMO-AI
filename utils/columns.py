import pandas as pd  # type: ignore


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

# i dono, df2 was de matches table en jij ben vage redirects aan doen

def rikishi_wins_this_basho(basho_id, day, rikishi):
    df = df2.loc[df2['basho_id'] == basho_id]
    df = df.loc[df['day'] < day]
    return len(df[df['winner_id'] == rikishi])


def rikishi_wins_last_2_years(basho_id, day, rikishi):
    basho_id = int(basho_id)
    basho_id_range = [str(i) for i in range(basho_id, basho_id - 12, -1)]
    # print(basho_id_range)
    df = df2.loc[df2['basho_id'].isin(basho_id_range)]
    return len(df[df['winner_id'] == rikishi])


def ratio_to_opponent(P1, P2):
    df = df2.loc[((df2['east_rikishi_id'] == P1) & (df2['west_rikishi_id'] == P2)) |
             ((df2['east_rikishi_id'] == P2) & (df2['west_rikishi_id'] == P1))]
    # print(len(df))
    return len(df.loc[df['winner_id'] == P1]), len(df.loc[df['winner_id'] == P2])

def winstreak(basho_id, day, rikishi):
    df = df2.loc[((df2['east_rikishi_id'] == rikishi) | (df2['east_rikishi_id'] == rikishi))]
    df_sorted = df.sort_values(by=['basho_id', 'day'], ascending=[False, False])
    current_row_index = df_sorted[(df_sorted['basho_id'] == basho_id) & (df_sorted['day'] == day)].index[0]
    df_filtered = df_sorted.loc[current_row_index:]
    wins = 0
    for index, i in enumerate(df_filtered['winner_id']):
        if i == rikishi:
            wins += 1
        if i != rikishi:
            return wins
        


if __name__ == "__main__":
    count = 0

    for index, i in enumerate(df2['match_no']):
        print(df2.loc[df2.index[index], 'basho_id'], df2.loc[df2.index[index], 'day'], df2.loc[df2.index[index], 'match_no'])
        print(df2.loc[df2.index[index], 'east_rikishi_id'], df2.loc[df2.index[index], 'east_shikona'])
        print(df2.loc[df2.index[index], 'west_rikishi_id'], df2.loc[df2.index[index], 'west_shikona'])
        print("rikishi wins this basho", rikishi_wins_this_basho(df2.loc[df2.index[index], 'basho_id'], df2.loc[df2.index[index], 'day'], df2.loc[df2.index[index], 'east_rikishi_id']))
        print("rikishi wins last 2 years", rikishi_wins_last_2_years(df2.loc[df2.index[index], 'basho_id'], df2.loc[df2.index[index], 'day'], df2.loc[df2.index[index], 'east_rikishi_id']))
        print("ratio to opponent", ratio_to_opponent(df2.loc[df2.index[index], 'east_rikishi_id'], df2.loc[df2.index[index], 'west_rikishi_id']))
        print("winstreak", winstreak(df2.loc[df2.index[index], 'basho_id'], df2.loc[df2.index[index], 'day'], df2.loc[df2.index[index], 'east_rikishi_id']))
        count += 1
        if count > 10:
            break
