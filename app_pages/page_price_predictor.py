import streamlit as st
import pandas as pd 
from src.data_manager import load_small_dataset

# Display price prediction page
def page_price_predictor_body():
    st.write("### Property Price Predictor")
    st.write("---")
    
    # Load property data
    df = load_small_dataset()
    if df is not None: 
        st.write("#### Enter Property Details")

        col1,col2 = st.columns(2)

        with col1:
            property_type = st.selectbox("Property Type",
                                        options=df['Property Type'].unique())
            county = st.selectbox("County",
                                options==sorted(df['County'].unique()))

        with col2:
            old_new = st.selectbox("Old/New Property",
                                options=df['Old/New'].unique())
            duration = st.selectbox("Duration",
                                    options=df['Duration'].unique())
        
        if st.button("Predict Price"):
            similar_properties = df[
                (df['Property Type'] == property_type) &
                (df['County'] == county) &
                (df['Old/New'] == old_new)
            ]['Price']

            if len(similar_properties) > 0:
                prediction = similar_properties.mean()
                st.success(f"Predicted Price: £[prediction:,.0f]")

                st.write("#### Similar Property Analysis")
                st.write(f"Found {len(similar_properties)} similar properties")
                st.write(f"Price range: £{similar_properties.min():,.0f} - £{similar_properties.max():,.0f}")
                st.write(f"Median price: £{similar_properties.median():,.0f}")
        else:
                county_avg = df[df['County'] == county]['Price'].mean()
                st.warning(f"No exact matches found. County average: £{county_avg:,.0f}")
    else:
        st.error("Error loading data for predictions")