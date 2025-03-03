import numpy as np
import pandas as pd  # type: ignore
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from utils import processing
from utils.queries import get_session
from utils.models import Rikishi
from external_api.scraper import scramble_rikishi
from utils.estimate import estimate
from utils.parsing import kimarite_to_value


def add_winstreaks(df_matches: pd.DataFrame) -> pd.DataFrame:
    df_matches = df_matches.sort_values(
        ["basho_id", "day"], ascending=True
    ).reset_index(drop=True)

    east_streaks = np.zeros(len(df_matches), dtype=int)
    west_streaks = np.zeros(len(df_matches), dtype=int)

    winners: dict[int, int] = {}

    for idx, match in estimate(df_matches.iterrows(), length=len(df_matches)):
        east = match["east_id"]
        west = match["west_id"]

        east_ws = winners.get(east, 0)
        west_ws = winners.get(west, 0)

        east_streaks[idx] = east_ws
        west_streaks[idx] = west_ws

        winner_id = match["winner_id"]

        if winner_id == east:
            winners[east] = east_ws + 1
            winners[west] = 0
        else:
            winners[west] = west_ws + 1
            winners[east] = 0

    df_matches["east_winstreak"] = east_streaks
    df_matches["west_winstreak"] = west_streaks

    return df_matches


def ratio_to_opponent(df_matches: pd.DataFrame):
    df_matches = df_matches.sort_values(
        ["basho_id", "day"], ascending=True
    ).reset_index(drop=True)

    east_ratios = np.zeros(len(df_matches), dtype=float)
    west_ratios = np.zeros(len(df_matches), dtype=float)

    matches: dict[int, dict[int, int]] = {}

    for idx, match in estimate(df_matches.iterrows(), length=len(df_matches)):
        east = match["east_id"]
        west = match["west_id"]

        if matches.get(east) is None:
            matches[east] = {}
        if matches.get(west) is None:
            matches[west] = {}

        east_m = matches[east].get(west, 0)
        west_m = matches[west].get(east, 0)

        if match["winner_id"] == east:
            matches[east][west] = east_m + 1
        else:
            matches[west][east] = west_m + 1

        t = east_m + west_m
        east_ratios[idx] = east_m / t if t > 0 else 0.5
        west_ratios[idx] = west_m / t if t > 0 else 0.5

    df_matches["east_ratio"] = east_ratios
    df_matches["west_ratio"] = west_ratios

    return df_matches


def get_wins(df_matches: pd.DataFrame) -> pd.DataFrame:
    df_matches = df_matches.sort_values(
        ["basho_id", "day"], ascending=True
    ).reset_index(drop=True)

    east_wins = np.zeros(len(df_matches), dtype=int)
    west_wins = np.zeros(len(df_matches), dtype=int)

    wins: dict[int, int] = {}

    for idx, match in estimate(df_matches.iterrows(), length=len(df_matches)):
        east = match["east_id"]
        west = match["west_id"]

        east_w = wins.get(east, 0)
        west_w = wins.get(west, 0)

        if match["winner_id"] == east:
            wins[east] = east_w + 1
        else:
            wins[west] = west_w + 1

        east_wins[idx] = east_w
        west_wins[idx] = west_w

    df_matches["east_wins"] = east_wins
    df_matches["west_wins"] = west_wins

    return df_matches


def mark_winner(df_matches: pd.DataFrame) -> pd.DataFrame:
    # df_matches["winner"] = (df_matches["winner_id"] == df_matches["east_id"]).astype(int) - (df_matches["winner_id"] == df_matches["west_id"]).astype(int)
    df_matches["east_win"] = (df_matches["winner_id"] == df_matches["east_id"]).astype(int)
    return df_matches


