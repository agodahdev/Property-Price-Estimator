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

        # Left column - property type and location
        with col1:
            property_type = st.selectbox("Property Type", options=df['Property Type'].unique())
            county = st.selectbox("County", options=sorted(df['County'].unique()))
        
        # Right columb - property age and ownership type
        with col2:
            # User selects if property is newly built or older
            old_new = st.selectbox("Old/New Property", 
                                   options=df['Old/New'].unique())
            duration = st.selectbox("Duration",
                                    options=df['Duration'].unique())

        # When user clicks the predict button
        if st.button("Predict Price"):
            # Find properties that match the user's criteria
            similar_properties = df[
                (df['Property Type'] == property_type) &
                (df['County'] == county) &
                (df['Old/New'] == old_new)
            ]['Price']

            # If we found matching properties
            if len(similar_properties) > 0:
                # Calculate the average price of similar properties
                prediction = similar_properties.mean()
                st.success(f"Predicted Price: £{prediction:,.0f}")
                
                # Shows additional information about similar properties
                st.write("#### Similar Property Analysis")
                st.write(f"Found {len(similar_properties)} similar properties")
                st.write(f"Price range: £{similar_properties.min():,.0f} - £{similar_properties.max():,.0f}")
                st.write(f"Median price: £{similar_properties.median():,.0f}")
            else:
                # if no exact matches, show county average as back up
                county_avg = df[df['County'] == county]['Price'].mean()
                st.warning(f"No exact matches found. County average: £{county_avg:,.0f}")
    else:
        st.error("Error loading data for predictions")