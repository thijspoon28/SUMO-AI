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
