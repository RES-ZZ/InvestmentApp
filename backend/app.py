# app.py
from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return "AI-Powered Stock Basket Backend"
# app.py (continued)

# Function to generate stock tickers based on theme using OpenAI
def generate_stock_tickers(theme):
    prompt = f"Generate a diversified list of 10 Indian stocks or ETFs for the following investment theme: {theme}. Ensure diversification across sectors such as Technology, Banking, Healthcare, Consumer Goods, and Energy. Provide only the stock tickers separated by commas."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    tickers = response.choices[0].text.strip().split(',')
    tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
    return tickers

# Function to fetch detailed stock information from Alpha Vantage
def fetch_stock_details(ticker):
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker.split('.')[0],  # Remove exchange suffix if present
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        return {
            'name': data.get('Name', 'N/A'),
            'ticker': ticker,
            'sector': data.get('Sector', 'N/A'),
            'url': data.get('Website', '#'),
            'pe_ratio': data.get('PERatio', 'N/A'),
            'eps': data.get('EPS', 'N/A'),
            'dividend_yield': data.get('DividendYield', 'N/A'),
            'market_cap': data.get('MarketCapitalization', 'N/A'),
            '52_week_change': data.get('52WeekChange', 'N/A'),
            'description': data.get('Description', 'N/A'),
        }
    else:
        return None
    # app.py (continued)

@app.route('/generate-portfolio', methods=['POST'])
def generate_portfolio():
    data = request.get_json()
    theme = data.get('theme')
    if not theme:
        return jsonify({"error": "Theme is required"}), 400

    # Generate stock tickers using OpenAI
    tickers = generate_stock_tickers(theme)

    # Fetch detailed stock information
    detailed_stocks = []
    for ticker in tickers:
        stock_info = fetch_stock_details(ticker)
        if stock_info:
            detailed_stocks.append(stock_info)

    return jsonify({"stocks": detailed_stocks})
# app.py (continued)

@app.route('/stock-details', methods=['GET'])
def stock_details():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    stock_info = fetch_stock_details(ticker)
    if stock_info:
        return jsonify(stock_info)
    else:
        return jsonify({"error": "Stock data not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)

