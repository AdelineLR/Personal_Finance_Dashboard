# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Functions to clean bank data

import pandas as pd
import os

def drop_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Drop columns with only NaN values. """
    na_col = df.columns[df.isna().sum() == len(df)].tolist()
    return df.drop(columns=na_col)

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """ Drop duplicates operations. """
    return df.drop_duplicates(ignore_index=True)

def rename_columns(df: pd.DataFrame, new_names: list) -> pd.DataFrame:
    """ Rename dataframe columns. """
    df.columns = new_names
    return df

def convert_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """ Convert a string column to datetime (day-first format). """
    df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')
    return df

def convert_amount_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Replace comma with dot in a string amount column and convert to float.
    """
    df[column] = df[column].str.replace(',', '.', regex=False).astype(float)
    return df

def add_Debit_Credit_column(df: pd.DataFrame, amount_column: str, new_column='Debit/Credit') -> pd.DataFrame:
    """ Create a new column to indicate if the operation is a debit or credit. """
    df[new_column] = 'Debit'
    df.loc[df[amount_column] > 0, new_column] = 'Credit'
    return df

def add_date_parts(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """ Add 'Month' and 'Year' columns from a date column. """
    df['Month'] = df[date_column].dt.month
    df['Year'] = df[date_column].dt.year
    return df

def add_currency_column(df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """ Add 'Currency' column. """
    df['Currency'] = currency
    return df

def clean_bank_data(df_raw : pd.DataFrame, config : dict) -> pd.DataFrame:
    """
    Perform full cleaning pipeline on raw bank statement data.
    
    Returns a cleaned DataFrame with:
    - Drop empty columns
    - Rename columns
    - Convert date and amount fields
    - Add debit/credit classification
    - Extract month and year
    """
    df = df_raw.copy()
    df = drop_empty_columns(df)
    df = drop_duplicates(df)
    df = rename_columns(df, config['rename_columns'])
    df = add_currency_column(df, config['currency'])
    df = convert_date_column(df, config['date_column'])
    df = convert_amount_column(df, config['amount_column'])
    df = add_Debit_Credit_column(df, config['amount_column'])
    df = add_date_parts(df, config['date_column'])
    
    return df
