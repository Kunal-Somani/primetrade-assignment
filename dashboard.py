import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Trader Behavior Dashboard", layout="wide")
st.title("📊 Market Sentiment vs Trader Performance")

# 2. Load Data
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/final_merged_data.csv') 
    except FileNotFoundError:
        return pd.read_csv('data/trader_data.csv') 

df = load_data()

# 3. Dashboard Layout
if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # --- FIX: Changed 'Classification' to 'classification' (lowercase) ---
    if 'classification' in df.columns:
        sentiment_filter = st.sidebar.multiselect(
            "Select Sentiment", 
            options=df['classification'].unique(),
            default=df['classification'].unique()
        )
        # Apply Filter
        df = df[df['classification'].isin(sentiment_filter)]
    else:
        st.sidebar.warning("Column 'classification' not found in data.")

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trades", f"{len(df):,}")
    
    total_pnl = df['Closed PnL'].sum() if 'Closed PnL' in df.columns else 0
    col2.metric("Total PnL", f"${total_pnl:,.2f}")
    
    win_rate = (df['Closed PnL'] > 0).mean() * 100 if 'Closed PnL' in df.columns else 0
    col3.metric("Win Rate", f"{win_rate:.1f}%")
    
    # Chart: PnL Distribution
    st.subheader("PnL Distribution")
    if 'Closed PnL' in df.columns:
        # --- FIX: Changed 'Classification' to 'classification' here too ---
        color_col = 'classification' if 'classification' in df.columns else None
        
        fig = px.histogram(
            df, 
            x='Closed PnL', 
            nbins=50, 
            color=color_col,
            title="Distribution of Profits & Losses"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Column 'Closed PnL' not found.")

else:
    st.error("Data could not be loaded. Please ensure 'data/final_merged_data.csv' exists.")