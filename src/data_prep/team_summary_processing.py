import pandas as pd
import ast

from src.data_prep.load_data import get_team_data


def get_kit_information(team_data):
    if team_data["kit"] is None:
        kit = False
        kit_shirt_type = None
        kit_shirt_logo = None
        kit_socks_type = None

    else:
        kit_dict = ast.literal_eval(team_data["kit"])
        kit = True
        kit_shirt_type = kit_dict["kit_shirt_type"]
        kit_shirt_logo = kit_dict["kit_shirt_logo"]
        kit_socks_type = kit_dict["kit_socks_type"]

    kit_summary_data = {
        "kit": kit,
        "kit_shirt_type": kit_shirt_type,
        "kit_shirt_logo": kit_shirt_logo,
        "kit_socks_type": kit_socks_type,
    }

    return kit_summary_data


def process_team_history(team_history_data):
    if len(team_history_data["past"]) == 0:
        min_rank_history = None
        max_rank_history = None
        stdev_rank_history = None
        max_total_points_history = None
        earliest_season_year_history = None
        career_break_history = None
        seasons_played_in = None
    else:
        # Convert to DataFrame and extract the start year as an integer
        team_history_data_df = pd.DataFrame(team_history_data["past"])
        team_history_data_df["start_year"] = team_history_data_df["season_name"].apply(
            lambda x: int(x.split("/")[0])
        )

        # Calculate the differences between consecutive years
        team_history_data_df["year_diff"] = team_history_data_df["start_year"].diff()

        # Get metrics
        min_rank_history = team_history_data_df["rank"].min()
        max_rank_history = team_history_data_df["rank"].max()
        stdev_rank_history = round(team_history_data_df["rank"].std(), 3)
        max_total_points_history = team_history_data_df["total_points"].max()
        earliest_season_year_history = team_history_data_df["start_year"].min()
        career_break_history = team_history_data_df["year_diff"].max()
        seasons_played_in = len(team_history_data_df["season_name"])

    # Handle NaN by replacing it with None
    if pd.isna(stdev_rank_history):
        stdev_rank_history = None
    else:
        pass

    if pd.isna(career_break_history):
        career_break_history = None
    else:
        pass

    # Create summary dictionary
    team_summary_history_data = {
        "min_rank_history": min_rank_history,
        "max_rank_history": max_rank_history,
        "stdev_rank_history": stdev_rank_history,
        "max_total_points_history": max_total_points_history,
        "earliest_season_year_history": earliest_season_year_history,
        "career_break_history": career_break_history,
        "seasons_played_in": seasons_played_in,
    }

    return team_summary_history_data


def aggregate_team_data(team_data, kit_summary_data, team_summary_history_data):
    # Create the team_summary_data dictionary
    team_summary_data = {
        "id": team_data["id"],
        "name": team_data["name"],
        "player_region_iso_code_long": team_data["player_region_name"],
        "years_active": team_data["years_active"],
        "joined_time": team_data["joined_time"][:10],
        "classic_leagues_competed_in": len(team_data["leagues"]["classic"]),
        "h2h_leagues_competed_in": len(team_data["leagues"]["h2h"]),
        "last_deadline_bank": team_data["last_deadline_bank"],
        "last_deadline_value": team_data["last_deadline_value"],
        "last_deadline_total_transfers": team_data["last_deadline_total_transfers"],
        "summary_overall_points": team_data["summary_overall_points"],
        "summary_overall_rank": team_data["summary_overall_rank"],
        "name_change_blocked": team_data["name_change_blocked"],
        "leagues_admin": sum(
            1
            for league in team_data["leagues"]["classic"]
            if league.get("entry_can_admin", False)
        ),
        "kit": kit_summary_data["kit"],
        "kit_shirt_type": kit_summary_data["kit_shirt_type"],
        "kit_shirt_logo": kit_summary_data["kit_shirt_logo"],
        "kit_socks_type": kit_summary_data["kit_socks_type"],
        "min_rank_history": team_summary_history_data["min_rank_history"],
        "max_rank_history": team_summary_history_data["max_rank_history"],
        "stdev_rank_history": team_summary_history_data["stdev_rank_history"],
        "max_total_points_history": team_summary_history_data[
            "max_total_points_history"
        ],
        "earliest_season_year_history": team_summary_history_data[
            "earliest_season_year_history"
        ],
        "career_break_history": team_summary_history_data["career_break_history"],
        "seasons_played_in": team_summary_history_data["seasons_played_in"],
    }

    return team_summary_data


def get_team_summary(team_data, team_history_data):
    # Get kit information
    kit_summary_data = get_kit_information(team_data)

    # Process team history
    team_summary_history_data = process_team_history(
        team_history_data=team_history_data
    )

    # Create team summary
    team_summary_data = aggregate_team_data(
        team_data,
        kit_summary_data=kit_summary_data,
        team_summary_history_data=team_summary_history_data,
    )

    return team_summary_data
