from src.data_prep.create_sample import get_all_data_sample
from datetime import datetime
import pandas as pd


# Get the current date and time
now = datetime.now()

# Format date and time as a string in the format YYYYMMDDHHMMSS
date_time_str = now.strftime("%Y%m%d%H%M%S")

# Get sample data
sample_data = get_all_data_sample()

df = pd.DataFrame(sample_data)

# Save DataFrame to CSV
file_path = f"data/{date_time_str}_team_sample_data.csv"
df.to_csv(file_path, index=False)
