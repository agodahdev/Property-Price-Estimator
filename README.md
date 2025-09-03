# UK Property Price Predictor

## What This Project Does
This project helps people understand UK house prices smart computer analysis. It's designed for estate agents, property investors,
and anyone looking to buy a house who wants to make better decisions based on real data.

**Main Goals:**
- Look at UK house price patterns
- Build a computer system that can predict house prices
- Give useful advice for property decisions
- Make it easy for use for regular people

## Business Goals

**Goal 1 - Analyze the Markey:**
Study how different things about houses (where they are, what type, how old) affect price across the UK to spot trends and
opportunities.

**Goal 2 - Predict Prices:**
Build a smart sytem that can guess how much should cost, helping estate agents and buyers make better choices

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

## The Three Big Questions

### Question 1: Are London Houses Way More Expensive?
**What we think:** London houses cost much more than houses anywhere else in the UK.

**How we test it:** Compare average London house prices with everywhere else.

**What counts as success:** London houses cost at least 50% more.

### Question 2: Are Detached Houses the Most Expensive?
**What we think:** Detached houses cost the most money compared to other property types.

**How we test it:** Look at average prices for all house types (detached, semi-detached, terraced, flat)

**What counts as success:** Detached houses are the most expensive type.

### Question 3: Do New Houses Cost More?
**What we think:** Newly built houses sell for more money than older houses.

**How we test it:** Compare prices of new vs old houses.

**What counts as success:** New houses have higher average prices.

## How the Smart Sytem Works

### What it Does
Creates a computer system that can guess house prices for estate agents and investors.

### How It Learns
Uses "Random Forest" - a smart method that looks a lot of different factors to make good guesses.

### What Information It Uses
- House types (detached, semi-detached, terrace, flat)
- Location (which county)
- Age (new/old)
- Ownership type (leased/own forever)

### What It Tells You
- Predicated house price in pounds
- How confident we are in our guess
- Price range for similar houses

### How Well It Works
- **Accuracy Score:** Above 70%
- **Average Error:** less than £50,000 (reasonble mistake range)
- **Success Rate:** Right withn 20% for 8 out of 10 houses

### Our Results
- **Training Score**: 85%+ (learns well from examples)
- **Test Score:** 75%+ (works well on new houses)
- **Training Error:** £35,000 - £45,000 (acceptable mistakes)
- **Test Error:** £40,000 - £55,000 (reasonable for new data)

## The Website

### Page 1: Project Summary
**What's on it:** Overview of everything, main goals, data summary

**Why it's useful:** Gives you the big picture of what this project does

**What you can do:** See key numbers and statistics

### Page 2: Property Analysis
**What's on it:** Charts and graphs showing house prices patterns

**Why it's useful:** Answers Goal 1 - gives price predictions

**What you can see:** Different types of charts showing price trends

**What you can do:** Look at interactive charts

### Page 3: Price Predicator
**What's on it:** Forms where you enter house details to get a price guess

**Why it's useful:** Answers Goal 2 - gives price predictions

**What you can see:** Pick house features and get instant price estimates

**Special features:** Show how confident we are in the prediction

### Page 4: Project Questions
**What's on it:** Results of testing our three big questions

**Why it's useful:** Proves our assumptions with real data

**What you can see:** Charts and evidence for each question

**What you can do:** See which questions were right or wrong

### Page 5: System Performance
**What's on it:** How well our smart system works

**Why it's useful:** Shows you can trust Goal 2 predictions

**What you can see:** Accuracy charts and error measurements

**What you can do:** Check how reliable the predictions are
## What We Built This With

**Main Language:** Python

**Website Framework:** Streamli

**Data work:** Pandas, Numpy

**Smart Learning:** Scikit-learn (Random Forest)

**Charts:** Plotly, Matplotlib, Seaborn

**Development:** Jupyter Notebooks

**Data Storage:** Kaggle API

## How To Set It Up

### What You Need First
- Python 3.12 or newer
- Kaggle Account

### Set by Step Setup

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

## How We Get and Process Data:

### Automatic Data Sytem
The project downloads data by itself using Kaggle:

1.**Download**: Gets UK house price data automatically
1. **Download:** Gets UK house price data automatically
2. **Extract:** Unzips files and loads data
3. **Clean:** Fixes any problems with the data
4. **Make Smaller:** Creates faster version for the app
5. **Save:** Puts data in organized folders

### Data Processing Steps
- **Collection:** Downloads from official government source
- **Cleaning:** Fixes missing information
- **Engineering:** Converts text to numbers for the computer
- **Sampling:** Makes smaller dataset (20,000 houses) for speed
- **Validation:** Checks data quality

## How We Built the Smart System

### Preparing the Data
- **Converting Text:** Changes house types and counties to numbers
- **Picking Features:** Focuses on important factors (location, type, ownership)
- **Splitting Data:** Uses 80% for training, 20% for testing

### Why We Chose Random Forest
**Random Forest chosen because:**
- Great at handling different types of information
- Doesn't get confused by complex patterns
- Can tell us which factors matter most
- Works well for guessing prices
- Easy for business people to understand

### Making It Better
We tested different settings to make it work best:
- **Number of trees:** Tried 10, 50, 100, 200 trees
- **Tree depth:** Tested different maximum depths
- **Splitting rules:** Various ways to split data
- **Leaf size:** Different minimum sizes
- **Feature selection:** Different ways to pick factors
- **Consistency:** Set random seed for same results every time

**Final Setup:** 50 trees with other settings optimized for best performance.

## What We Found Out

### Our Three Questions - The Results

**Question 1: CORRECT**
London houses do cost 150-200% more than other UK areas. Big difference confirmed.

**Question 2: CORRECT** 
Detached houses are definitely the most expensive, costing 40-60% more than terraced houses.

**Question 3: PARTLY CORRECT**
New houses sometimes cost more, but it depends on location. Usually 15-25% more in popular areas.

### Business Value
- **Estate Agents:** Give clients data-backed price estimates
- **Investors:** Find good deal and market opportunities  
- **Buyers:** Make smarter decisions with real market data
- **Everyone:** Better understanding of UK house market

## Problems We Solved

### Technical Challenges Fixed

**Speed Problems:**
- Started with 2 million+ house records that took 10 minutes to load
- Fixed by using smaller sample and smart caching
- Now loads in under 10 seconds

**Code Errors:**
- Fixed many spelling mistakes in code
- Corrected Python syntax problems
- Fixed file path mistakes

**Data Problems:**
- Made automatic download from Kaggle work
- Added error handling for missing files
- Created backup plans when things go wrong

**User Experience:**
- Added clear explanations for UK house terms
- Made technical codes user-friendly
- Added confidence indicators for predictions