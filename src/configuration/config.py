# System imports
import json
from typing import Dict, Any

CONFIG_FILE_PATH = 'src/configuration/config.json'

def load_config() -> Dict[str, Any]:
    """
    Loads the bot configuration from a JSON file.

    This function reads the 'config.json' file located in the 'src/configuration/' directory
    and returns its contents as a dictionary.

    :return: A dictionary containing the configuration settings.
    """
    with open(CONFIG_FILE_PATH, 'r') as f:
        config = json.load(f)
    return config

# Load the configuration into a global variable
config: Dict[str, Any] = load_config()