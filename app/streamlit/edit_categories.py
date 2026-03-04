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
        self.columns_to_display = [
            'Date', 
            'Month', 
            'Year', 
            'Details', 
            'Amount', 
            'Account', 
            'Category', 
            'Subcategory'
            ]
        self.columns_to_edit = [
            'New Subcategory'
            ]

    #---------------------------------------------------------------------------------------------------------------
    # Internal method to load config, data and rules into session state if not already loaded
    #---------------------------------------------------------------------------------------------------------------
    def _load_initial_state(self):
        """
        Load data, config and rules if not already in session state
        """
        # Load config
        if 'config' not in st.session_state :
            st.session_state.config = load_config()
        # Load data
        if 'data' not in st.session_state :                 
            st.session_state.data = load_existing_dataset(st.session_state.config)

        if 'rules' not in st.session_state :
            # Load rules file to get categories and subcategories
            st.session_state.rules = load_json(st.session_state.config['rules_file'])

        if 'current_df' not in st.session_state :
            # Filter data to keep only relevant columns for editing
            st.session_state.current_df = (
                st.session_state.data
                .loc[:, self.columns_to_display]
                .copy()
            )
            st.session_state.current_df['Date'] = st.session_state.current_df['Date'].dt.strftime('%Y-%m-%d')

            # Add columns to store modifications
            for col in ['New Subcategory', 'New Category']:
                if col not in st.session_state.current_df.columns:
                    st.session_state.current_df[col] = ''

    #---------------------------------------------------------------------------------------------------------------
    # Internal method to apply filters to the master dataframe and return the filtered dataframe for display
    #---------------------------------------------------------------------------------------------------------------
    def _apply_amount_filter(self, df, filter_str):
            """
            Apply numeric filtering on the Amount column.

            Accepted formats:
            - '>100'
            - '<50'
            - '10-200'
            - '150'

            Parameters
            ----------      
            df : pd.DataFrame
            filter_str : str          
            
            Returns
            -------
            pd.DataFrame
                Filtered dataframe based on the amount filter.
            """
            try:
                if filter_str.startswith('>'):
                    threshold = float(filter_str[1:])
                    return df[df['Amount'] > threshold]
                elif filter_str.startswith('<'):
                    threshold = float(filter_str[1:])
                    return df[df['Amount'] < threshold]
                # elif '-' in filter_str:
                #     low, high = map(float, filter_str.split('-'))
                #     return df[(df['Amount'] >= low) & (df['Amount'] <= high)]
                else:
                    value = float(filter_str)
                    return df[df['Amount'] == value]
            except ValueError:
                st.warning("Invalid amount filter format. Please use '>100', '<50', '10-200', or '150'.")
                return df

    #---------------------------------------------------------------------------------------------------------------
    # Internal method to apply filters to the master dataframe and return the filtered dataframe for display
    #---------------------------------------------------------------------------------------------------------------
    def _apply_filters(
        self,
        df,
        search_date,
        search_month,
        search_year,
        search_text,
        amount_filter,
        account,
        category,
        subcategory,
        filter_modified
        ):
        """
        Apply all UI filters to the master dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            The master dataframe stored in session_state.
        search_date : datetime.date or None
        search_month : int or None
        search_year : int or None
        search_text : str
        amount : str
             Examples: '50', '-50', '>100', '<100', '10-200'
        account : list
        category : list
        subcategory : list
        amount_filter : str
            Examples: '>100', '<50', '10-200'
        filter_modified : bool

        Returns
        -------
        pd.DataFrame
            Filtered dataframe (view only, does not modify master).
        """
        # Initiate df_filtered with all data
        df_filtered = df

        # Apply filters to the dataframe
        if search_date:
            df_filtered = df_filtered[
                df_filtered["Date"] == search_date
            ]
        if search_month:
            df_filtered = df_filtered[
                df_filtered["Month"] == search_month
            ]
        if search_year:
            df_filtered = df_filtered[
                df_filtered["Year"] == search_year
            ]       
        if search_text:
            df_filtered = df_filtered[
                df_filtered["Details"].str.contains(search_text, case=False, na=False)
            ]
        if amount_filter:
            df_filtered = self._apply_amount_filter(df_filtered, amount_filter)
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
        if filter_modified:
            df_filtered = df_filtered[
                df_filtered['New Subcategory'] != ''
            ]

        return df_filtered
    
    #---------------------------------------------------------------------------------------------------------------
    # Internal method to list subcategories from rules file
    #---------------------------------------------------------------------------------------------------------------
    def _list_categories(self,rules_file):
        """
        List all unique categories from the rules file.

        Parameters
        ----------
        rules_file : dict
            The rules loaded from the rules file, where keys are subcategories.
        
        Returns
        ------- 
        list
            Sorted list of unique subcategories, including 'other'.
        """
        subcat_list = set()
        for cat, _ in rules_file.items():
            subcat_list.add(cat)
            subcat_list.add('other')
        return sorted(subcat_list)

    #---------------------------------------------------------------------------------------------------------------
    #   Internal method to map subcategory to main category using rules file
    #---------------------------------------------------------------------------------------------------------------
    def _map_subcat_to_main(self, subcat):
        """
        Map a subcategory to its main category using the rules file.
        Parameters
        ----------
        subcat : str
            The subcategory to map.
        
        Returns
        -------
        str
            The main category corresponding to the subcategory.
        """
        if subcat in st.session_state.rules:
            return st.session_state.rules[subcat]['main_category']
        elif subcat == 'other':
            return 'other'
        else:
            return ''   

    #---------------------------------------------------------------------------------------------------------------
    # Internal method to apply modifications from the edited dataframe to the master dataframe in session state
    #---------------------------------------------------------------------------------------------------------------
    def _apply_modifications(self, edited_df):
        """
        Apply modifications from the edited dataframe to the master dataframe in session state.

        Parameters
        ----------
        edited_df : pd.DataFrame
            The dataframe returned by the data editor, containing user modifications.
        
        Returns
        -------
        None
        
        This method updates the master dataframe in session state with the modifications made by the user in the data editor.
        It checks for rows where the 'New Subcategory' column is not empty, maps the
        new subcategory to the main category, and updates the master dataframe accordingly.
        """
        # Filter only modified rows
        mask = edited_df['New Subcategory'] != ''
        df_modified = edited_df.loc[mask].copy()

        # If there are no modifications, show info message and return
        if df_modified.empty:
            st.info("No modifications to apply.")
            return
            
        # If there are modifications, map new subcategories to main categories and update the master dataframe
        if not df_modified.empty:
            df_modified['New Category'] = df_modified['New Subcategory'].map(self._map_subcat_to_main)
            st.session_state.current_df.update(df_modified)
            st.success("✅ Modifications applied !")

    #
    def _save_to_csv(self, test=False):
        """
        Save the modified dataframe to a CSV file.
        """
        try:
            if test:
                output_path = "data/processed/personal/final_data_test.csv"
            else:
                output_path = st.session_state.config['output_file']
            
            st.session_state.data.to_csv(output_path, index=False)
            st.success(f"✅ Data saved to {output_path}!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

    #---------------------------------------------------------------------------------------------------------------
    # Internal method to save modifications from the edited dataframe to the master dataframe in session state
    #---------------------------------------------------------------------------------------------------------------
    def _save_modifications(self):
        """
        Save modifications from the edited dataframe to the master dataframe in session state.
        Parameters
        ----------
        edited_df : pd.DataFrame
            The dataframe returned by the data editor, containing user modifications.
        Returns
        -------
        None
        """
        # Filter only modified rows
        mask = st.session_state.current_df['New Subcategory'] != ''
        df_modified = st.session_state.current_df.loc[mask].copy()

        if df_modified.empty:
            st.info("No modifications to save.")
            return

        # If there are modifications, update the master dataframe 
        if not df_modified.empty:
            df_modified['Category'] = df_modified['New Category']
            df_modified['Subcategory'] = df_modified['New Subcategory']

            # Update current dataframe with modifications
            st.session_state.current_df.update(df_modified)

            # Reset temp columns
            st.session_state.current_df.loc[mask, 'New Subcategory'] = ''
            st.session_state.current_df.loc[mask, 'New Category'] = ''

            # Update master dataframe with modifications
            st.session_state.data.update(df_modified)

            st.success("✅ Modifications saved!")

            self._save_to_csv(test=True)  # Save to test file to check before overwriting master file

    #---------------------------------------------------------------------------------------------------------------
    # Main method to run the page : display filters, editable dataframe and buttons to apply/save modifications
    #---------------------------------------------------------------------------------------------------------------
    def run(self):      
        st.title("✏️ Edit Categories")

        # Load data, config and rules if not already in session state
        self._load_initial_state()

        # Container for filters and data editor
        with st.container():
            # Initiate df_filtered with all data
            df_filtered = st.session_state.current_df
          
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write("Use the filters below to narrow down the transactions you want to edit. " \
                "Don't forget to click on 'Apply modifications' before changing filters ! " \
                "Click on 'Save modifications' to save the changes into master database.")
            with col2 :
                # Checkbox to filter only modified rows
                filter_modified = st.toggle("Filter modified rows")

            # Define filters : date, year, month, text search in details, account, category, subcategory
            col1, col2, col3, col4, col5, col6, col7 , col8= st.columns(8)
            with col1:
                search_date = st.date_input(
                    "Search by date",
                    value=None,
                    help="Filter transactions by date. Leave empty to show all."
                )
            
            with col2:
                search_month = st.selectbox(
                    "Search by month",
                    options=[None] + sorted(st.session_state.current_df["Month"].dropna().unique()),
                    help="Filter transactions by month. Leave empty to show all."
                )
            
            with col3:
                search_year = st.selectbox(
                    "Search by year",
                    options=[None] + sorted(st.session_state.current_df["Year"].dropna().unique()),
                    help="Filter transactions by year. Leave empty to show all."
                )

            with col4:
                search_text = st.text_input(
                    "Search in details",
                    placeholder="e.g. CARREFOUR, AUCHAN, ...",
                    help="Filter transactions by searching for specific text in the 'Details' column. Leave empty to show all."
                )

            with col5:
                amount = st.text_input(
                    "Search by amount",
                    placeholder="50, -50, >100, <100, ...",
                    help="Filter transactions by searching for specific amount in the 'Amount' column. Leave empty to show all."
                )
                
            with col6:
                account = st.multiselect(
                    "Search by account",
                    sorted(st.session_state.current_df["Account"].dropna().unique()),
                    help="Filter transactions by account. Leave empty to show all."
                )

            with col7:
                category = st.multiselect(
                    "Search by category",
                    sorted(st.session_state.current_df["Category"].dropna().unique()),
                    help="Filter transactions by category. Leave empty to show all."
                )

            with col8:
                # if a category is selected, filter corresponding subcategories
                if category != []:
                    subcat = sorted(
                        st.session_state.current_df[
                            st.session_state.current_df["Category"].isin(category)
                            ]["Subcategory"].dropna().unique()
                        )
                else:
                    subcat = sorted(st.session_state.current_df["Subcategory"].dropna().unique())

                subcategory = st.multiselect(
                    "Search by subcategory",
                    subcat,
                    help="Filter transactions by subcategory. Leave empty to show all."
                )                  

            # Apply filters to the dataframe
            df_filtered = self._apply_filters(
                st.session_state.current_df,
                search_date,
                search_month,
                search_year,
                search_text,
                amount,
                account,
                category,
                subcategory,
                filter_modified
            )
            
            # Create lists of all available subcategories
            subcat_list = self._list_categories(st.session_state.rules)
                             
            # Display editable dataframe : change only in "Subcategory" column, other columns are disabled
            edited_df = st.data_editor(
                df_filtered,
                column_config={
                    'New Subcategory': st.column_config.SelectboxColumn(
                        options=subcat_list
                    )
                },
                disabled = [
                    col for col in df_filtered.columns
                    if col not in self.columns_to_edit
                ],
                hide_index=True,
                key="category_editor"
            )    

           # Buttons to apply modifications to the current dataframe and save modifications to the master database
            cols = st.columns([6,1,1])
            with cols[1]:
                if st.button('Apply modifications', 
                             help="This will apply the changes you made in the table to the current dataframe. " \
                                  "You can then save all modifications by clicking on 'Save modifications'. "\
                                  "Don't forget to click on 'Apply modifications' before changing filters, "\
                                  "otherwise your unsaved changes will be lost!"):
                    self._apply_modifications(edited_df)
                    
            with cols[2]:
                if st.button('Save modifications', 
                            help="This will save all the changes you made into the master database. "\
                                 "Make sure to click on 'Apply modifications' before to apply your changes "\
                                 "to the current dataframe, otherwise no change will be saved! "):
                    self._save_modifications()
                