def top_moves(df_matches: pd.DataFrame, top_amount: int) -> pd.DataFrame:
    def get_top_moves(
        data: dict[int, dict[str, dict[str, int]]],
        rikishi_id: int,
        sort_by="w",
    ):
        if rikishi_id not in data:
            return []

        moves = data[rikishi_id]
        sorted_moves = sorted(
            moves.keys(), key=lambda move: moves[move][sort_by], reverse=True
        )

        return sorted_moves

    df_matches = df_matches.sort_values(
        ["basho_id", "day"], ascending=True
    ).reset_index(drop=True)

    stats = {
        "east": {
            "wins": [
                {
                    "move": np.zeros(len(df_matches), dtype=int),
                    "percent": np.zeros(len(df_matches), dtype=float),
                }
                for _ in range(top_amount)
            ],
            "losses": [
                {
                    "move": np.zeros(len(df_matches), dtype=int),
                    "percent": np.zeros(len(df_matches), dtype=float),
                }
                for _ in range(top_amount)
            ],
        },
        "west": {
            "wins": [
                {
                    "move": np.zeros(len(df_matches), dtype=int),
                    "percent": np.zeros(len(df_matches), dtype=float),
                }
                for _ in range(top_amount)
            ],
            "losses": [
                {
                    "move": np.zeros(len(df_matches), dtype=int),
                    "percent": np.zeros(len(df_matches), dtype=float),
                }
                for _ in range(top_amount)
            ],
        },
    }

    wins: dict[int, int] = {}
    losses: dict[int, int] = {}
    moves: dict[int, dict[str, dict[str, int]]] = {}

    for idx, match in estimate(df_matches.iterrows(), length=len(df_matches)):
        east = match["east_id"]
        west = match["west_id"]
        kim = match["kimarite"]

        east_w = wins.setdefault(east, 0)
        east_l = wins.setdefault(east, 0)
        west_w = wins.setdefault(west, 0)
        west_l = wins.setdefault(west, 0)

        east_m = moves.setdefault(east, {}).setdefault(kim, {"w": 0, "l": 0})
        west_m = moves.setdefault(west, {}).setdefault(kim, {"w": 0, "l": 0})

        east_w_top = get_top_moves(moves, east, "w")
        east_l_top = get_top_moves(moves, east, "l")
        west_w_top = get_top_moves(moves, west, "w")
        west_l_top = get_top_moves(moves, west, "l")

        for i in range(top_amount):
            if len(east_w_top) > i:
                percent = moves[east][east_w_top[i]]["w"] / wins[east] if wins[east] > 0 else 1.0
                stats["east"]["wins"][i]["move"][idx] = kimarite_to_value(east_w_top[i])
                stats["east"]["wins"][i]["percent"][idx] = percent

            if len(east_l_top) > i:
                percent = moves[east][east_l_top[i]]["l"] / wins[east] if wins[east] > 0 else 1.0
                stats["east"]["losses"][i]["move"][idx] = kimarite_to_value(east_l_top[i])
                stats["east"]["losses"][i]["percent"][idx] = percent

            if len(west_w_top) > i:
                percent = moves[west][west_w_top[i]]["w"] / wins[west] if wins[west] > 0 else 1.0
                stats["west"]["wins"][i]["move"][idx] = kimarite_to_value(west_w_top[i])
                stats["west"]["wins"][i]["percent"][idx] = percent

            if len(west_l_top) > i:
                percent = moves[west][west_l_top[i]]["l"] / wins[west] if wins[west] > 0 else 1.0
                stats["west"]["losses"][i]["move"][idx] = kimarite_to_value(west_l_top[i])
                stats["west"]["losses"][i]["percent"][idx] = percent

        if match["winner_id"] == east:
            wins[east] = east_w + 1
            losses[west] = west_l + 1

            east_m["w"] += 1
            moves[east][kim] = east_m

            west_m["l"] += 1
            moves[west][kim] = west_m

        else:
            wins[west] = west_w + 1
            losses[east] = east_l + 1

            east_m["l"] += 1
            moves[east][kim] = east_m

            west_m["w"] += 1
            moves[west][kim] = west_m

    for i in range(top_amount):
        east_n_win_move = f"east_n{i+1}_win_move"
        east_n_win_perc = f"east_n{i+1}_win_percent"
        df_matches[east_n_win_move] = stats["east"]["wins"][i]["move"]
        df_matches[east_n_win_perc] = stats["east"]["wins"][i]["percent"]

        east_n_loss_move = f"east_n{i+1}_loss_move"
        east_n_loss_perc = f"east_n{i+1}_loss_percent"
        df_matches[east_n_loss_move] = stats["east"]["losses"][i]["move"]
        df_matches[east_n_loss_perc] = stats["east"]["losses"][i]["percent"]

        west_n_win_move = f"west_n{i+1}_win_move"
        west_n_win_perc = f"west_n{i+1}_win_percent"
        df_matches[west_n_win_move] = stats["west"]["wins"][i]["move"]
        df_matches[west_n_win_perc] = stats["west"]["wins"][i]["percent"]

        west_n_loss_move = f"west_n{i+1}_loss_move"
        west_n_loss_perc = f"west_n{i+1}_loss_percent"
        df_matches[west_n_loss_move] = stats["west"]["losses"][i]["move"]
        df_matches[west_n_loss_perc] = stats["west"]["losses"][i]["percent"]


    return df_matches


def rikishi_stats(df_matches: pd.DataFrame, fix_missing: bool = False) -> pd.DataFrame:
    session = get_session()
    rikishi_lookup = {rikishi.id: rikishi for rikishi in session.query(Rikishi).all()}

    df_matches = df_matches.copy()

    east_weights = np.zeros(len(df_matches), dtype=int)
    east_heights = np.zeros(len(df_matches), dtype=int)
    west_weights = np.zeros(len(df_matches), dtype=int)
    west_heights = np.zeros(len(df_matches), dtype=int)

    for idx, match in estimate(df_matches.iterrows(), length=len(df_matches)):
        east = match["east_id"]
        west = match["west_id"]

        try:
            r_east = rikishi_lookup[east]
            
        except KeyError:
            if fix_missing:
                r_east = scramble_rikishi(east)
                session.add(r_east)
                rikishi_lookup[east] = r_east
                print(f"Rikishi '{east}' is being added.")
                session.commit()

            else:
                east_weights[idx] = None
                east_heights[idx] = None

        else:
            east_weights[idx] = r_east.weight
            east_heights[idx] = r_east.height
            
        try:
            r_west = rikishi_lookup[west]

        except KeyError:
            if fix_missing:
                print(f"Rikishi '{west}' is being added.")
                r_west = scramble_rikishi(west)
                session.add(r_west)
                rikishi_lookup[west] = r_west
                session.commit()

            else:
                west_weights[idx] = None
                west_heights[idx] = None

        else:
            west_weights[idx] = r_west.weight
            west_heights[idx] = r_west.height

    df_matches["east_weight"] = east_weights
    df_matches["east_height"] = east_heights
    df_matches["west_weight"] = west_weights
    df_matches["west_height"] = west_heights

    return df_matches


