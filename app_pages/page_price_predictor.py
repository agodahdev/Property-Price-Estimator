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
        st.info("Fill in the property characteristics below to get a price prediction based on similar UK properties")

        col1, col2 = st.columns(2)

        # Left column - property type and location
        with col1:
            property_type = st.selectbox("Property Type", options=df['Property Type'].unique(),
                                        help="D=Detached, S=Semi-detached, T=Terraced, F=Flat")
            county = st.selectbox("County", options=sorted(df['County'].unique()),
                                help="Select the county where your property is located")
        
        # Right column - property age and ownership type
        with col2:
            # User selects if property is newly built or older
            old_new = st.selectbox("Old/New Property", 
                                   options=df['Old/New'].unique(),
                                   format_func=lambda x: "New Build" if x == "Y" else "Existing Property",
                                   help="Y=New Build, N=Existing Property")

            # User selects property tenure (ownership type)
            duration_mapping = {'F': 'Freehold', 'L': 'Leasehold'}
            duraration_options = [duration_mapping.get(d,d) for d in df['Duration'].unique()]

            duration_display = st.selectbox("Property Tenure",
                                            options=duraration_options,
                                            help="Freehold: Own property & land permanently. Leashold: Own for fixed period")

            duration = 'F' if duration_display == 'Freehold' else 'L'

        # Information box about tenure types 
        st.info("""
        **Tenure Types Explained:**
        - **Freehold**: You own the property and land permanently (typical for houses).
        - **Leasehold**: You own the property for a fixed period, usually 99-999 years.
        """)

        # When user clicks the predict button
        if st.button("Predict Price", type="primary"):
            # Find properties that match the user's criteria
            similar_properties = df[
                (df['Property Type'] == property_type) &
                (df['County'] == county) &
                (df['Old/New'] == old_new) &
                (df['Duration'] == duration)
            ]['Price']

            # If we found matching properties
            if len(similar_properties) > 0:
                # Calculate the average price of similar properties
                prediction = similar_properties.mean()

                st.success(f"Predicted Price: £{prediction:,.0f}")
                
                # Shows additional information about similar properties
                st.write("#### Similar Property Analysis")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Properties Found",len(similar_properties))
                with col2:
                    st.metric(f"Median price", f"£{similar_properties.median():,.0f}")
                with col3:                   
                    st.metric(f"Price range", f"£{similar_properties.min():,.0f} - £{similar_properties.max():,.0f}")
                
                st.write(f"**Price Range:** £{similar_properties.min():,.0f} - £{similar_properties.max():,.0f}")

                if len(similar_properties) > 50:
                    st.success("High confidence prediction (50+ similar properties)")
                elif len(similar_properties) >= 20:
                    st.warning("Medium confidence prediction (20+ simila properties)")
                else:
                    st.warning("Lower confidence prediction (fewer than 20 similar properties)")

            else:
                # if no exact matches, show fallback option
                st.warning(f"No properties found with exact matching criteria")

                fallback_properties = df[
                    (df['Property Type'] == property_type) &
                    (df['County'] == county)
                ]['Price']

                if len(fallback_properties) > 0:
                    fallback_avg = fallback_properties.mean()
                    st.info(f"** Alternative estimate based on {len(fallback_properties)} similar properties in {county}:** £{fallback_avg:,.0f}")
                else:
                    county_avg = df[df['County'] == county]['Price'].mean()
                    st.info(f"County average for {county}:** £{county_avg:,.0f}")

        st.write("#### How this works")
        st.write("""
        This predictor analyzes similar properties in our database and calculates the average price. 
        The prediction accuracy depends on:
        - Number of similar properties found
        - How closely they match your criteria
        - Regional market conditions
        
        **Note:** This is an estimate based on historical data and should not be used as the sole basis for property decisions.
        
        """)   
    else:
        st.error("Error loading data for predictions")