from src.data_prep.load_data import get_boostrap_data
from src.app_tools.yaml_loader import load_yaml_file
from src.data_prep.all_team_data import get_all_team_data
import pandas as pd
import random

# Get config
yaml_file_path = "conf/parameters.yaml"
config = load_yaml_file(yaml_file_path)


training_sample_size = config["training_sample_size"]
random_seed = config["random_seed"]


def get_sample_ids(training_sample_size, random_seed):
    bootstrap_data = get_boostrap_data()
    total_players = bootstrap_data["total_players"]
    random.seed(random_seed)
    sample_ids = random.sample(range(1, total_players + 1), training_sample_size)

    return sample_ids


def get_all_data_sample():
    # Get random sample of ids
    sample_ids = get_sample_ids(
        training_sample_size=training_sample_size, random_seed=random_seed
    )

    # Get data for each sample
    all_data = []
    for team_id in sample_ids:
        team_data = get_all_team_data(team_id)
        all_data.append(team_data)

    return all_data
