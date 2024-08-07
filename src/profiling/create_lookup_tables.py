import pandas as pd
import numpy as np

def create_lookup_table_numeric(df, column_name):
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

    # Create the lookup table
    lookup_table = pd.DataFrame({
        'column_name': column_name,
        'value': value_counts.index,
        'total_volume_sample': value_counts.values,
        'percentage_above': value_counts.index.map(percentage_above),
        'percentage_below': value_counts.index.map(percentage_below)
    })

    # Round percentages
    lookup_table['percentage_above'] = lookup_table['percentage_above'].round(3)
    lookup_table['percentage_below'] = lookup_table['percentage_below'].round(3)

    return lookup_table


def create_lookup_table_categorical(df, column_name):
    # Calculate the proportion of each unique value
    percentage_share = df[column_name].value_counts(normalize=True)

    # Create lookup table
    lookup_table = pd.DataFrame({
        'column_name': column_name,
        'value': percentage_share.index,
        'percentage_share': percentage_share.values
    })

    # Add ranks
    lookup_table['rank_ascending'] = lookup_table['percentage_share'].rank(method='min', ascending=True)
    lookup_table['rank_descending'] = lookup_table['percentage_share'].rank(method='min', ascending=False)

    # Round percentages
    lookup_table['percentage_share'] = lookup_table['percentage_share'].round(3)

    return lookup_table


def create_lookup_tables_aggregated(df, column_data_types):
    # Dictionary with fill values for each column
    fill_values = {
        'career_break_history': 0,   
        'kit': 'No Kit',
        'kit': 'No Kit',
        'kit_shirt_type': 'No Kit Shirt',
        'kit_shirt_logo': 'No Kit Logo',
        'kit_socks_type': 'No Kit Socks',
    }

    # Fill NaN values in each column with specified values
    df = df.fillna(value=fill_values)

    lookup_table_numeric = pd.DataFrame(columns=['column_name', 'value','total_volume_sample','percentage_above','percentage_below'])
    lookup_table_categorical = pd.DataFrame(columns=['column_name', 'value','percentage_share','rank_ascending','rank_descending'])

    for column_name, column_type in column_data_types.items():
        
        if column_type == 'numeric':
            lookup_table_stage_numeric = create_lookup_table_numeric(df=df,column_name=column_name)
            lookup_table_numeric = pd.concat([lookup_table_numeric, lookup_table_stage_numeric], axis=0)
        elif column_type == 'categorical':
            lookup_table_stage_categorical = create_lookup_table_categorical(df=df,column_name=column_name)
            lookup_table_categorical = pd.concat([lookup_table_categorical, lookup_table_stage_categorical], axis=0)
        else:
            pass

    return lookup_table_numeric, lookup_table_categorical