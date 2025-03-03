import pandas as pd
import numpy as np
from typing import Dict, List, Set, Optional, Tuple, Any, Union
import functools


class SumoDataProcessor:
    """
    A class for processing sumo match data and generating various statistics and features.
    Allows selective feature generation through configuration parameters and performs
    all calculations in a single pass through the data for efficiency.
    """

    def __init__(self, session=None):
        """
        Initialize the SumoDataProcessor.

        Args:
            session: Database session for querying rikishi data (optional)
        """
        self.session = session
        self.rikishi_lookup = {}

        # Load rikishi data if session is provided
        if self.session and hasattr(self.session, "query"):
            self._load_rikishi_data()

    def _load_rikishi_data(self):
        """Load rikishi data from the database into a lookup dictionary."""
        try:
            from models import Rikishi  # Assuming models module exists

            self.rikishi_lookup = {
                rikishi.id: rikishi for rikishi in self.session.query(Rikishi).all()
            }
        except (ImportError, AttributeError) as e:
            print(f"Warning: Could not load rikishi data: {e}")

    def process_dataframe(
        self,
        df_matches: pd.DataFrame,
        add_winstreaks: bool = False,
        add_opponent_ratio: bool = False,
        add_win_counts: bool = False,
        mark_winners: bool = False,
        add_top_moves: bool = False,
        top_moves_count: int = 0,
        add_rikishi_stats: bool = False,
        fix_missing_rikishi: bool = False,
    ) -> pd.DataFrame:
        """
        Process a dataframe of sumo matches and add requested features in a single pass.

        Args:
            df_matches: DataFrame containing sumo match data
            add_winstreaks: Add current winstreak for each rikishi
            add_opponent_ratio: Add historical win ratio against current opponent
            add_win_counts: Add total win counts for each rikishi
            mark_winners: Add column indicating if east rikishi won
            add_top_moves: Add top winning and losing moves for each rikishi
            top_moves_count: Number of top moves to track per category
            add_rikishi_stats: Add physical stats (height/weight) for each rikishi
            fix_missing_rikishi: Create placeholder entries for missing rikishi

        Returns:
            DataFrame with added features
        """
        print("nah")
        return

        # Create a copy to avoid modifying the original
        df = df_matches.copy()

        # Sort by basho and day to ensure chronological ordering
        df = df.sort_values(["basho_id", "day"], ascending=True).reset_index(drop=True)

        # Initialize result columns based on enabled features
        if mark_winners:
            df["east_win"] = (df["winner_id"] == df["east_id"]).astype(int)

        # Initialize data structures for tracking state
        n_matches = len(df)

        # Winstreaks
        if add_winstreaks:
            east_streaks = np.zeros(n_matches, dtype=int)
            west_streaks = np.zeros(n_matches, dtype=int)
            winstreaks = {}  # rikishi_id -> current winstreak

        # Win counts
        if add_win_counts:
            east_wins = np.zeros(n_matches, dtype=int)
            west_wins = np.zeros(n_matches, dtype=int)
            win_counts = {}  # rikishi_id -> total wins

        # Opponent ratios
        if add_opponent_ratio:
            east_ratios = np.zeros(n_matches, dtype=float)
            west_ratios = np.zeros(n_matches, dtype=float)
            head_to_head = {}  # rikishi_id -> {opponent_id -> wins against}

        # Top moves
        if add_top_moves:
            moves_data = (
                {}
            )  # rikishi_id -> {move -> {"w": wins_with_move, "l": losses_with_move}}
            # Initialize arrays for storing results
            move_stats = {
                "east": {
                    "wins": [
                        {
                            "move": np.zeros(n_matches, dtype=int),
                            "percent": np.zeros(n_matches, dtype=float),
                        }
                        for _ in range(top_moves_count)
                    ],
                    "losses": [
                        {
                            "move": np.zeros(n_matches, dtype=int),
                            "percent": np.zeros(n_matches, dtype=float),
                        }
                        for _ in range(top_moves_count)
                    ],
                },
                "west": {
                    "wins": [
                        {
                            "move": np.zeros(n_matches, dtype=int),
                            "percent": np.zeros(n_matches, dtype=float),
                        }
                        for _ in range(top_moves_count)
                    ],
                    "losses": [
                        {
                            "move": np.zeros(n_matches, dtype=int),
                            "percent": np.zeros(n_matches, dtype=float),
                        }
                        for _ in range(top_moves_count)
                    ],
                },
            }
            win_count_for_moves = (
                {}
            )  # rikishi_id -> total wins (for percentage calculation)
            loss_count_for_moves = (
                {}
            )  # rikishi_id -> total losses (for percentage calculation)

        # Rikishi physical stats
        if add_rikishi_stats:
            if not self.session and (add_rikishi_stats or fix_missing_rikishi):
                raise ValueError("Database session is required for rikishi_stats")

            east_weights = np.zeros(n_matches, dtype=object)
            east_heights = np.zeros(n_matches, dtype=object)
            west_weights = np.zeros(n_matches, dtype=object)
            west_heights = np.zeros(n_matches, dtype=object)

            # Pre-load all rikishi data if using rikishi stats
            if not self.rikishi_lookup:
                self._load_rikishi_data()

        # Single pass through the data
        for idx, match in enumerate(df.itertuples()):
            east_id = match.east_id
            west_id = match.west_id
            winner_id = match.winner_id
            east_won = winner_id == east_id

            # Process winstreaks
            if add_winstreaks:
                east_ws = winstreaks.get(east_id, 0)
                west_ws = winstreaks.get(west_id, 0)

                east_streaks[idx] = east_ws
                west_streaks[idx] = west_ws

                if east_won:
                    winstreaks[east_id] = east_ws + 1
                    winstreaks[west_id] = 0
                else:
                    winstreaks[west_id] = west_ws + 1
                    winstreaks[east_id] = 0

            # Process win counts
            if add_win_counts:
                east_w = win_counts.get(east_id, 0)
                west_w = win_counts.get(west_id, 0)

                east_wins[idx] = east_w
                west_wins[idx] = west_w

                if east_won:
                    win_counts[east_id] = east_w + 1
                else:
                    win_counts[west_id] = west_w + 1

            # Process opponent ratios
            if add_opponent_ratio:
                if east_id not in head_to_head:
                    head_to_head[east_id] = {}
                if west_id not in head_to_head:
                    head_to_head[west_id] = {}

                east_wins_vs_west = head_to_head[east_id].get(west_id, 0)
                west_wins_vs_east = head_to_head[west_id].get(east_id, 0)

                total_matches = east_wins_vs_west + west_wins_vs_east
                east_ratios[idx] = (
                    east_wins_vs_west / total_matches if total_matches > 0 else 0.5
                )
                west_ratios[idx] = (
                    west_wins_vs_east / total_matches if total_matches > 0 else 0.5
                )

                # Update head-to-head record after calculating the ratio for the current match
                if east_won:
                    head_to_head[east_id][west_id] = east_wins_vs_west + 1
                else:
                    head_to_head[west_id][east_id] = west_wins_vs_east + 1

            # Process top moves
            if add_top_moves:
                kimarite = match.kimarite

                # Ensure data structures exist
                if east_id not in moves_data:
                    moves_data[east_id] = {}
                    win_count_for_moves[east_id] = 0
                    loss_count_for_moves[east_id] = 0

                if west_id not in moves_data:
                    moves_data[west_id] = {}
                    win_count_for_moves[west_id] = 0
                    loss_count_for_moves[west_id] = 0

                if kimarite not in moves_data[east_id]:
                    moves_data[east_id][kimarite] = {"w": 0, "l": 0}

                if kimarite not in moves_data[west_id]:
                    moves_data[west_id][kimarite] = {"w": 0, "l": 0}

                # Get top moves for display in current match
                def get_top_moves(rikishi_id, sort_by="w"):
                    if rikishi_id not in moves_data:
                        return []

                    rikishi_moves = moves_data[rikishi_id]
                    sorted_moves = sorted(
                        rikishi_moves.keys(),
                        key=lambda move: rikishi_moves[move][sort_by],
                        reverse=True,
                    )
                    return sorted_moves

                east_top_wins = get_top_moves(east_id, "w")
                east_top_losses = get_top_moves(east_id, "l")
                west_top_wins = get_top_moves(west_id, "w")
                west_top_losses = get_top_moves(west_id, "l")

                # Record current top moves in results
                for i in range(top_moves_count):
                    # East wins
                    if i < len(east_top_wins):
                        move = east_top_wins[i]
                        wins_with_move = moves_data[east_id][move]["w"]
                        total_wins = win_count_for_moves[east_id]
                        percent = wins_with_move / total_wins if total_wins > 0 else 1.0

                        move_stats["east"]["wins"][i]["move"][idx] = (
                            self._kimarite_to_value(move)
                        )
                        move_stats["east"]["wins"][i]["percent"][idx] = percent

                    # East losses
                    if i < len(east_top_losses):
                        move = east_top_losses[i]
                        losses_with_move = moves_data[east_id][move]["l"]
                        total_losses = loss_count_for_moves[east_id]
                        percent = (
                            losses_with_move / total_losses if total_losses > 0 else 1.0
                        )

                        move_stats["east"]["losses"][i]["move"][idx] = (
                            self._kimarite_to_value(move)
                        )
                        move_stats["east"]["losses"][i]["percent"][idx] = percent

                    # West wins
                    if i < len(west_top_wins):
                        move = west_top_wins[i]
                        wins_with_move = moves_data[west_id][move]["w"]
                        total_wins = win_count_for_moves[west_id]
                        percent = wins_with_move / total_wins if total_wins > 0 else 1.0

                        move_stats["west"]["wins"][i]["move"][idx] = (
                            self._kimarite_to_value(move)
                        )
                        move_stats["west"]["wins"][i]["percent"][idx] = percent

                    # West losses
                    if i < len(west_top_losses):
                        move = west_top_losses[i]
                        losses_with_move = moves_data[west_id][move]["l"]
                        total_losses = loss_count_for_moves[west_id]
                        percent = (
                            losses_with_move / total_losses if total_losses > 0 else 1.0
                        )

                        move_stats["west"]["losses"][i]["move"][idx] = (
                            self._kimarite_to_value(move)
                        )
                        move_stats["west"]["losses"][i]["percent"][idx] = percent

                # Update move statistics after recording current state
                if east_won:
                    # East won with this move
                    moves_data[east_id][kimarite]["w"] += 1
                    win_count_for_moves[east_id] += 1

                    # West lost to this move
                    moves_data[west_id][kimarite]["l"] += 1
                    loss_count_for_moves[west_id] += 1
                else:
                    # West won with this move
                    moves_data[west_id][kimarite]["w"] += 1
                    win_count_for_moves[west_id] += 1

                    # East lost to this move
                    moves_data[east_id][kimarite]["l"] += 1
                    loss_count_for_moves[east_id] += 1

            # Process rikishi physical stats
            if add_rikishi_stats:
                # Process east rikishi
                try:
                    r_east = self.rikishi_lookup.get(east_id)
                    if r_east is None and fix_missing_rikishi:
                        r_east = self._scramble_rikishi(east_id)
                        self.session.add(r_east)
                        self.rikishi_lookup[east_id] = r_east
                        print(f"Rikishi '{east_id}' is being added.")
                        self.session.commit()

                    if r_east:
                        east_weights[idx] = r_east.weight
                        east_heights[idx] = r_east.height
                    else:
                        east_weights[idx] = None
                        east_heights[idx] = None

                except Exception as e:
                    print(f"Error processing east rikishi {east_id}: {e}")
                    east_weights[idx] = None
                    east_heights[idx] = None

                # Process west rikishi
                try:
                    r_west = self.rikishi_lookup.get(west_id)
                    if r_west is None and fix_missing_rikishi:
                        r_west = self._scramble_rikishi(west_id)
                        self.session.add(r_west)
                        self.rikishi_lookup[west_id] = r_west
                        print(f"Rikishi '{west_id}' is being added.")
                        self.session.commit()

                    if r_west:
                        west_weights[idx] = r_west.weight
                        west_heights[idx] = r_west.height
                    else:
                        west_weights[idx] = None
                        west_heights[idx] = None

                except Exception as e:
                    print(f"Error processing west rikishi {west_id}: {e}")
                    west_weights[idx] = None
                    west_heights[idx] = None

        # Add computed columns to dataframe
        if add_winstreaks:
            df["east_winstreak"] = east_streaks
            df["west_winstreak"] = west_streaks

        if add_win_counts:
            df["east_wins"] = east_wins
            df["west_wins"] = west_wins

        if add_opponent_ratio:
            df["east_ratio"] = east_ratios
            df["west_ratio"] = west_ratios

        if add_top_moves:
            for i in range(top_moves_count):
                # East win moves
                east_n_win_move = f"east_n{i+1}_win_move"
                east_n_win_perc = f"east_n{i+1}_win_percent"
                df[east_n_win_move] = move_stats["east"]["wins"][i]["move"]
                df[east_n_win_perc] = move_stats["east"]["wins"][i]["percent"]

                # East loss moves
                east_n_loss_move = f"east_n{i+1}_loss_move"
                east_n_loss_perc = f"east_n{i+1}_loss_percent"
                df[east_n_loss_move] = move_stats["east"]["losses"][i]["move"]
                df[east_n_loss_perc] = move_stats["east"]["losses"][i]["percent"]

                # West win moves
                west_n_win_move = f"west_n{i+1}_win_move"
                west_n_win_perc = f"west_n{i+1}_win_percent"
                df[west_n_win_move] = move_stats["west"]["wins"][i]["move"]
                df[west_n_win_perc] = move_stats["west"]["wins"][i]["percent"]

                # West loss moves
                west_n_loss_move = f"west_n{i+1}_loss_move"
                west_n_loss_perc = f"west_n{i+1}_loss_percent"
                df[west_n_loss_move] = move_stats["west"]["losses"][i]["move"]
                df[west_n_loss_perc] = move_stats["west"]["losses"][i]["percent"]

        if add_rikishi_stats:
            df["east_weight"] = east_weights
            df["east_height"] = east_heights
            df["west_weight"] = west_weights
            df["west_height"] = west_heights

        return df

    def get_move_statistics(self, df_matches: pd.DataFrame) -> pd.DataFrame:
        """
        Count wins and losses by move type for each rikishi.

        Args:
            df_matches: DataFrame containing sumo match data

        Returns:
            DataFrame with move statistics per rikishi and move type
        """
        win_moves: Dict[int, Dict[str, int]] = {}
        loss_moves: Dict[int, Dict[str, int]] = {}

        for match in df_matches.itertuples():
            east_id = match.east_id
            west_id = match.west_id
            east_won = match.winner_id == east_id
            kimarite = match.kimarite

            winner_id, loser_id = (east_id, west_id) if east_won else (west_id, east_id)

            # Initialize dictionaries if needed
            if winner_id not in win_moves:
                win_moves[winner_id] = {}
            if loser_id not in loss_moves:
                loss_moves[loser_id] = {}

            # Update win move count
            win_moves[winner_id][kimarite] = win_moves[winner_id].get(kimarite, 0) + 1

            # Update loss move count
            loss_moves[loser_id][kimarite] = loss_moves[loser_id].get(kimarite, 0) + 1

        # Transform into a structured format for the DataFrame
        data = []

        # Get all unique rikishi IDs and kimarite types
        unique_ids = set(win_moves.keys()).union(set(loss_moves.keys()))
        all_kimarites: Set[str] = set()

        for moves_dict in win_moves.values():
            all_kimarites.update(moves_dict.keys())
        for moves_dict in loss_moves.values():
            all_kimarites.update(moves_dict.keys())

        # Build the data for the DataFrame
        for rikishi_id in unique_ids:
            for kimarite in all_kimarites:
                wins = win_moves.get(rikishi_id, {}).get(kimarite, 0)
                losses = loss_moves.get(rikishi_id, {}).get(kimarite, 0)

                if wins > 0 or losses > 0:  # Only include non-zero entries
                    data.append(
                        {
                            "Rikishi_ID": rikishi_id,
                            "Move_Type": kimarite,
                            "Win_Count": wins,
                            "Loss_Count": losses,
                        }
                    )

        return pd.DataFrame(data)

    def _kimarite_to_value(self, kimarite: str) -> int:
        """Convert kimarite (move name) to numeric value for storage."""
        # This function placeholder should be defined based on your implementation
        # For now, returning a hash of the string as a simple implementation
        return hash(kimarite) % 10000

    def _scramble_rikishi(self, rikishi_id: int):
        """Create a placeholder rikishi entry with generated values."""
        try:
            import random
            from models import Rikishi  # Assuming models module exists

            return Rikishi(
                id=rikishi_id,
                shikona_en=f"Unknown-{rikishi_id}",
                weight=random.randint(100, 200),
                height=random.randint(160, 200),
            )
        except ImportError:
            print("Warning: models module not found, cannot create rikishi")
            return None
