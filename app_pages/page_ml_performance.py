import streamlit as st
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.express as px
from src.data_manager import load_small_dataset

def page_ml_performance_body():
    st.write("### ML Model Performance")
    st.write("---")

    # Load the property data
    df = load_small_dataset()
    if df is not None:
        
        # Step 1: Prepare the data for machine learning
        # Make a copy so we don't change the original data
        df_encoded = df.copy()

        # Convert text categories to numbers
        df_encoded['Property_Type_Encoded'] = pd.Categorical(df['Property Type']).codes
        df_encoded['County_Encoded'] = pd.Categorical(df['County']).codes

        # Step 2: Set Up features and target (what we want to predict)
        features = ['Property_Type_Encoded', 'County_Encoded']
        X = df_encoded[features] # Features data
        y = df_encoded['Price'] # Target data

        # Step 3: Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Step 4: Create and train the machine learning model
        rf = RandomForestRegressor(n_estimators=50, random_state=42)
        rf.fit(X_train, y_train) 

        # Step 5: Make predictions on both training and test data
        train_pred = rf.predict(X_train) # Predictions on training data
        test_pred = rf.predict(X_test)   # Predictions on test data

        # Step 6: Show model performance metrics in two columns
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Training Performance")

            # How well the model fits
            st.metric("R² Score", f"{r2_score(y_train, train_pred):.3f}")

            # MAE: Average prediction error
            st.metric("MAE", f"{mean_absolute_error(y_train, train_pred):,.0f}")
        
        with col2:
            st.write("#### Test Performance")

            #Test performance shows how well model works on new data (unseen)
            st.metric("R² Score", f"{r2_score(y_test, test_pred):.3f}")
            st.metric("MAE", f"{mean_absolute_error(y_test, test_pred):,.0f}")

        # Step 7: Create scatter plot to visualize prediction accuracy
        st.write("#### Actual vs Predicted Prices")
        
        fig = px.scatter(x=y_test, y=test_pred,
                        labels={'x': 'Actual Price', 'y': 'Predicted Price'},
                        title="Model Prediction Accuracy")
        st.plotly_chart(fig)
    
    else:
        st.error("Could not load data for ML performance analysis")