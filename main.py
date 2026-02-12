import os
import pandas as pd
import logging
from scripts.clean import clean_bank_data
from scripts.categorize import categorize_operations#, build_specific_rules_from_json
from scripts.io_utils import load_json, load_yaml, get_all_files, load_bank_data

# Load configuration
config = load_yaml("config/config.yml")

# Load existing database (if exists)
if os.path.exists(config['output_final']):
    df_existing = pd.read_csv(config['output_final'])
    df_existing ['Date'] = pd.to_datetime(df_existing ['Date'], errors='coerce')
else:
    df_existing = pd.DataFrame()

# Load and clean raw files
raw_files = get_all_files(config['input_folder'], config['file_extensions'])
df_all = pd.concat([load_bank_data(f, config) for f in raw_files], ignore_index=True)
df_clean = clean_bank_data(df_all, config)

# Remove already processed rows
if not df_existing.empty:
    df_merged = df_clean.merge(
        df_existing,
        on=config['merge_col'], 
        how='left', 
        indicator=True
        )

    df_new = df_merged[df_merged['_merge']=='left_only'].drop(columns=['_merge'])

else:
    df_new = df_clean

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Categorize new data
if not df_new.empty:
    rules = load_json(config['rules_file'])
    # specific_rules_raw = load_json(config['specific_rules']) # ToDo : to remove later if not used
    # specific_rules = build_specific_rules_from_json(df_new, specific_rules_raw) 
    df_new_cat = categorize_operations(
        df_new, 
        config['category_columns'], 
        category_rules=rules
        )

    # Combine old and new data
    df_final = pd.concat(
        [df_existing, df_new_cat], 
        ignore_index=True
        )
    df_final.sort_values(
        'Date', 
        inplace=True
        )

    df_final.to_csv(
        config['output_final'], 
        sep=',', 
        index=False
        )
    logging.info(f"{len(df_new)} new operations added")
else:
    logging.info("No new operations to add.")