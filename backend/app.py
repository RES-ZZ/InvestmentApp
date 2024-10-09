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

if __name__ == '__main__':
    app.run(debug=True)
