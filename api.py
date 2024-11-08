from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import jwt
from datetime import datetime, timedelta
from flask_swagger_ui import get_swaggerui_blueprint
import yfinance as yf
import pandas as pd
from save_load_model import load_model
from data_collection import get_stock_data
from data_preprocessing import preprocess_data
from feature_engineering import add_features
from labeling import label_risk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Rate limiting configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

# Authentication middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Stock Analysis API"}
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

# Authentication endpoint
@app.route('/api/auth/token', methods=['POST'])
@limiter.limit("5 per minute")
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'error': 'Missing credentials'}), 401
        
    # Replace with your actual authentication logic
    if auth.username == "admin" and auth.password == "password":
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Stock analysis endpoint
@app.route('/api/v1/analyze/<ticker>', methods=['GET'])
@token_required
@limiter.limit("30 per minute")
def analyze_stock(ticker):
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
        app.logger.error(f"Error analyzing stock {ticker.upper()}: {str(e)}")
        return jsonify({
            'error': 'An internal error has occurred. Please try again later.',
            'ticker': ticker.upper()
        }), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True) 