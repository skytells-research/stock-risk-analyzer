from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from data_collection import get_stock_data
from data_preprocessing import preprocess_data
from feature_engineering import add_features
from labeling import label_risk
import joblib
import pandas as pd

def save_model(model, filename='risk_model.pkl'):
    """
    Save the trained model to disk.
    """
    joblib.dump(model, filename)

def train_model(ticker_list):
    """
    Train the risk classification model on provided stock tickers.
    """
    all_data = []
    for ticker in ticker_list:
        data = get_stock_data(ticker, period='2y')
        data = preprocess_data(data)
        data = add_features(data)
        data = label_risk(data)
        all_data.append(data)
    
    df = pd.concat(all_data)
    df = df.dropna()
    
    features = ['Daily Return', 'Volatility', 'MA50', 'MA200']
    X = df[features]
    y = df['Risk Level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the model
    save_model(model)
    
    print("Model training completed and saved as 'risk_model.pkl'.")

if __name__ == "__main__":
    ticker_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    train_model(ticker_list)