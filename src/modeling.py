import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pickle
import warnings

warnings.filterwarnings('ignore')

def run_modeling():
    print("🚀 Starting Model Pipeline...")
    try:
        print("   -> Loading datasets...")
        sentiment = pd.read_csv('data/sentiment.csv')
        traders = pd.read_csv('data/trader_data.csv')
    except FileNotFoundError:
        print("❌ Error: Files not found. Make sure 'sentiment.csv' and 'trader_data.csv' are in the 'data/' folder.")
        return

    print("   -> Merging data...")

    sentiment['date'] = pd.to_datetime(sentiment['date'])
    traders['clean_date'] = pd.to_datetime(traders['Timestamp IST'], errors='coerce')
    traders['date_only'] = traders['clean_date'].dt.normalize()

    df = traders.merge(sentiment, left_on='date_only', right_on='date', how='left')
    df = df.dropna(subset=['value'])
    df.to_csv('data/final_merged_data.csv', index=False)
    print(f"   -> Data merged. Total rows for modeling: {len(df)}")

    print("\n🧠 Running Bonus Task 1: Trader Clustering...")

    df['is_win'] = df['Closed PnL'] > 0
    trader_profiles = df.groupby('Account').agg({
        'Closed PnL': 'sum',
        'Size USD': 'mean',
        'is_win': 'mean',    
        'value': 'mean'        
    }).reset_index()
    trader_profiles = trader_profiles.fillna(0)
    X_cluster = trader_profiles[['Closed PnL', 'Size USD', 'is_win', 'value']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    trader_profiles['Cluster'] = kmeans.fit_predict(X_cluster)
    print("   -> Clusters generated. Summary:")
    print(trader_profiles.groupby('Cluster')[['Closed PnL', 'Size USD', 'is_win']].mean())
    print("\n🔮 Running Bonus Task 2: Predictive Modeling...")
 
    df['target'] = (df['Closed PnL'] > 0).astype(int)

    le = LabelEncoder()
    df['Side_Code'] = le.fit_transform(df['Side'].astype(str))
    features = ['value', 'Size USD', 'Side_Code']
    X = df[features]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    print(f"   -> Model Accuracy: {acc:.2%}")
    print("\n   -> Classification Report:")
    print(classification_report(y_test, preds))
    with open('models/trade_predictor.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("   -> Model saved to 'models/trade_predictor.pkl'")

if __name__ == "__main__":
    run_modeling()