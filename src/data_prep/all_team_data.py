from src.data_prep.team_summary_processing import get_team_summary
from src.data_prep.load_data import get_team_data


def get_all_team_data(team_id):
    team_data, team_history_data = get_team_data(team_id)
    team_summary_data = get_team_summary(team_data, team_history_data)
    all_team_data = team_summary_data
    return all_team_data
