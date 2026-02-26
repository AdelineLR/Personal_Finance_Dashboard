import pytest
import pandas as pd
from src.run_pipeline import (
    load_existing_dataset,
    load_raw_files,
    clean_data,
    remove_existing_rows,
    categorize_data,
    save_final_dataset
)
from src.config_loader import load_config

config = load_config()

def test_load_existing_dataset():
    df = load_existing_dataset(config)
    assert isinstance(df, pd.DataFrame)

def test_load_raw_files():
    df = load_raw_files(config)
    assert isinstance(df, pd.DataFrame)
    assert 'Account' in df.columns, "La colonne 'Account' est manquante dans les données brutes chargées."

def test_clean_data():
    df_raw = load_raw_files(config)
    df_clean = clean_data(df_raw, config)
    missing_cols = [col for col in config['merge_col'] if col not in df_clean.columns]
    assert isinstance(df_clean, pd.DataFrame)
    assert not missing_cols, f"Colonnes merge_col manquantes après nettoyage : {missing_cols}"

def test_remove_existing_rows():
    df_raw = load_raw_files(config)
    df_clean = clean_data(df_raw, config)
    df_existing = load_existing_dataset(config)
    df_new = remove_existing_rows(df_clean, df_existing, config)
    assert isinstance(df_new, pd.DataFrame)

def test_categorize_data():
    df_raw = load_raw_files(config)
    df_clean = clean_data(df_raw, config)
    df_categorized = categorize_data(df_clean, config)
    missing_category_cols = [col for col in ['Category', 'Subcategory'] if col not in df_categorized.columns]
    assert isinstance(df_categorized, pd.DataFrame)
    assert not missing_category_cols, f"Colonnes de catégorisation manquantes : {missing_category_cols}"

def test_save_final_dataset():
    df_raw = load_raw_files(config)
    df_clean = clean_data(df_raw, config)
    df_existing = load_existing_dataset(config)
    df_new = remove_existing_rows(df_clean, df_existing, config)
    df_categorized = categorize_data(df_new, config)
    
    save_final_dataset(df_categorized, df_existing, config)
    
    # Reload the final dataset to check if it was saved correctly
    df_final = load_existing_dataset(config)
    assert isinstance(df_final, pd.DataFrame)