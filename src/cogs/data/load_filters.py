# System imports
import json
from typing import List

# Define the path to the filters JSON file
FILTERS_FILE_PATH = 'src/cogs/data/filters.json'

def load_filters() -> List[str]:
    """
    Loads the global filters from a JSON file.

    This function reads the 'filters.json' file located in the 'src/cogs/data/' directory
    and returns a list of filters that apply globally to all users.

    If the file is not found, it returns an empty list.

    :return: A list containing all the filters, or an empty list if the file doesn't exist.
    """
    try:
        with open(FILTERS_FILE_PATH, 'r') as f:
            data = json.load(f)
            return data.get('filters', [])
    except FileNotFoundError:
        # Return an empty list if the filters file doesn't exist
        return []

def save_filters(filters: List[str]) -> None:
    """
    Saves the global filters to a JSON file.

    This function writes the provided list of filters into the 'filters.json' file
    located in the 'src/cogs/data/' directory, overwriting any existing data.

    :param filters: The list of filters to save.
    """
    with open(FILTERS_FILE_PATH, 'w') as f:
        json.dump({'filters': filters}, f, indent=4)
