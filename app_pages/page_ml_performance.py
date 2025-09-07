import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import plotly.express as px
import plotly.graph_objects as go
from src.data_manager import load_small_dataset

def page_ml_performance_body():
    st.write("### ML Model Performance Metrics")
    st.write("---")
    
    # Load our property data
    df = load_small_dataset()
    if df is not None:
        
        # Step 1: Clean the data
        st.write("#### 1. Data Preparation")
        original_count = len(df)
        
        # Remove very cheap and very expensive houses
        df_clean = df[(df['Price'] > 50000) & (df['Price'] < 1000000)].copy()
        removed = original_count - len(df_clean)
        
        # Show how many properties we're using
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Data", f"{original_count:,} properties")
        with col2:
            st.metric("After Cleaning", f"{len(df_clean):,} properties")
        with col3:
            st.metric("Outliers Removed", f"{removed:,} properties")
        
        # Step 2: Create new features from existing data
        st.write("#### 2. Feature Engineering")
        
        df_encoded = df_clean.copy()
        
        # Convert text to numbers so computer can understand
        df_encoded['Property_Type_Encoded'] = pd.Categorical(df_clean['Property Type']).codes
        df_encoded['County_Encoded'] = pd.Categorical(df_clean['County']).codes
        df_encoded['Old_New_Encoded'] = pd.Categorical(df_clean['Old/New']).codes
        df_encoded['Duration_Encoded'] = pd.Categorical(df_clean['Duration']).codes
        
        st.write("**Creating new features to help prediction...**")
        
        # Combine property type and age (new terraced vs old terraced might differ)
        df_encoded['Type_Age_Interaction'] = (
            df_encoded['Property_Type_Encoded'] * df_encoded['Old_New_Encoded']
        )
        
        # Group counties by how expensive they are
        county_avg_price = df_clean.groupby('County')['Price'].mean()
        df_encoded['County_Price_Tier'] = df_clean['County'].map(
            lambda x: 0 if county_avg_price[x] < 250000 else 
                     (1 if county_avg_price[x] < 400000 else 2)
        )
        
        # How common is each property type (rare types might cost more)
        type_frequency = df_clean['Property Type'].value_counts(normalize=True)
        df_encoded['Type_Rarity'] = df_clean['Property Type'].map(type_frequency)
        
        # Show what features we created
        feature_types = {
            'Original Features': ['Property Type', 'County', 'Old/New', 'Duration'],
            'Interaction Features': ['Type × Age'],
            'Derived Features': ['County Price Tier', 'Type Rarity']
        }
        
        feature_df = pd.DataFrame([
            {'Category': cat, 'Features': ', '.join(feats), 'Count': len(feats)}
            for cat, feats in feature_types.items()
        ])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(feature_df, use_container_width=True, hide_index=True)
        with col2:
            st.metric("Total Features", "7", delta="+3 new features")
        
        # List all features we'll use
        features = [
            'Property_Type_Encoded', 'County_Encoded', 'Old_New_Encoded', 
            'Duration_Encoded', 'Type_Age_Interaction', 'County_Price_Tier', 
            'Type_Rarity'
        ]
        X = df_encoded[features]  # Features (what we know)
        y = df_encoded['Price']   # Target (what we want to predict)
        
        # Split data - 80% for training, 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Step 3: Try different models to see which works best
        st.write("#### 3. Model Comparison")
        
        # Create 4 different models to test
        models = {
            'Linear Regression': LinearRegression(),  # Simplest model
            'Decision Tree': DecisionTreeRegressor(max_depth=10, random_state=42),  # Tree-based
            'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),  # Many trees
            'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=10)  # Looks at similar properties
        }
        
        # Show progress while training
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Store results for each model
        model_results = {}
        best_model = None
        best_score = -float('inf')
        
        # Train each model and see how well it works
        for i, (name, model) in enumerate(models.items()):
            status_text.text(f'Training {name}...')
            progress_bar.progress((i + 1) / len(models))
            
            # Train the model on training data
            model.fit(X_train, y_train)
            
            # Make predictions
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            # Check how good predictions are
            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)
            test_mae = mean_absolute_error(y_test, test_pred)
            
            # Test model 5 times to make sure it's stable
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                       scoring='r2', n_jobs=-1)
            
            # Save all results
            model_results[name] = {
                'Train R²': train_r2,
                'Test R²': test_r2,
                'CV R² (mean)': cv_scores.mean(),
                'CV R² (std)': cv_scores.std(),
                'MAE': test_mae,
                'model': model,
                'predictions': test_pred
            }
            
            # Remember which model is best
            if test_r2 > best_score:
                best_score = test_r2
                best_model = name
        
        # Clear progress bar
        progress_bar.empty()
        status_text.empty()
        
        # Show results
        st.write("**Performance Metrics Comparison:**")
        
        # Make a table of results
        comparison_df = pd.DataFrame({
            name: {
                'Train R²': f"{results['Train R²']:.3f}",
                'Test R²': f"{results['Test R²']:.3f}",
                'CV R²': f"{results['CV R² (mean)']:.3f} ± {results['CV R² (std)']:.3f}",
                'MAE': f"£{results['MAE']:,.0f}"
            }
            for name, results in model_results.items()
        }).T
        
        # Show which model won
        st.success(f"🏆 **Best Model: {best_model}** (Test R² = {best_score:.3f})")
        
        # Display table with best model highlighted
        st.dataframe(
            comparison_df.style.highlight_max(subset=['Test R²'], color='lightgreen'),
            use_container_width=True
        )
        
        # Make charts to compare models
        col1, col2 = st.columns(2)
        
        with col1:
            # Compare R² scores
            r2_data = pd.DataFrame({
                'Model': list(model_results.keys()),
                'Train R²': [r['Train R²'] for r in model_results.values()],
                'Test R²': [r['Test R²'] for r in model_results.values()]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Train R²', x=r2_data['Model'], y=r2_data['Train R²']))
            fig.add_trace(go.Bar(name='Test R²', x=r2_data['Model'], y=r2_data['Test R²']))
            fig.update_layout(title='R² Score Comparison', barmode='group', 
                            yaxis_title='R² Score', showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Compare prediction errors
            mae_data = pd.DataFrame({
                'Model': list(model_results.keys()),
                'MAE': [r['MAE'] for r in model_results.values()]
            })
            
            fig = px.bar(mae_data, x='Model', y='MAE', title='Prediction Error (Lower is Better)')
            fig.update_layout(yaxis_tickformat='£,.0f')
            st.plotly_chart(fig, use_container_width=True)
        
        # Step 4: Look closer at the best model
        st.write(f"#### 4. Best Model Analysis: {best_model}")
        
        best_results = model_results[best_model]
        best_predictions = best_results['predictions']
        
        # Show the best model's scores
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Train R²", f"{best_results['Train R²']:.3f}")
        with col2:
            st.metric("Test R²", f"{best_results['Test R²']:.3f}")
        with col3:
            st.metric("CV R²", f"{best_results['CV R² (mean)']:.3f}")
        with col4:
            st.metric("MAE", f"£{best_results['MAE']:,.0f}")
        
        # Show how close predictions are to real prices
        fig = px.scatter(x=y_test, y=best_predictions,
                        labels={'x': 'Actual Price (£)', 'y': 'Predicted Price (£)'},
                        title=f'{best_model}: How Close Are Our Predictions?')
        
        # Add a line showing perfect predictions
        min_val = min(y_test.min(), best_predictions.min())
        max_val = max(y_test.max(), best_predictions.max())
        fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val],
                                mode='lines', name='Perfect Prediction',
                                line=dict(color='red', dash='dash')))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show which features are most important (only for tree models)
        if best_model in ['Random Forest', 'Decision Tree']:
            st.write("**Which Features Matter Most:**")
            
            importance_df = pd.DataFrame({
                'Feature': features,
                'Importance': best_results['model'].feature_importances_
            }).sort_values('Importance', ascending=False)
            
            fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                        title='Feature Importance for Price Prediction')
            st.plotly_chart(fig, use_container_width=True)
        
        # Step 5: Explain what the results mean
        st.write("#### 5. What Do These Results Mean?")
        
        if best_score > 0.5:
            st.success("""
            **Good Performance!**
            - Our model can explain over half of price differences
            - The new features we created really helped
            - The model gives consistent results
            """)
        elif best_score > 0.3:
            st.warning("""
            **Okay Performance:**
            - Model understands some price patterns
            - But we need more information for better predictions
            - Property size and exact address would help a lot
            """)
        else:
            st.info("""
            **Limited Performance:**
            - Model struggles to predict prices accurately
            - Shows we need more detailed property information
            - Current information isn't enough for good predictions
            """)
        
        # Explain why we can't do better
        with st.expander("📊 Why Can't We Predict Better?"):
            st.write("""
            **We're Missing Important Information:**
            
            Think about buying a house - what would you want to know?
            - **How big is it?** - We don't have square footage or number of rooms
            - **Where exactly?** - We only know the county, not the street
            - **What condition?** - Is it newly renovated or needs work?
            - **Special features?** - Garden? Parking? Nice view?
            
            Without this information, even the best computer model can only guess.
            It's like trying to guess someone's age just from their first name!
            """)
    
    else:
        st.error("Could not load data for ML performance analysis")