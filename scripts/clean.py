# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Functions to clean bank data

import pandas as pd
from datetime import datetime as dt

def drop_empty_columns(df):
    """
    Drop columns with only NaN values.
    """
    na_col = df.columns[df.isna().sum() == len(df)].tolist()
    return df.drop(columns=na_col)

def drop_duplicates(df):
    """
    Drop duplicates operations
    """
    return df.drop_duplicates(ignore_index=True)

def rename_columns(df, new_names):
    """
    Rename dataframe columns.
    """
    df.columns = new_names
    return df

def convert_date_column(df, column):
    """
    Convert a string column to datetime (day-first format).
    """
    df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')
    return df

def convert_amount_column(df, column):
    """
    Replace comma with dot in a string amount column and convert to float.
    """
    df[column] = df[column].str.replace(',', '.', regex=False).astype(float)
    return df

def add_Debit_Credit_column(df, amount_column, new_column='Debit/Credit'):
    """
    Create a new column to indicate if the operation is a debit or credit.
    """
    df[new_column] = 'Debit'
    df.loc[df[amount_column] > 0, new_column] = 'Credit'
    return df

def add_date_parts(df, date_column):
    """
    Add 'Month' and 'Year' columns from a date column.
    """
    df['Month'] = df[date_column].dt.month
    df['Year'] = df[date_column].dt.year
    return df

def clean_bank_data(df_raw, config):
    """
    Perform full cleaning pipeline on raw bank statement data.
    
    Returns a cleaned DataFrame with:
    - Drop empty columns
    - Rename columns
    - Convert date and amount fields
    - Add debit/credit classification
    - Extract month and year

    Args:
        df_raw (pd.DataFrame): Raw input DataFrame.
        config (dict): Configuration parameters loaded from a YAML file.
    Returns:
        pd.DataFrame: Cleaned DataFrame ready for analysis.
    """
    df = df_raw.copy()
    df = drop_empty_columns(df)
    df = drop_duplicates(df)
    df = rename_columns(df, config['rename_columns'])
    df['Currency'] = 'Euros'
    df = convert_date_column(df, config['date_column'])
    df = convert_amount_column(df, config['amount_column'])
    df = add_Debit_Credit_column(df, config['amount_column'])
    df = add_date_parts(df, config['date_column'])
    
    return df
