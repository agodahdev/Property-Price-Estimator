import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_data_files():
    #Test data files directly
    try:
        # Check for small dataset first
        small_dataset_path = "inputs/datasets/collection/uk_housing_small.csv"
        if os.path.exists(small_dataset_path):
            df = pd.read_csv(small_dataset_path)
            print(f"✅ Small dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        
        # If small dataset doesn't exist, try to create it from raw data
        print("Small dataset not found, checking raw data...")
        raw_csv = "inputs/datasets/raw/price_paid_records.csv"
        
        if os.path.exists(raw_csv):
            print(f"Found raw data file: {raw_csv}")
            df = pd.read_csv(raw_csv, low_memory=False)
            print(f"Raw data loaded: {df.shape[0]} rows")
            
            # Create small dataset
            df_small = df.sample(n=min(20000, len(df)), random_state=42)
            
            # Save small dataset
            os.makedirs("inputs/datasets/collection", exist_ok=True)
            df_small.to_csv(small_dataset_path, index=False)
            print(f"✅ Created small dataset: {df_small.shape[0]} rows")
            return df_small
        else:
            print(f"❌ Raw data file not found: {raw_csv}")
            return None
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return None

def test_app():
    """Test basic app functionality"""
    print("=== Testing Data Files ===")
    
    df = test_data_files()
    if df is None:
        return False
    
    # Test required columns
    required_cols = ['Transaction unique identifier', 'Price', 'Date of Transfer', 
                    'Property Type', 'Old/New', 'Duration', 'County']
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        print(f"❌ Missing columns: {missing}")
        print(f"Available columns: {df.columns.tolist()}")
        return False
    
    print("✅ All required columns present")
    print(f"✅ Price range: £{df['Price'].min():,.0f} - £{df['Price'].max():,.0f}")
    print(f"✅ Property types: {df['Property Type'].unique()}")
    print(f"✅ Counties available: {df['County'].nunique()}")
    
    return True

if __name__ == "__main__":
    if test_app():
        print("\n🎉 App ready - run 'streamlit run app.py'")
    else:
        print("\n❌ App has issues - check data files")