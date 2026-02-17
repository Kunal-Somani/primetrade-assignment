# Bitcoin Sentiment & Trader Behavior Analysis

## Overview
This project analyzes how **Market Sentiment (Fear vs. Greed)** impacts trader psychology and performance on Hyperliquid. Using data from 167,000+ trades, we clustered traders into archetypes and built a predictive model to forecast trade outcomes.

![Dashboard Preview](dashboard_preview.png)

## Key Insights (Part C)

### 1. Market Sentiment & Performance
* **"Extreme Greed" Volatility:** Our analysis shows that while "Extreme Greed" days have the highest average win rates (~40%), they also exhibit the widest variance in PnL.
* **The "Neutral" Trap:** Traders perform worst during "Neutral" sentiment, likely due to a lack of clear market direction.

### 2. Trader Archetypes (Clustering Results)
Using K-Means clustering, we identified 3 distinct behaviors:
* **Cluster 0 (Retail Scalpers):** High frequency, small position sizes (~$5k), taking quick profits.
* **Cluster 1 (The Snipers):** Best performers with **$1.9M total PnL**. They trade less often but with high conviction.
* **Cluster 2 (Whales):** Largest average position sizes (~$17.5k).

### 3. Predictive Modeling (Bonus)
We built a Random Forest Classifier to predict profitable trades.
* **Accuracy:** **72.15%**
* **Precision (Predicting Losses):** **76%**
* **Utility:** This model can be used as a risk-filter to prevent trades during unfavorable sentiment conditions.

---

##Project Structure
* `notebooks/01_analysis.ipynb`: Detailed EDA, Data Cleaning, and Visualizations (Part A & B).
* `src/modeling.py`: Automated pipeline for Merging, Clustering, and Training the Predictive Model.
* `dashboard.py`: Interactive Streamlit App for exploring the data.
* `data/`: Contains raw CSVs (ignored by git) and processed data.

---

## Setup & Usage

### 1. Installation 
Clone the repository and install dependencies:
```bash
git clone [https://github.com/Kunal-Somani/primetrade-assignment.git](https://github.com/Kunal-Somani/primetrade-assignment.git)
cd primetrade-assignment
pip install -r requirements.txt
```

### 2. Run the Analysis
To execute the data processing pipeline, perform trader clustering, and train the predictive model:
```bash
streamlit run src/dashboard.py
```

### 3. Launch Dashboard
To launch the interactive Streamlit dashboard for visual exploration:
```bash
streamlit run dashboard.py
```
---

## Submitted by Kunal Somani for Primetrade.ai Internship
