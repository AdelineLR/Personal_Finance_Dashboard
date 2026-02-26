# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Function to categorize operations and define sepecific rules

import json
import yaml
import os
import pandas as pd

def load_yaml(file_path: str) -> dict:
    """Load a yaml file"""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) 

def load_json(file_path: str) -> dict:
    """Load a json files (e.g. Categorization rules)"""
    with open(file_path, 'r') as file:
        return json.load(file)
    
def load_raw_data(file_path: str, config: dict) -> pd.DataFrame:
    """ Load CSV file with specific formatting (separator, encoding, skiprows) defined in config and add Account column. """
    df = pd.read_csv(file_path,
                     sep=config['separator'],
                     skiprows=config['skiprows'],
                     encoding=config['encoding'])
    # Add account column
    account = os.path.basename(file_path)[:11]
    df['Account'] = account
    return df

def get_all_files(folder_path : str, extensions: list) -> list:
    """ Return a list of file paths from a folder that match the given extensions. """
    all_files = []
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext.lower()) for ext in extensions):
            all_files.append(os.path.join(folder_path, file))
    return all_files