def fightertype(df_matches: pd.DataFrame) -> pd.DataFrame:
    df = processing.count_moves(df_matches)

    # Pivot the data to get a wide format with separate columns for Wins and Losses for each move
    pivot_wins = df.pivot_table(index='Rikishi_ID', columns='Move_Type', values='Win_Count', aggfunc='sum', fill_value=0)
    pivot_losses = df.pivot_table(index='Rikishi_ID', columns='Move_Type', values='Loss_Count', aggfunc='sum', fill_value=0)

    # Rename the columns to include 'Wins' and 'Losses' for clarity
    pivot_wins.columns = [f'{col}_Wins' for col in pivot_wins.columns]
    pivot_losses.columns = [f'{col}_Losses' for col in pivot_losses.columns]

    # Combine the wins and losses data
    final_df = pd.concat([pivot_wins, pivot_losses], axis=1)

    # Reset the index to make 'Rikishi_ID' a regular column
    final_df.reset_index(inplace=True)

    # change back
    df = final_df


    # Normalize the data
    scaler = StandardScaler()
    X = df.drop(columns=['Rikishi_ID'])
    X_scaled = scaler.fit_transform(X)


    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=4, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # Function to assign a fighter type to each rikishi based on their win counts and cluster-wise win averages
    def assign_fighter_type(cluster_row, cluster_avg_wins):
        # Select only columns related to win counts (excluding 'Rikishi_ID' and 'Cluster')
        win_columns = [col for col in cluster_row.index if 'Wins' in col]

        # Find the move with the highest win count for this individual rikishi
        max_move = cluster_row[win_columns].idxmax()

        # Compare the rikishi's highest move win count to the cluster's average win count
        if cluster_row[max_move] > cluster_avg_wins[max_move]:
            return f'{max_move.split("_")[0]} Specialist'  # Extract the move name (e.g., 'Oshidashi', 'Shiko')
        else:
            return 'Balanced Fighter'

    # Function to classify all rikishi within each cluster
    def classify_rikishi_by_cluster(final_df):
        # Create a new column 'Fighter_Type' to store the fighter type for each rikishi
        final_df['Fighter_Type'] = None

        # Loop through each cluster
        for cluster in final_df['Cluster'].unique():
            # Subset the data for the current cluster
            cluster_data = final_df[final_df['Cluster'] == cluster]

            # Calculate the average win counts for each move in this cluster
            cluster_avg_wins = cluster_data[[col for col in cluster_data.columns if 'Wins' in col]].mean()

            # Apply the fighter type classification to each rikishi in this cluster
            for idx, row in cluster_data.iterrows():
                final_df.loc[idx, 'Fighter_Type'] = assign_fighter_type(row, cluster_avg_wins)

        return final_df

    # Apply the function to classify all rikishi in final_df based on their clusters
    final_df = classify_rikishi_by_cluster(final_df)

    # Display the final DataFrame with fighter types
    print(final_df[['Rikishi_ID', 'Cluster', 'Fighter_Type']])

    # Count how many rikishi are in each cluster
    cluster_counts = final_df['Cluster'].value_counts().reset_index(name='Rikishi_Count')

    # Rename the columns for clarity
    cluster_counts.columns = ['Cluster', 'Rikishi_Count']

    # Assuming 'df_matches' contains a 'Rikishi_ID' column
    # And 'final_df' contains 'Rikishi_ID' and 'Cluster'

    # First, get all the column names from df except the Rikishi_ID
    data_cols = [col for col in final_df.columns if col != 'Rikishi_ID']

    # First merge for east_id
    df_matches = df_matches.merge(
        final_df, 
        left_on='east_id', 
        right_on='Rikishi_ID', 
        how='left'
    )

    # Rename columns from df to add 'east_' prefix
    rename_dict_east = {col: f'east_{col}' for col in data_cols}
    df_merged = df_matches.rename(columns=rename_dict_east)

    # Second merge for west_id
    df_matches = df_merged.merge(
        final_df,
        left_on='west_id',
        right_on='Rikishi_ID',
        how='left'
    )

    # Rename columns from the second merge to add 'west_' prefix
    rename_dict_west = {col: f'west_{col}' for col in data_cols}
    df_matches = df_matches.rename(columns=rename_dict_west)

    return df_matches
