import pandas as pd


def count_kimarite(df_rikishi: pd.DataFrame, df_matches: pd.DataFrame) -> pd.DataFrame:
    """Returns a rikishi dataframe with move counts (kimarite win/loss)."""

    # Extract unique rikishi IDs
    df = df_rikishi[["id"]].copy()

    # Prepare winners data
    winners = df_matches.groupby(["winner_id", "kimarite"]).size().unstack(fill_value=0)
    winners.columns = [f"{kimarite}_win" for kimarite in winners.columns]
    winners.reset_index(inplace=True)

    # Prepare losers data
    df_matches["loser_id"] = df_matches.apply(
        lambda row: (
            row["east_id"] if row["winner_id"] == row["west_id"] else row["west_id"]
        ),
        axis=1,
    )
    losers = df_matches.groupby(["loser_id", "kimarite"]).size().unstack(fill_value=0)
    losers.columns = [f"{kimarite}_loss" for kimarite in losers.columns]
    losers.reset_index(inplace=True)

    # Merge winners and losers with rikishi DataFrame
    df = df.merge(winners, left_on="id", right_on="winner_id", how="left").drop(
        columns=["winner_id"]
    )
    df = df.merge(losers, left_on="id", right_on="loser_id", how="left").drop(
        columns=["loser_id"]
    )

    # Fill NaN values with 0 (for rikishi with no matches)
    df.fillna(0, inplace=True)

    return df


def count_moves(df_matches: pd.DataFrame) -> pd.DataFrame:
    win_moves: dict[int, dict[str, int]] = {}
    loss_moves: dict[int, dict[str, int]] = {}

    for _, match in df_matches.iterrows():
        east = match["east_id"]
        west = match["west_id"]
        east_win = match["winner_id"] == east
        kimarite = match["kimarite"]
        
        winner, loser = (east, west) if east_win else (west, east)

        win_moves.setdefault(winner, {}).setdefault(kimarite, 0)
        win_moves[winner][kimarite] += 1

        loss_moves.setdefault(loser, {}).setdefault(kimarite, 0)
        loss_moves[loser][kimarite] += 1

    # Transform into a structured format for the DataFrame
    data = []
    unique_ids = set(win_moves.keys()).union(set(loss_moves.keys()))
    all_kimarites: set[str] = set()

    for rikishi_id in unique_ids:
        all_kimarites = all_kimarites.union(set(win_moves.get(rikishi_id, {}).keys())).union(set(loss_moves.get(rikishi_id, {}).keys()))
        
    for rikishi_id in unique_ids:
        for kimarite in all_kimarites:
            wins = win_moves.get(rikishi_id, {}).get(kimarite, 0)
            losses = loss_moves.get(rikishi_id, {}).get(kimarite, 0)
            data.append({"Rikishi_ID": rikishi_id, "Move_Type": kimarite, "Win_Count": wins, "Loss_Count": losses})

    return pd.DataFrame(data)
