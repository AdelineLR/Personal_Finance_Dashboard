# Author : Adeline Le Ray
# Date : 2025/05/28
# Project : Personal finance analysis
# Content : Function to categorize operations and define specific rules

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

    # # Custom specific rules (if true)
    # if specific_rules:
    #     for condition_mask, category in specific_rules:
    #         df.loc[condition_mask & (df['Category'] == 'Other'), 'Category'] = category

    return df

    
# def build_specific_rules_from_json(df, rules):
#     """
#     Builds specific rule-based masks for categorizing operations from a JSON list of rules.

#     Args:
#         df (pd.DataFrame): The cleaned DataFrame containing bank transactions.
#         rules (list of dict): List of rules (loaded from a JSON file), where each rule specifies:
#             - type: Type of rule ('date_range', 'regex', 'value_match')
#             - field: Column on which to apply the rule (for 'regex' and 'value_match')
#             - pattern or values: Pattern(s) to match
#             - amount: (Optional) Exact amount to match
#             - start/end: (For 'date_range') start and end dates in string format
#             - category: Category label to assign if rule matches

#     Returns:
#         list of tuples: Each tuple contains (boolean mask, category name)
#     """
#     specific_rules = []

#     for rule in rules:
#         category = rule.get("category", "Other")

#         if rule["type"] == "date_range":
#             start = pd.to_datetime(rule["start"])
#             end = pd.to_datetime(rule["end"])
#             mask = df["Date"].between(start, end)

#         elif rule["type"] == "regex":
#             mask = df[rule["field"]].str.contains(rule["pattern"], case=False, na=False, regex=True)

#         elif rule["type"] == "value_match":
#             values = rule['values']
#             if isinstance(values, str):
#                 values=[values]
#             mask = df[rule["field"]].str.contains('|'.join(map(re.escape,values)), case=False, na=False, regex=True)
#             if "amount" in rule:
#                 mask &= (df["Amount"] == rule["amount"])

#         else:
#             continue

#         specific_rules.append((mask, category))

#     return specific_rules
