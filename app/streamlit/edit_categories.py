import streamlit as st
import pandas as pd

class EditCategoriesPage:
    def __init__(self):
        pass

    def run(self):
        # Load data function with caching
        @st.cache_data
        def load_data(file_path):
            return pd.read_csv(file_path)
        
        st.title("✏️ Edit Categories")
        data_file = 'data/processed/final_data.csv'
        
        df = load_data(data_file)

        # Display current categories
        st.dataframe(df, use_container_width=True)