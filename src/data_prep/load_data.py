import requests
import concurrent.futures


def fetch_url(url):
    """
    Fetches data from a given URL using the requests library.

    Parameters:
    ----------
    url : str
        The URL to fetch data from.

    Returns:
    ----------
    data : dict or None
        The JSON data retrieved from the URL if the request is successful, otherwise None.
    """
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data
    else:
        return None


# Function to fetch URLs concurrently
def fetch_urls_concurrently(urls):
    """
    Fetches multiple URLs concurrently using ThreadPoolExecutor.

    Parameters:
    ----------
    urls : list
        A list of URLs to fetch.

    Returns:
    ----------
    results : list:
        A list containing the fetched results from the URLs.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(fetch_url, url) for url in urls]

        # Retrieve results as they become available
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results


def get_boostrap_data():
    """
    This gets the bootstrap static data from the Fantasy Premier League API.

    Returns
    -------
    dict
        A dictionary containing the bootstrap static data from the Fantasy Premier League API. This data typically includes information about teams, players, and other game-related metadata.

    Notes
    -----
    The data is fetched from the URL:
    'https://fantasy.premierleague.com/api/bootstrap-static/'
    """
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    bootstrap_data = fetch_url(url)
    return bootstrap_data


def get_team_data(team_id):
    """
    This gets the team data for a given team ID from the Fantasy Premier League API.

    Parameters
    ----------
    team_id : int
        The unique identifier for the team whose data is to be fetched.

    Returns
    -------
    dict
        A dictionary containing the team data from the Fantasy Premier League API. This data includes details about the team's players, performance, and other related information.

    Notes
    -----
    The data is fetched from the URL:
    'https://fantasy.premierleague.com/api/entry/{team_id}/', where `{team_id}` is replaced with the provided team ID.
    """
    team_url = f"https://fantasy.premierleague.com/api/entry/{team_id}/"
    team_data = fetch_url(team_url)

    team_history_url = f"https://fantasy.premierleague.com/api/entry/{team_id}/history/"
    team_history_data = fetch_url(team_history_url)

    return team_data, team_history_data
