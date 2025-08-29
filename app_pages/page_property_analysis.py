import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from src.data_manager import load_small_dataset

# Display property analysis page
def page_property_analysis_body():
    st.write("### Property Data Analysis")
    st.write("---")

    # Load small dataset
    df = load_small_dataset()
    if df is not None:
        st.info(f"Analyzing {len(df):,} properties")

        # Property Type Distribution
        st.write("#### Property Type Distribution")
        fig1 = px.bar(df['Property Type'].value_counts(),
                    title="Number of Properties by Type")
        st.plotly_chart(fig1) 

        # Price Distribution 
        st.write("#### Price Distribution")
        fig2 = px.histogram(df, x='Price', nbins=50,
                            title="UK Property Price Distribution")
        st.plotly_chart(fig2)

        # Price by Property Type
        st.write("#### Average Price by Property Type")
        price_by_type = df.groupby('Property Type')['Price'].mean().sort_values(ascending=False)
        fig3 = px.bar(x=price_by_type.index, y=price_by_type.values,
                      title="Average Price by Property Type")
        st.plotly_chart(fig3)

        # County Analysis
        st.write("#### Top 10 Most Expensive Counties")
        county_prices = df.groupby('County')['Price'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(county_prices)

    else:
        st.error(f"Error loading data") 