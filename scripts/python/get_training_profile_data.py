from src.data_prep.create_sample import get_all_data_sample
from src.profiling.create_lookup_tables import create_lookup_tables_aggregated
import pandas as pd
from src.app_tools.yaml_loader import load_yaml_file

### Data Collection

# Get sample data
sample_data = get_all_data_sample()

df = pd.DataFrame(sample_data)

# Save DataFrame as CSV
file_path = f"data/sample/team_sample_data.csv"
df.to_csv(file_path, index=False)


### Profiling

# Get data types
yaml_file_path = "conf/column_data_types.yaml"
column_data_types = load_yaml_file(yaml_file_path)

# Create profile lookup tables
lookup_table_numeric, lookup_table_categorical = create_lookup_tables_aggregated(df, column_data_types)

# Save DataFrame as CSVs
lookup_table_numeric.to_csv(f'data/profile_lookup/numeric_columns.csv', index=False)
lookup_table_categorical.to_csv(f'data/profile_lookup/categorical_columns.csv', index=False)
