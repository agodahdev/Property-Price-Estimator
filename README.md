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
