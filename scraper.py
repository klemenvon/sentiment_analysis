import requests
import json

# File that scrapes a particualr steam app, then creates database entries for each of the comments


def scrape_steam_reviews(app_id, params):
    """
    Scrapes Steam reviews for a given app ID.

    Args:
        app_id (str): The Steam app ID.
        params (dict): A dictionary of parameters to pass to the API.

    Returns:
        dict: A dictionary containing the JSON response from the API.
    """
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
