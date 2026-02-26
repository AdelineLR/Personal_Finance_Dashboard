import os
from src.io_utils import load_yaml


def config_path() -> str:
    """ Determine which config file should be used. """
    if os.path.exists("data/raw/personal"):
        return "config/config_local.yml"
    return "config/config_example.yml"


def load_config() -> dict:
    """ Load project configuration. """
    path = config_path()
    return load_yaml(path)