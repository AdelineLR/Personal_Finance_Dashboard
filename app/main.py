import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Bank Statement Analysis",
    layout="wide"
)

st.title("🧪 Streamlit test – Display DataFrame")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "processed" / "final_data.csv"
CAT_FILE = BASE_DIR / "data" / "reference" / "categories.json"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

def list_categories(path):
    with open(path, 'r') as file:
        categories = json.load(file)
    cat_list = set()
    subcat_list = set()
    for cat, details in categories.items():
        cat_list.add(details['main_category'])
        cat_list.add('other')
        subcat_list.add(cat)
        subcat_list.add('other')
    return sorted(cat_list), sorted(subcat_list)

# Load data
df = load_data(DATA_FILE)

# Create lists of categories and subcategories
cat_list, subcat_list = list_categories(CAT_FILE)

# Filters
col1, col2, col3  = st.columns(3)
with col1:
    search_text = st.text_input(
    "Search in details",
    placeholder="e.g. CARREFOUR, AMAZON, UBER..."
    )

with col2:
    account = st.multiselect(
        "Account",
        sorted(df["Account"].dropna().unique())
    )
with col3:
    category = st.multiselect(
        "Category",
        sorted(df["Category"].dropna().unique())
    )
df_filtered = df.copy()

if search_text:
    df_filtered = df_filtered[
        df_filtered["Details"]
        .str.contains(search_text, case=False, na=False)
    ]
if account:
    df_filtered = df_filtered[
        df_filtered["Account"]
        .isin(account)
        ]
if category:
    df_filtered = df_filtered[
        df_filtered["Category"]
        .isin(category)
    ]

# Display editable dataframe
edited_df = st.data_editor(
    df_filtered,
    column_config={
        'Category': st.column_config.SelectboxColumn(
            options=cat_list,
        ),
        'Subcategory': st.column_config.SelectboxColumn(
            options=subcat_list
        )
    },
    disabled = [
        col for col in df_filtered.columns 
        if col not in ['Category', 'Subcategory']
    ],
    hide_index=True
)
