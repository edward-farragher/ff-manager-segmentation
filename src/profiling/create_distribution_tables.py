import pandas as pd
import numpy as np


def create_distribution_table_numeric(df, column_name):
    # Calculate the total number of non-NaN rows
    total_non_nan_rows = len(df[column_name].dropna())

    # Calculate the counts for each unique value
    value_counts = df[column_name].value_counts().sort_index()

    # Calculate percentage of rows that are each value and above
    cumulative_counts_above = value_counts.sort_index(ascending=False).cumsum()
    percentage_above = (cumulative_counts_above / total_non_nan_rows) * 100

    # Calculate percentage of rows that are each value and below
    cumulative_counts_below = value_counts.sort_index(ascending=True).cumsum()
    percentage_below = (cumulative_counts_below / total_non_nan_rows) * 100

    # Create the distribution table
    distribution_table = pd.DataFrame(
        {
            "column_name": column_name,
            "value": value_counts.index,
            "total_volume_sample": value_counts.values,
            "percentage_above": value_counts.index.map(percentage_above),
            "percentage_below": value_counts.index.map(percentage_below),
        }
    )

    # Round percentages
    distribution_table["percentage_above"] = distribution_table[
        "percentage_above"
    ].round(3)
    distribution_table["percentage_below"] = distribution_table[
        "percentage_below"
    ].round(3)

    return distribution_table


def create_distribution_table_categorical(df, column_name):
    # Calculate the proportion of each unique value
    percentage_share = df[column_name].value_counts(normalize=True)

    # Create distribution table
    distribution_table = pd.DataFrame(
        {
            "column_name": column_name,
            "value": percentage_share.index,
            "percentage_share": percentage_share.values,
        }
    )

    # Add ranks
    distribution_table["rank_ascending"] = distribution_table["percentage_share"].rank(
        method="min", ascending=True
    )
    distribution_table["rank_descending"] = distribution_table["percentage_share"].rank(
        method="min", ascending=False
    )

    # Round percentages
    distribution_table["percentage_share"] = distribution_table[
        "percentage_share"
    ].round(3)

    return distribution_table


def create_distribution_tables_aggregated(df, impute_nulls):
    column_data_types = {
        "player_region_iso_code_long": "categorical",
        "name_change_blocked": "categorical",
        "kit": "categorical",
        "kit_shirt_type": "categorical",
        "kit_shirt_logo": "categorical",
        "kit_socks_type": "categorical",
        "kit_full": "categorical",
        "classic_leagues_competed_in": "numeric",
        "h2h_leagues_competed_in": "numeric",
        "last_deadline_bank": "numeric",
        "last_deadline_value": "numeric",
        "last_deadline_total_transfers": "numeric",
        "summary_overall_points": "numeric",
        "summary_overall_rank": "numeric",
        "leagues_admin": "numeric",
        "min_rank_history": "numeric",
        "max_total_points_history": "numeric",
        "earliest_season_year_history": "numeric",
        "career_break_history": "numeric",
        "seasons_played_in": "numeric",
        "yoyo_score": "numeric",
        "rising_score": "numeric",
    }

    # Fill NaN values in each column with specified values
    df = df.fillna(value=impute_nulls)

    distribution_table_numeric = pd.DataFrame(
        columns=[
            "column_name",
            "value",
            "total_volume_sample",
            "percentage_above",
            "percentage_below",
        ]
    )
    distribution_table_categorical = pd.DataFrame(
        columns=[
            "column_name",
            "value",
            "percentage_share",
            "rank_ascending",
            "rank_descending",
        ]
    )

    for column_name, column_type in column_data_types.items():
        if column_type == "numeric":
            distribution_table_stage_numeric = create_distribution_table_numeric(
                df=df, column_name=column_name
            )
            distribution_table_numeric = pd.concat(
                [distribution_table_numeric, distribution_table_stage_numeric], axis=0
            )
        elif column_type == "categorical":
            distribution_table_stage_categorical = (
                create_distribution_table_categorical(df=df, column_name=column_name)
            )
            distribution_table_categorical = pd.concat(
                [distribution_table_categorical, distribution_table_stage_categorical],
                axis=0,
            )
        else:
            pass

    return distribution_table_numeric, distribution_table_categorical
