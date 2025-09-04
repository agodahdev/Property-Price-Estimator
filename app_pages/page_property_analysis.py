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
        st.info(f"Analyzing {len(df):,} properties from UK housing market")

        # Chart 1: Show how many of each property type we have
        st.write("#### Property Type Distribution")
        st.write("This shows how many houses, flats, and other property types are in our data")

        property_counts = df['Property Type'].value_counts()
        fig1 = px.bar(x=property_counts.index,
                     y=property_counts.values,
                     title="Number of Properties by Type",
                     labels={'x': 'Property Type', 'y': 'Count'})
        st.plotly_chart(fig1)

        # Explain what the letters mean
        st.info("""
        **Property Type Codes:**
        - D = Detached houses (stand alone)
        - S = Semi-detached houses (joined to one other house)
        - T = Terraced houses (joined to houses on both sides)
        - F = Flats/apartments
        - O = Other types
        """)

        # Chart 2: Show the spread of property prices
        st.write("#### Price Distribution")
        st.write("This shows how UK property prices are spread out - most houses cost a certain amount, with fewer very cheap or very expensive ones")

        fig2 = px.histogram(df, x='Price', nbins=50,
                            title="UK Property Price Distribution")
        fig2.update_layout(xaxis_title="Price (£)", yaxis_title="Number of Properties")
        st.plotly_chart(fig2)

        # Chart 3: Compare average prices by property type
        st.write("#### Average Price by Property Type")
        st.write("This shows which types of properties cost the most on average")

        price_by_type = df.groupby('Property Type')['Price'].mean().sort_values(ascending=False)
        fig3 = px.bar(x=price_by_type.index, y=price_by_type.values,
                      title="Average Price by Property Type",
                      labels={'x': 'Property Type', 'y': 'Average Price (£)'})
        st.plotly_chart(fig3)

        # Chart 4: County analysis with better data quality
        st.write("#### Most Expensive Counties (Reliable Analysis)")
        st.write("This shows which UK counties have the highest property prices, using only counties with enough data to be reliable")

        # Apply filtering to get reliable results
        min_properties = 100  # Only look at counties with lots of properties

        # Calculate detailed statistics for each county
        county_stats = df.groupby('County').agg({
            'Price': ['count', 'mean', 'median', 'std', 'min', 'max']
        }).round(0)

        # Make column names easier to work with
        county_stats.columns = ['Property_Count', 'Mean_Price', 'Median_Price', 'Price_StdDev', 'Min_Price', 'Max_Price']
        county_stats = county_stats.reset_index()

        # Filter out counties with unreliable data
        valid_counties = county_stats[
             (county_stats['Property_Count'] >= min_properties) &      # Must have enough properties
             (county_stats['Mean_Price'] >= 50000) &                   # Exclude unrealistic low prices
             (county_stats['Mean_Price'] <= 3000000) &
             (county_stats['Price_StdDev'] / county_stats['Mean_Price'] <= 2.0)  # Exclude counties with wild price swings
        ].copy()

        if len(valid_counties) > 0:
            # Use median prices (middle value) instead of average to avoid being fooled by super-expensive outliers
            top_counties = valid_counties.sort_values('Median_Price', ascending=False).head(10)

            # Create the chart
            fig4 = px.bar(top_counties,
                         x='County',
                         y='Median_Price',
                         title=f"Top 10 Counties by Median Price (At least {min_properties} properties each)",    
                         labels={'Median_Price': 'Median Price (£)', 'County': 'County'},
                         hover_data={
                             'Property_Count': True,
                             'Mean_Price': ':,.0f',
                             'Median_Price': ':,.0f'
            })
            fig4.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_tickangle=45)
            st.plotly_chart(fig4)

            # Explain what we did to make this reliable
            st.success(f"""
            **Why This Analysis Is Reliable:**
            - Only showing counties with {min_properties}+ properties (enough data for good averages)
            - Using median prices instead of averages (not fooled by super-expensive outliers)
            - Removed counties with unrealistic or inconsistent price data
            - {len(valid_counties)} counties met our quality standards out of {df['County'].nunique()} total
            """)

            # Show the detailed numbers in a table
            st.write("#### Detailed County Results")
            display_counties = top_counties[['County', 'Property_Count', 'Median_Price', 'Mean_Price']].copy()
            display_counties['Median_Price'] = display_counties['Median_Price'].apply(lambda x: f"£{x:,.0f}")
            display_counties['Mean_Price'] = display_counties['Mean_Price'].apply(lambda x: f"£{x:,.0f}")
            display_counties.columns = ['County', 'Number of Properties', 'Median Price', 'Average Price']
            st.dataframe(display_counties, use_container_width=True)

            # Investigate why certain counties are most expensive
            st.write("#### Understanding the Results")
            st.write("Let's look at why these counties are the most expensive:")

            # Show detailed breakdown of top 3 counties
            top_3_counties = top_counties.head(3)

            for idx, county_info in top_3_counties.iterrows():
                county_name = county_info['County']
                county_properties = df[df['County'] == county_name]

                st.write(f"**{county_name}:**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Properties analyzed: {county_info['Property_Count']:,}")
                with col2:
                    st.write(f"Price range: £{county_info['Min_Price']:,.0f} - £{county_info['Max_Price']:,.0f}")
                with col3:
                    price_variation = (county_info['Price_StdDev'] / county_info['Mean_Price']) * 100
                    st.write(f"Price variation: {price_variation:.0f}%")

                # Show what types of properties are in this county
                type_breakdown = county_properties['Property Type'].value_counts()
                type_percentages = (type_breakdown / len(county_properties) * 100).round(1)

                property_mix = []
                for prop_type, percentage in type_percentages.items():
                    type_name = {'D': 'Detached', 'S': 'Semi-detached', 'T': 'Terraced', 'F': 'Flats', 'O': 'Other'}.get(prop_type, prop_type)
                    property_mix.append(f"{type_name}: {percentage}%")
                
                st.write(f"Property mix: {', '.join(property_mix)}")
                st.write("---")

            # Explain why these results make sense
            st.info("""
            **Why Surrey and Buckinghamshire Are Expensive:**
            - These are "Home Counties" - wealthy areas near London
            - People can live there and commute to high-paying London jobs
            - Larger properties with more space than central London
            - Historically affluent areas with high demand
            - Good schools and amenities attract wealthy families
             """)

            # Address the London hypothesis issue
            st.write("#### What This Means for Our London Hypothesis")
            if top_counties.iloc[0]['County'] != 'GREATER LONDON':
                st.warning("""
                **Important Finding:** Greater London is not the most expensive county in our data.

                **Possible Explanations:**
                1. **Home Counties Effect**: Wealthy areas around London (like Surrey, Buckinghamshire)
                   offer larger properties for similar money
                2. **Data Coverage**: Our sample might not capture the most expensive London areas
                3. **Property Size Factor**: London flats might be smaller and cheaper than large 
                   Home Counties houses
                4. **Historical Data**: This data is from 1995-2017, market patterns may have changed

                This doesn't invalidate our analysis - it shows that wealth extends beyond London 
                city boundaries into surrounding affluent areas.
                """)
            
            # Show how many counties we had to exclude
            excluded_counties = df['County'].nunique() - len(valid_counties)
            if excluded_counties > 0:
                st.warning(f"""
                **Data Quality Information:**
                We excluded {excluded_counties} counties from this analysis because they had:
                - Too few properties (less than {min_properties}) for reliable averages
                - Extreme price variations suggesting data quality problems
                - Unrealistic price ranges indicating possible data errors

                This filtering gives us more trustworthy and meaningful results.
                """)

            else:
                st.error("No counties have enough reliable data for meaningful analysis.")

            # Summary of what we learned
            st.write("#### Key Insights from Property Analysis")
            st.success("""
            **What We Discovered:**
            1. **Property Types**: The data shows the mix of different property types in the UK market
            2. **Price Distribution**: Most properties fall within a typical price range, with fewer very expensive outliers
            3. **Type Pricing**: Different property types have notably different average prices
            4. **Regional Variations**: Significant price differences exist between UK counties
            5. **Data Quality Matters**: Filtering out unreliable data gives much better insights
            

            **Business Value:** This analysis helps estate agents, investors, and buyers understand 
            market patterns and make more informed property decisions.
            """)


    else:
        st.error(f"Error loading data") 


