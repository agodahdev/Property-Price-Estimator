import streamlit as st
import pandas as pd
from src.data_manager import load_small_dataset

# Display project summary page
def page_summary_body():
    st.write('### UK Property Price Predictor')
    st.write("---")

    # Project overview
    st.write("#### Project Overview")
    st.info("Analyzing UK Property data to predict house prices using machine learning")

    # Business requirements
    st.write("#### Business Requirements")
    st.success("""
    **BR1:** Analyze UK property characteristics and price patterns
    **BR2:** Build ML model to predict property values
    """
    )

    # Dataset summary with real data
    st.write("#### Dataset Summary")

    df = load_small_dataset()
    if df is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Properties", f"{df.shape[0]:,}")
            st.metric("Average Price", f"£{df['Price'].mean():,.0f}")
        
        with col2:
            st.metric("Date Range", f"{df['Date of Transfer'].min()[:4]} - {df['Date of Transfer'].max()[:4]}")
            st.metric("Property Types", df['Property Type'].nunique())
        
    else:
        st.warning("Dataset not loaded yet")