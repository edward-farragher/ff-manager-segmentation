from src.data_prep.create_sample import get_all_data_sample
from src.profiling.create_distribution_tables import create_distribution_tables_aggregated
import pandas as pd

### Data Collection

# Get sample data
sample_data = get_all_data_sample()

df = pd.DataFrame(sample_data)

# Save DataFrame as CSV
file_path = f"data/sample/team_sample_data.csv"
df.to_csv(file_path, index=False)


### Profiling

# Create profile distribution tables
distribution_table_numeric, distribution_table_categorical = create_distribution_tables_aggregated(df=df)

# Save DataFrame as CSVs
distribution_table_numeric.to_csv(f"data/variable_distributions/numeric_columns.csv", index=False)
distribution_table_categorical.to_csv(
    f"data/variable_distributions/categorical_columns.csv", index=False
)
