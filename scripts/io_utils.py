# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Function to categorize operations and define sepecific rules

import json
import yaml
import os
import pandas as pd

def load_yaml(file_path):
    """Load a YAML configuration file"""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def load_json(file_path):
    """Load a json files (e.g. Categorization rules)"""
    with open(file_path, 'r') as file:
        return json.load(file)
    
def load_bank_data(file_path, config):
    """
    Load bank CSV file with specific format
    """
    df = pd.read_csv(file_path, 
                     sep=config['separator'],
                     skiprows=config['skiprows'], 
                     encoding=config['encoding'])
    
    # Add account ref from filename
    filename = os.path.basename(file_path)
    df['Account'] = filename[:11]

    return df

def get_all_files(folder_path, extensions):
    """
    Return a list of file paths from a folder that match the given extensions.

    Args:
        folder_path (str): Path to the folder containing files.
        extensions (list of str): List of allowed file extensions (e.g., ['.csv']).

    Returns:
        list of str: List of file paths.
    """
    all_files = []
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext.lower()) for ext in extensions):
            all_files.append(os.path.join(folder_path, file))
    return all_files