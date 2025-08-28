import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Display property analysis page
def page_property_analysis_body():
    st.write("### Property Data Analysis")
    st.write("---")

    try:
        df = pd.read_csv("inputs/datasets/collection/uk_housing_clean.csv")
        
        # Sample the datat to prevent browser overload
        df = df.sample(n=5000, random_state=42)
        st.info(f"Analyzing sample of {len(df):,} properties")


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

    except Exception as e:
        st.error(f"Error loading data: {e}") 