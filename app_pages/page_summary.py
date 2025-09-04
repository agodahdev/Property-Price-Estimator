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

    # Updated project hyptheses section
    st.write("### Project Hypotheses")
    st.info("""
    **H1: Home Counties Command Premium Prices**
    *Revised from London-only hypothesis based on data findings*
    Wealthy areas around London (Surrey, Buckinghamshire, Hertfordshire) command premium prices due to London accessibility with larger properties.

    **H2: Detached Houses Are Most Expensive**
    Detached properties cost more than other property types due to space and privacy.

    **H3: New Properties Command Higher Prices**
    Newly built properties sell for premium prices compared to existing properties.
    """)

    # Add data limitation notice
    st.warning("""
    **Data Limitation:**
    - Analysis based on historical UK property data (1995-2017).
    - Results reflect established market patterns rather than current conditions.
    """)