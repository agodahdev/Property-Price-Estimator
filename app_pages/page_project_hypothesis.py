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

        st.info("**Data Period:** Analysis based on UK property transactions 1995-2017")

        # Hypothesis 1: Revised based on data reality
        st.write("#### Hypothesis 1: Home Counties Command Premium Prices")
        st.write("*Revised from original London-only hypothesis based on data findings*")

        # Quality filtering
        min_properties = 100
        county_stats = df.groupby('County').agg({
            'Price': ['count', 'median']
        }).round(0)
        county_stats.columns = ['Property_Count', 'Median_Price']
        county_stats = county_stats.reset_index()

        valid_counties = county_stats[county_stats['Property_Count'] >= min_properties]

        # Define Home Counties (wealthy areas around London)
        home_counties = ['SURREY', 'BUCKINGHAMSHIRE', 'HERTFORDSHIRE', 'GREATER LONDON', 'BERKSHIRE']
        home_counties_data = valid_counties[valid_counties['County'].isin(home_counties)]

        # Compare to other regions
        other_regions = valid_counties[~valid_counties['County'].isin(home_counties)]

        if len(home_counties_data) > 0 and len(other_regions) > 0:
            home_counties_median = home_counties_data['Median_Price'].mean()
            other_regions_median = other_regions['Median_Price'].mean()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Home Counties Average", f"£{home_counties_median:,.0f}")
            with col2:
                st.metric("Other Regions Average", f"£{other_regions_median:,.0f}")

            premium_percentage = ((home_counties_median - other_regions_median) / other_regions_median) * 100

            if premium_percentage > 30:
                st.success(f"VALIDATED: Home Counties are {premium_percentage:.0f}% more expensive than other regions")
            else:
                st.warning(f"PARTIALLY VALIDATED: Home Counties premium is {premium_percentage:.0f}%")
            
            # Show Home Counties breakdown
            st.write("**Home Counties Individual Analysis:**")
            home_counties_display = home_counties_data.sort_values('Median_Price', ascending=False)
            for _, row in home_counties_display.iterrows():
                st.write(f"- {row['County']}: £{row['Median_Price']:,.0f} ({row['Property_Count']} properties)")

            st.info("""
            **Revised Hypothesis Rationale:**
            Original data showed Surrey and Buckinghamshire as most expensive, not Greater London alone.
            This led to recognizing that wealth extends beyond London city boundaries into surrounding 
            affluent "Home Counties" that offer larger properties with London accessibility.
            """)
        
        # Hypothesis 2: Property type analysis
        st.write("#### Hypothesis 2: Detached Houses Are Most Expensive")

        type_analysis = df.groupby('Property Type').agg({
            'Price': ['count', 'median']
        }).round(0)
        type_analysis.columns = ['Count', 'Median_Price']
        type_analysis = type_analysis.reset_index()

        # Filter property types with sufficient data
        valid_types = type_analysis[type_analysis['Count'] >= 100]

        if len(valid_types) > 0:
            type_prices_sorted = valid_types.sort_values('Median_Price', ascending=False)

            fig = px.bar(type_prices_sorted,
                        x='Property Type',
                        y='Median_Price',
                        title="Property Types by Median Price",
                        hover_data={'Count': True},
                        labels={'Median_Price': 'Median Price (£)'})
            st.plotly_chart(fig)

            most_expensive_type = type_prices_sorted.iloc[0]['Property Type']
            most_expensive_price = type_prices_sorted.iloc[0]['Median_Price']

            if most_expensive_type == 'D':
                st.success("VALIDATED: Detached properties (D) are most expensive")
            else:
                type_name = {'S': 'Semi-detached', 'T': 'Terraced', 'F': 'Flats', 'O': 'Other'}.get(most_expensive_type, most_expensive_type)
                st.error(f"NOT VALIDATED: {type_name} properties ({most_expensive_type}) are most expensive at £{most_expensive_price:,.0f}")

            # Show all property type results
            st.write("**Property Type Breakdown:**")
            for _, row in type_prices_sorted.iterrows():
                type_name = {'D': 'Detached', 'S': 'Semi-detached', 'T': 'Terraced', 'F': 'Flats', 'O': 'Other'}.get(row['Property Type'], row['Property Type'])
                st.write(f"- {type_name}: £{row['Median_Price']:,.0f} ({row['Count']:,} properties)")

        # Hypothesis 3: New vs old properties
        st.write("#### Hypothesis 3: New Properties Command Higher Prices")

        old_new_analysis = df.groupby('Old/New').agg({
            'Price': ['count', 'median']
        }).round(0)
        old_new_analysis.columns = ['Count', 'Median_Price']
        old_new_analysis = old_new_analysis.reset_index()

        new_data = old_new_analysis[old_new_analysis['Old/New'] == 'Y']
        old_data = old_new_analysis[old_new_analysis['Old/New'] == 'N']

        if len(new_data) > 0 and len(old_data) > 0:
            new_median = new_data['Median_Price'].iloc[0]
            old_median = old_data['Median_Price'].iloc[0]
            new_count = new_data['Count'].iloc[0]
            old_count = old_data['Count'].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("New Properties", f"£{new_median:,.0f}")
            with col2:
                st.metric("Existing Properties", f"£{old_median:,.0f}")
            
            if new_median > old_median:
                premium_percentage = ((new_median - old_median) / old_median) * 100
                st.success(f"VALIDATED: New properties are {premium_percentage:.1f}% more expensive")
            else:
                discount_percentage = ((old_median - new_median) / old_median) * 100
                st.error(f"NOT VALIDATED: New properties are {discount_percentage:.1f}% LESS expensive")
            
            st.write(f"**Sample sizes:** New properties: {new_count:,}, Existing properties: {old_count:,}")

        # Summary of findings
        st.write("#### Hypothesis Validation Summary")

        # Calculate validation results for summary
        validation_results = []

        # Check Home Counties validation
        if len(home_counties_data) > 0 and len(other_regions) > 0:
            home_premium = ((home_counties_median - other_regions_median) / other_regions_median) * 100
            if home_premium > 30:
                validation_results.append("✅ Home Counties premium validated")
            else:
                validation_results.append("⚠️ Home Counties premium partially validated")

        # Check property type validation
        if len(valid_types) > 0:
            most_expensive = type_prices_sorted.iloc[0]['Property Type']
            if most_expensive == 'D':
                validation_results.append("✅ Detached houses most expensive validated")
            else:
                validation_results.append("❌ Detached houses hypothesis not validated")
        
        # Check new vs old validation
        if len(new_data) > 0 and len(old_data) > 0:
            if new_median > old_median:
                validation_results.append("✅ New properties premium validated")
            else:
                validation_results.append("❌ New properties premium not validated")
        
        # Display summary 
        if validation_results:
           st.success("**Final Results:**")
           for result in validation_results:
               st.write(result)

        st.info("""
         **Key Learning:** Data-driven analysis led to hypothesis revision and more accurate understanding
         of UK property market patterns. The Home Counties finding reflects real market dynamics where
         wealth extends beyond city boundaries into surrounding premium areas.
        """)

    else:
        st.error("Error loading data for hypothesis testing")