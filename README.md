# UK Property Price Predictor

## What This Project Does
This project uses machine learning to predict UK house prices. I built it to help people understand what affects property prices and to practice my data science skills.

**Who It's For:**
- Anyone curious about UK house prices
- People learning about data science
- Estate agents who want rough price estimates

**What It Does:**
- Shows UK house price patterns
- Predicts prices based on property features
- Explains what makes houses expensive

## Business Requirements

### Requirement 1: Understand Price Patterns
- Show which areas are most expensive
- Compare different property types
- See if new houses cost more than old ones

### Requirement 2: Predict House Prices
- Build a machine learning model
- Predict prices from property features
- Show how confident the prediction is

## The Data We Use

**Where it comes from:** Official UK government - HM Land Registry
**What it contains:** Records of every house sale in England and Wales since 1995
**How much"** 20,000 house sales (made smaller to the app runs fast)
**What information::** 11 different details about each house including price and location

### What Each Column Means:
- **Transaction ID:** Unique number for each house sale
- **Price:** How much the house sold for in pounds
- **Date:** When the house was sold
- **Property Type:** D=Detached, S=Semi-detached, T=Terraced, F=Flat
- **Old/New:** Y=Newly built, N=Older house
- **Duration:** F=You own it forever, L=You lease it for years
- **Town/City:** Which town house is in
- **District:** Local area
- **County:** Which county
- **Category:** Type classification
- **Status:** Data record information

## Project Hypotheses and Validation

### Hypothesis 1: Location Affects Price
**Initial Thought:** London would be most expensive  
**What We Found:** Surrey and Buckinghamshire are actually most expensive  
**Result:** REVISED - wealthy Home Counties cost more than London

### Hypothesis 2: Property Type Affects Price  
**Thought:** Detached houses cost more than other types  
**What We Found:** Yes! Detached > Semi > Terraced > Flat  
**Result:** VALIDATED

### Hypothesis 3: New Houses Cost More
**Thought:** Newly built houses are more expensive  
**What We Found:** Depends on location and market conditions  
**Result:** PARTIALLY VALIDATED

## Machine Learning Business Case

### The Problem
Estate agents and buyers need quick price estimates but professional valuations are expensive and slow.

### The Solution
A machine learning model that predicts prices instantly based on:
- Property type
- Location (county)
- New or old
- Freehold or leasehold

### Success Metrics
- **R² Score:** Above 0.2 (explains 20%+ of price variation)
- **MAE:** Under £100,000 (average error)
- **Business Value:** Provides rough estimates for initial discussions

### Model Results
- **R² Score:** 0.22 (explains 22% of prices)
- **MAE:** £78,000 (average error)
- **Conclusion:** Model provides basic estimates but needs more data for accuracy

## Dashboard Design

The app has 5 pages:

### Page 1: Project Summary
- Overview of the project
- Links to all other pages
- Quick statistics

### Page 2: House Price Study
- Charts showing price patterns
- County comparison map
- Property type analysis

### Page 3: Project Hypotheses
- Tests each hypothesis with data
- Shows charts proving or disproving ideas
- Explains what we learned

### Page 4: Predict House Price
- Enter property details
- Get instant price prediction
- See confidence level

### Page 5: ML Performance
- Shows how well model works
- Actual vs predicted prices chart
- Explains limitations

# How to Install and Run

### Requirements
- Python 3.8 or higher
- Internet connection
- Kaggle Account 

### Steps

1. **Clone the project:**
git clone [your-repo-url]
cd property-price-predictor

1. **Install Everything Needed:**
pip - install -r requirements.txt

2. **Set up data download:**
- Make free account at kaggle.com
- Go to Settings > API > Create New API Token
- Write down your username and key 

3. **Get the data:**

juypter notebook:

_Open jupyter_notebooks/01_DataCollection.ipynb_

_Put your Kaggle username and key in Cell 1_

