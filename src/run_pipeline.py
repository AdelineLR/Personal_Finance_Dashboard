import os
import pandas as pd
import logging
from src.io_utils import load_json, get_all_files, load_raw_data
from src.config_loader import load_config
from src.clean import clean_bank_data
from src.categorize import categorize_operations

# Load existing database (if exists)
def load_existing_dataset(config: dict) -> pd.DataFrame:
    """ Load existing dataset if it exists, otherwise return an empty DataFrame. """
    if os.path.exists(config['output_final']):
        df = pd.read_csv(config['output_final'])
        df ['Date'] = pd.to_datetime(df ['Date'], errors='coerce')
    return df

# Load raw files
def load_raw_files(config: dict) -> pd.DataFrame:
    """ Load and concatenate all raw files from the input folder. """
    raw_files = get_all_files(config['input_folder'], config['file_extensions'])
    df = pd.concat([load_raw_data(f, config) for f in raw_files], ignore_index=True)
    return df

# Clean raw data
def clean_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """ Clean raw data using the cleaning pipeline defined in clean.py. """
    return clean_bank_data(df, config)


# Remove existing rows
def remove_existing_rows(df_clean: pd.DataFrame, df_existing: pd.DataFrame, config: dict) -> pd.DataFrame:
    """ Remove rows from the cleaned DataFrame that already exist in the existing dataset. """
    if df_existing.empty:
        return df_clean
    df_merged = df_clean.merge(
            df_existing,
            on=config['merge_col'], 
            how='left', 
            indicator=True
            )
    return df_merged[df_merged['_merge']=='left_only'].drop(columns=['_merge'])

# Categorize data
def categorize_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """ Categorize operations using rules defined in a JSON file. """
    if df.empty:
        return df
    
    rules = load_json(config['rules_file'])

    return categorize_operations(
        df, 
        config['category_columns'], 
        category_rules=rules
        )

def save_final_dataset(df_new: pd.DataFrame, df_existing: pd.DataFrame, config: dict) -> None:
    """ Merge new and existing data and save result."""
    # Combine old and new data
    df = pd.concat(
        [df_existing, df_new], 
        ignore_index=True
        )
    # Sort by date
    df.sort_values(
        'Date', 
        inplace=True
        )
    # Save to CSV
    df.to_csv(
        config['output_final'], 
        sep=',', 
        index=False
        )
    logging.info(f"{len(df_new)} new operations added")


def run_pipeline():
    """ Main function to run the data processing pipeline. """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
        )

    logging.info("Pipeline started")

    config = load_config()
    
    if not config:
        raise ValueError("Configuration is empty. Check your YAML file!")

    df_existing = load_existing_dataset(config)
    df_raw = load_raw_files(config)
    df_clean = clean_data(df_raw, config)
    df_new = remove_existing_rows(df_clean, df_existing, config)

    if df_new.empty:
        logging.info("No new operations to add.")
        return

    df_new_cat = categorize_data(df_new, config)
    save_final_dataset(df_existing, df_new_cat, config)

    logging.info("Pipeline finished successfully")

if __name__ == "__main__":
    run_pipeline()