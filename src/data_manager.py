import streamlit as st 
import pandas as pd 

# Load the pre-processed small dataset for fast performance
@st.cache_data
def load_small_dataset():
    try:
        df = pd.read_csv("inputs/datasets/collection/uk_housing_small.csv")
        return df
    except FileNotFoundError:
        st.error("Small dataset not found - please create it first")
        return None