_Run all the cells to download data_

4. **Start the app:**
streamlit run app.py

## Technologies Used

### Main Tools
- **Python 3.8** - Programming language
- **Streamlit** - Web app framework
- **Pandas** - Data handling
- **Scikit-learn** - Machine learning
- **Plotly** - Interactive charts

### Libraries
- numpy - Math operations
- matplotlib/seaborn - Charts
- pickle - Save models

## Testing

### Manual Testing
- Tested all pages load without errors
- Checked all charts display correctly
- Verified predictions work with different inputs
- Tested on different browsers (Chrome, Firefox, Safari)

### Data Testing
- Checked for missing values (none found)
- Removed outliers (prices below £50k and above £1M)
- Verified all features created correctly

### Model Testing
- Compared 4 different models (Linear Regression, Decision Tree, KNN, Random Forest)
- Used cross-validation to check stability
- Tested predictions on unseen data

# Bugs Fixed

### Bug 1: Negative R² Score
- **Problem:** Model had R² of -0.448 (worse than guessing average)
- **Cause:** Missing features and outliers in data
- **Fix:** Removed outliers and added Duration feature
- **Result:** R² improved to 0.22

### Bug 2: Plotly Error
- **Problem:** `update_yaxis` not working
- **Cause:** Wrong Plotly method
- **Fix:** Changed to `update_layout`

### Bug 3: Slow Loading
- **Problem:** App took 10+ minutes to load
- **Cause:** Loading 2 million records
- **Fix:** Created smaller dataset (20,000 records)

### Bug 4: Missing Features
- **Problem:** KeyError for 'Type_Age_Interaction'
- **Cause:** Trying to use feature before creating it
- **Fix:** Created features in correct order

### Known Issues
- Model accuracy limited (R² = 0.22) due to missing data
- Predictions have high error (MAE = £78k)
- Need more features for better accuracy

## Project Outcomes

### What Worked
- Successfully predicted prices with 22% accuracy
- Identified key price factors
- Created working web application
- Validated 4 out of 5 hypotheses

### Limitations
- Missing important data (house size, exact location)
- Historical data (1995-2017) not current
- Model accuracy limited without more features

### Future Improvements
- Get property size data
- Add postcode-level location
- Update with recent sales data
- Try more advanced models

## Credits

### Data Source
- UK Land Registry - Official government property data
- Kaggle API for data access

### Learning Resources That Helped

#### Machine Learning Concepts
- **StatQuest with Josh Starmer** - Random Forest Explained
  - https://www.youtube.com/watch?v=J4Wdy0Wc_xQ
  - Helped understand how Random Forest works
  

#### Python and Pandas
- **Corey Schafer Python Tutorials** - Pandas DataFrame basics
  - https://www.youtube.com/watch?v=ZyhVh-qRZPA
  - Helped with data manipulation

#### Statistics and Math
- **Khan Academy** - Statistics fundamentals
  - Mean, median, standard deviation explained
  - https://www.khanacademy.org/math/statistics-probability
  
- **3Blue1Brown** - Linear Regression visual explanation
  - https://www.youtube.com/watch?v=PaFPbb66DxQ
  - Visual understanding of regression

#### Streamlit Development
- **Streamlit Documentation** - Official tutorials
  - https://docs.streamlit.io
  
- **Data Professor YouTube** - Streamlit app tutorials
  - https://www.youtube.com/dataprofessor
  - Helped build the web interface

### Code Institute Resources
- Course materials and walkthrough projects
- Mentor guidance and support
- Slack community for troubleshooting

## Future Development

### If I Had More Time
- Add more features like property size and exact postcode
- Try advanced models like XGBoost or Neural Networks
- Create an API for other developers to use
- Add user accounts to save predictions
- Include recent 2020+ data

### What I Learned
- Data quality matters more than complex models
- Missing features limit accuracy
- Real projects need lots of debugging
- Simple explanations help users understand