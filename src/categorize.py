# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Function to categorize operations in a DataFrame using regex-based matching.

import pandas as pd
import re

def categorize_operations(df, operation_col, category_rules=None):
    """
    Categorizes operations in a DataFrame using:
      - Regular expression matching (category_rules)

    Args:
        df (pd.DataFrame): Input DataFrame containing transaction data.
        operation_col (str): Column name containing operation descriptions.
        category_rules (dict): Dictionary {category: [regex patterns]} for regex-based matching.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with a new 'Category' and 'Subcategory' column added.
    """
    df = df.copy()

    # Initialize new columns
    df['Category'] = 'other'  # Default value
    df['Subcategory'] = 'other'  # Default value
    df['is_manual'] = False  # Default value

    # Regex match rules 
    if category_rules:
        for category, details in category_rules.items():
            pattern = '|'.join(details['patterns'])
            mask = df[operation_col].str.contains(pattern, case=False, na=False)
            df.loc[mask, 'Subcategory'] = category
            df.loc[mask, 'Category'] = details['main_category']

    return df

    
