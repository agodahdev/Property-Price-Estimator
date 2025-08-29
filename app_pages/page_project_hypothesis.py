import streamlit as st
import pandas as pd 
import plotly.express as px
from src.data_manager import load_small_dataset

# Display project hypothesis page
def page_project_hypothesis_body():
    st.write("### Project Hypothesis Validation")
    st.write("---")

    # Load the property data 
    df = load_small_dataset()
    if df is not None:

        # Test 1: Are London properties more expensive than other area?
        st.write("#### Hypothesis 1: London Properties Command Premium Prices")

        # Define which counties count as "London"
        london_counties = ['GREATER LONDON', 'LONDON']
        #Calculate average prices for London vs other areas
        london_data = df[df['County'].isin(london_counties)]['Price'].mean()
        other_data = df[~df['County'].isin(london_counties)]['Price'].mean()

        #Show the comparison in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("London Average", f"£{london_data:,.0f}")
        with col2:
            st.metric("Other Areas Average", f"£{other_data:,.0f}")
        
        #Calculate how much more expensive London is (as percentage)
        premium_percentage = ((london_data - other_data) / other_data) * 100

        # Check if London is at leaset 50% more expensive
        if premium_percentage > 50:
            st.success(f"VALIDATED: London properties are {premium_percentage:.0f}% more expensive")
        else:
            st.error(f"NOT VALIDATED: Only {premium_percentage:.0f}% difference")

        # Test 2: Are detached houses the most expensive property types?
        st.write("#### Hypothesis 2: Detached Houses are Most Expensive")

        # Calculate average price for each property type and sort from highest to lowest
        type_prices = df.groupby('Property Type')['Price'].mean().sort_values(ascending=False)

        # Create a bar chart to visualize the results
        fig = px.bar(x=type_prices.index, y=type_prices.values,
                    title="Average Price by Property Type")
        st.plotly_chart(fig)

        # Check if the most expensive type is "D" (Detached)
        if type_prices.index[0] == 'D':
            st.success("VALIDATED: Detached properties are most expensive")
        else:
            st.error("NOT VALIDATED: Different property type is most expensive")

        # Test 3: Do new properties cost more than old properties?
        st.write("#### Hypothesis 3: New Properties Command Higher Prices")

        # Calculate average prices for new vs old properties
        # 'Y = Yes (new), 'N' = No (old/existing)
        old_new_prices = df.groupby('Old/New')['Price'].mean()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("New Properties", f"£{old_new_prices.get('Y', 0):,.0f}")
        with col2:
            st.metric("Old Properties", f"£{old_new_prices.get('N', 0):,.0f}")

        # Check if new properties are more expensive than old 
        if old_new_prices.get('Y', 0) > old_new_prices.get('N', 0):
            st.success("VALIDATED: New properties are more expensive")
        else:
            st.error("NOT VALIDATED: Old properties are more expensive")
    else:
        st.error("Error loading data for hypothesis testing")