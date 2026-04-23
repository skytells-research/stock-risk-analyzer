from flask import Flask, render_template, request, jsonify, url_for
import yfinance as yf
import pandas as pd
import os
import logging
from save_load_model import load_model
from data_collection import get_stock_data
from data_preprocessing import preprocess_data
from feature_engineering import add_features
from labeling import label_risk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mining-dashboard')
def mining_dashboard():
    return render_template('mining_dashboard.html')

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


# ── Mining Dashboard API ──────────────────────────────────────────────────────

PORTFOLIO_COMPANIES = [
    {'id': 1,  'ticker': 'DAK',   'name': 'Dakota Gold',         'region': 'USA',       'compliance': 'OK'},
    {'id': 2,  'ticker': 'NCU',   'name': 'Nevada Copper',       'region': 'USA',       'compliance': 'WARN'},
    {'id': 3,  'ticker': 'LAC',   'name': 'Lithium Americas',    'region': 'USA',       'compliance': 'OK'},
    {'id': 4,  'ticker': 'RVG.V', 'name': 'Revival Gold',        'region': 'Canada',    'compliance': 'OK'},
    {'id': 5,  'ticker': 'IVPAF', 'name': 'Ivanhoe Mines',       'region': 'Africa',    'compliance': 'OK'},
    {'id': 6,  'ticker': 'FCX',   'name': 'Freeport-McMoRan',    'region': 'USA',       'compliance': 'OK'},
    {'id': 7,  'ticker': 'NEM',   'name': 'Newmont Corp',        'region': 'USA',       'compliance': 'OK'},
    {'id': 8,  'ticker': 'GOLD',  'name': 'Barrick Gold',        'region': 'Canada',    'compliance': 'OK'},
    {'id': 9,  'ticker': 'WPM',   'name': 'Wheaton Precious',    'region': 'Canada',    'compliance': 'OK'},
    {'id': 10, 'ticker': 'ALB',   'name': 'Albemarle Corp',      'region': 'USA',       'compliance': 'OK'},
]

COMPLIANCE_RECORDS = [
    {'id': 1, 'company': 'Nevada Copper',   'type': 'NPDES',     'status': 'WARN',  'details': 'Quarterly discharge report pending (Q4)',      'deadline': '2025-12-31'},
    {'id': 2, 'company': 'Highland Copper', 'type': 'SWPPP',     'status': 'OK',    'details': 'Annual inspection complete',                   'deadline': 'N/A'},
    {'id': 3, 'company': 'Portfolio-Wide',  'type': 'TRI/Tier II','status': 'ALERT','details': 'Annual reporting deadline approaching',         'deadline': '2026-03-01'},
    {'id': 4, 'company': 'Freeport-McMoRan','type': 'NPDES',     'status': 'OK',    'details': 'All discharge permits current',                'deadline': 'N/A'},
    {'id': 5, 'company': 'Newmont Corp',    'type': 'SWPPP',     'status': 'OK',    'details': 'Stormwater plan updated Q3',                   'deadline': 'N/A'},
]

COMMODITY_TICKERS = {
    'gold':    'GC=F',
    'copper':  'HG=F',
    'silver':  'SI=F',
    'lithium': 'ALB',
}

STATIC_NEWS = [
    {'id': 1, 'headline': 'Ambler Access Approved for Alaska',                             'source': 'Internal Intel'},
    {'id': 2, 'headline': 'Vedanta Resources Launches CopperTech Initiative',              'source': 'Internal Intel'},
    {'id': 3, 'headline': 'Final 2025 List of Critical Minerals Adds Copper, Met Coal',    'source': 'Internal Intel'},
]

EVENT_CALENDAR = [
    {'id': 1, 'name': 'Resourcing Tomorrow',   'date': 'Dec 2-4, 2025',   'location': 'London, UK'},
    {'id': 2, 'name': 'AEMA Annual Conference', 'date': 'Dec 7-12, 2025',  'location': 'Reno, NV'},
    {'id': 3, 'name': 'Mining Indaba',          'date': 'Feb 9-12, 2026',  'location': 'Cape Town, SA'},
]


def _fetch_price_change(ticker_symbol):
    """Return (current_price, change_pct_str) via yfinance, or (None, None) on failure."""
    try:
        info = yf.Ticker(ticker_symbol).fast_info
        current = info.last_price
        prev = info.previous_close
        if current and prev and prev != 0:
            pct = (current - prev) / prev * 100
            sign = '+' if pct >= 0 else ''
            return round(current, 2), f"{sign}{pct:.1f}%"
    except Exception:
        pass
    return None, None


@app.route('/api/mining/market')
def mining_market():
    result = {}
    for name, sym in COMMODITY_TICKERS.items():
        price, change = _fetch_price_change(sym)
        if price is None:
            result[name] = {'price': 'N/A', 'change': 'N/A', 'alert': 'monitoring'}
        else:
            pct_val = float(change.replace('+', '').replace('%', ''))
            result[name] = {
                'price': price,
                'change': change,
                'alert': 'high-trigger' if abs(pct_val) > 1 else 'monitoring',
            }
    return jsonify(result)


@app.route('/api/mining/portfolio')
def mining_portfolio():
    rows = []
    for co in PORTFOLIO_COMPANIES:
        price, change = _fetch_price_change(co['ticker'])
        rows.append({
            **co,
            'price': price if price is not None else 'N/A',
            'change': change if change is not None else 'N/A',
        })
    return jsonify(rows)


@app.route('/api/mining/compliance')
def mining_compliance():
    return jsonify(COMPLIANCE_RECORDS)


@app.route('/api/mining/news')
def mining_news():
    items = list(STATIC_NEWS)
    try:
        raw = yf.Ticker('GC=F').news or []
        for i, article in enumerate(raw[:3], start=len(items) + 1):
            title = article.get('content', {}).get('title') or article.get('title', '')
            if title:
                items.append({'id': i, 'headline': title, 'source': 'Yahoo Finance'})
    except Exception:
        pass
    return jsonify({'news': items, 'events': EVENT_CALENDAR})


@app.route('/api/mining/query', methods=['POST'])
def mining_query():
    body = request.get_json(silent=True) or {}
    query = body.get('query', '').strip()
    if not query:
        return jsonify({'error': 'query field is required'}), 400

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return jsonify({'error': 'ANTHROPIC_API_KEY not configured on server'}), 503

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=1024,
            system=(
                'You are CommodAI-Tee, a mining industry analyst specializing in: '
                'All-in Sustaining Costs (AISC) for gold producers; '
                'ESG compliance (NPDES, SWPPP, TRI/Tier II reporting under EPA); '
                'critical mineral supply chains (copper, lithium, cobalt, rare earths); '
                'junior and mid-tier mining company risk assessment. '
                'Be concise and data-driven. Use bullet points where appropriate.'
            ),
            messages=[{'role': 'user', 'content': query}],
        )
        return jsonify({'response': message.content[0].text})
    except Exception as e:
        logging.error('mining_query error: %s', e)
        return jsonify({'error': 'Query processing failed. Check server logs.'}), 500


# ── End Mining Dashboard API ──────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)