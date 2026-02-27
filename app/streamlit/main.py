import streamlit as st

from edit_categories import EditCategoriesPage

st.set_page_config(page_title="Bank Expense Analysis", 
                   layout="wide",
                   initial_sidebar_state="expanded")

# Création des pages avec navigation
edit_categories_page = st.Page("edit_categories.py", title="Editer les catégories", icon=":material/edit:")

pg = st.navigation([edit_categories_page])

pg.run()  

if pg == edit_categories_page:
    EditCategoriesPage().run()


