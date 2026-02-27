import streamlit as st
import pandas as pd
import json
from pathlib import Path
import os
from src.config_loader import load_config
from src.run_pipeline import load_existing_dataset
from src.io_utils import load_json

class EditCategoriesPage:
    def __init__(self):
        pass

    def run(self):      
        st.title("✏️ Edit Categories")

        # Function to list categories and subcategories from rules file
        @st.cache_data
        def list_categories(rules_file):
            cat_list = set()
            subcat_list = set()
            for cat, details in rules_file.items():
                cat_list.add(details['main_category'])
                cat_list.add('other')
                subcat_list.add(cat)
                subcat_list.add('other')
            return sorted(cat_list), sorted(subcat_list)

        # Build mapping from main categories to their subcategories using rules file
        @st.cache_data
        def build_main_to_subs(rules):
            mapping = {}
            for subcat, details in rules.items():
                main = details.get("main_category")
                if main not in mapping:
                    mapping[main] = []
                mapping[main].append(subcat)
            return mapping

        # Load data, config and rules if not already in session state
        if 'data' not in st.session_state or 'config' not in st.session_state or 'rules' not in st.session_state:
            # Load config
            st.session_state.config = load_config()
            # Load data
            st.session_state.data = load_existing_dataset(st.session_state.config)
            # Load categories
            st.session_state.rules = load_json(st.session_state.config['rules_file'])

        # Create lists of all available main categories and subcategories
        main_to_subs = build_main_to_subs(st.session_state.rules)   
        cat_list, subcat_list = list_categories(st.session_state.rules)

        # Filters
        col1, col2, col3, col4  = st.columns(4)
        with col1:
            search_text = st.text_input(
            "Search in details",
            placeholder="e.g. CARREFOUR, AUCHAN, ..."
            )

        with col2:
            account = st.multiselect(
                "Account",
                sorted(st.session_state.data["Account"].dropna().unique())
            )
        with col3:
            category = st.multiselect(
                "Category",
                sorted(st.session_state.data["Category"].dropna().unique())
            )
        with col4:
            # if a category is selected, filter corresponding subcategories
            if category != []:
                subcat = sorted(
                    st.session_state.data[
                        st.session_state.data["Category"].isin(category)
                        ]["Subcategory"].dropna().unique()
                    )
            else:
                subcat = sorted(st.session_state.data["Subcategory"].dropna().unique())

            subcategory = st.multiselect(
                "Subcategory",
                subcat
            )
        
        # Keep current version of df in session state to track changes
        if 'current_df' not in st.session_state:
            st.session_state.current_df = st.session_state.data.copy()

        df_filtered = st.session_state.current_df

        if search_text:
            df_filtered = df_filtered[
                df_filtered["Details"]
                .str.contains(search_text, case=False, na=False)
            ]
        if account:
            df_filtered = df_filtered[
                df_filtered["Account"].isin(account)
                ]
        if category:
            df_filtered = df_filtered[
                df_filtered["Category"].isin(category)
            ]
        if subcategory:
            df_filtered = df_filtered[
                df_filtered["Subcategory"].isin(subcategory)
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
