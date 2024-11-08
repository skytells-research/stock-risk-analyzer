from flask import Flask, render_template, request, jsonify, url_for
import yfinance as yf
import pandas as pd
from save_load_model import load_model
from data_collection import get_stock_data
from data_preprocessing import preprocess_data
from feature_engineering import add_features
from labeling import label_risk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.form['ticker'].upper()
    try:
        # Get stock data and analyze
        data = get_stock_data(ticker)
        data = preprocess_data(data)
        data = add_features(data)
        data = label_risk(data)
        
        # Load the model
        model = load_model()
        
        # Get features for prediction
        features = ['Daily Return', 'Volatility', 'MA50', 'MA200']
        latest_data = data[features].iloc[-1]
        
        # Make prediction
        risk_level = model.predict(latest_data.values.reshape(1, -1))[0]
        
        # Format dates and prices for the chart (last 30 days)
        # Convert index to datetime if it's not already
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
            
        # Format dates for the chart
        dates = [d.strftime('%Y-%m-%d') for d in data.index[-30:]]
        prices = data['Close'].tail(30).tolist()
        
        return jsonify({
            'risk_level': risk_level,
            'current_price': f"{data['Close'].iloc[-1]:.2f}",
            'volatility': f"{data['Volatility'].iloc[-1]*100:.2f}",
            'daily_return': f"{data['Daily Return'].iloc[-1]*100:.2f}",
            'dates': dates,
            'prices': prices
        })
    except Exception as e:
        import traceback
        import logging
        logging.error(traceback.format_exc())  # Log the full error on the server
        return jsonify({'error': 'An internal error has occurred.'}), 400

@app.route('/api/analyze/<ticker>', methods=['GET'])
def analyze_api(ticker):
    try:
        # Get stock data and analyze
        data = get_stock_data(ticker.upper())
        data = preprocess_data(data)
        data = add_features(data)
        data = label_risk(data)
        
        # Load the model
        model = load_model()
        
        # Get features for prediction
        features = ['Daily Return', 'Volatility', 'MA50', 'MA200']
        latest_data = data[features].iloc[-1]
        
        # Make prediction
        risk_level = model.predict(latest_data.values.reshape(1, -1))[0]
        
        # Prepare API response
        response = {
            'ticker': ticker.upper(),
            'analysis': {
                'risk_level': int(risk_level),
                'current_price': float(data['Close'].iloc[-1]),
                'volatility': float(data['Volatility'].iloc[-1]),
                'daily_return': float(data['Daily Return'].iloc[-1]),
                'last_updated': data.index[-1].isoformat()
            },
            'historical_data': {
                'dates': [d.isoformat() for d in data.index[-30:]],
                'prices': [float(p) for p in data['Close'].tail(30)]
            }
        }
        
        return jsonify(response)
    except Exception as e:
        import traceback
        import logging
        logging.error(traceback.format_exc())  # Log the full error on the server
        return jsonify({
            'error': 'An internal error has occurred.',
            'ticker': ticker.upper()
        }), 400

if __name__ == '__main__':
    app.run(debug=True)