import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("TM_API_KEY")
BASE_URL = "https://api.tokenmetrics.com/v2"  # Updated to v2 API base URL

headers = {
    "accept": "application/json",
    "api_key": API_KEY
}

def get_tokens(symbols=None, limit=10):
    """
    Get token information by symbols
    """
    if not API_KEY:
        logging.error("Token Metrics API key not found")
        return {"error": "API key not configured"}
    
    url = f"{BASE_URL}/tokens"  # This endpoint exists in v2 as well
    
    params = {
        "limit": limit
    }
    
    if symbols:
        params["token_symbols"] = symbols
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching tokens: {e}")
        return {"error": str(e)}

def get_trading_signals(symbol=None, limit=10):
    """
    Get trading signals for a token using v2 endpoint
    """
    if not API_KEY:
        logging.error("Token Metrics API key not found")
        return {"error": "API key not configured"}
    
    # FIXED: Use a wider date range (last 180 days instead of 7)
    # This ensures we get the most recent available data even if it's older
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    # Updated to use the trading-signals endpoint from v2
    url = f"{BASE_URL}/trading-signals"
    
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "limit": limit
    }
    
    if symbol:
        params["symbol"] = symbol
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Log data for debugging
        logging.debug(f"Trading signals response: {data}")
        
        # Sort data by date to ensure we get the most recent first
        if "data" in data and data["data"]:
            data["data"] = sorted(data["data"], key=lambda x: x.get("DATE", ""), reverse=True)
        
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching trading signals: {e}")
        return {"error": str(e)}

def get_market_metrics():
    """
    Get market metrics (replaces market-indicator in v1)
    """
    if not API_KEY:
        logging.error("Token Metrics API key not found")
        return {"error": "API key not configured"}
    
    # FIXED: Use a wider date range (last 180 days instead of 30)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    # Updated to use the market-metrics endpoint from v2
    url = f"{BASE_URL}/market-metrics"
    
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "limit": 30
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Sort data by date to ensure we get the most recent first
        if "data" in data and data["data"]:
            data["data"] = sorted(data["data"], key=lambda x: x.get("DATE", ""), reverse=True)
        
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching market metrics: {e}")
        return {"error": str(e)}

def get_top_tokens(limit=5):
    """
    Get top tokens based on trader grades
    """
    # This function is not working well - we'll use get_alternative_top_tokens instead
    return get_alternative_top_tokens(limit)

def generate_signal(symbol):
    """
    Generate a trading signal for a specific token
    """
    # Get trading signal data from v2
    signal_data = get_trading_signals(symbol=symbol, limit=10)  # Get more signals to find recent ones
    
    if "error" in signal_data:
        return signal_data
    
    if "data" in signal_data and signal_data["data"]:
        # Get the most recent data (already sorted in get_trading_signals)
        latest = signal_data["data"][0]
        
        # Extract signal info based on v2 response structure
        token_symbol = latest.get("TOKEN_SYMBOL", symbol.upper())
        trading_signal = latest.get("TRADING_SIGNAL", 0)
        tm_trader_grade = latest.get("TM_TRADER_GRADE", 0)
        
        # Determine buy/sell signal based on TRADING_SIGNAL
        if trading_signal == 1:
            action = "BUY ✅"
            confidence = tm_trader_grade
        elif trading_signal == -1:
            action = "SELL ❌"
            confidence = 100 - tm_trader_grade if tm_trader_grade else 50
        else:
            action = "HOLD ⏹️"
            confidence = 50
        
        date = latest.get("DATE", datetime.now().strftime("%Y-%m-%d"))
        
        return {
            "symbol": token_symbol,
            "action": action,
            "confidence": confidence,
            "updated_at": date
        }
    
    # Log that we have no data for this token
    logging.warning(f"No trading signal data available for {symbol}")
    
    # Return a more informative error instead of a generic HOLD signal
    return {"error": f"No trading data available for {symbol.upper()}. Try a more popular token like BTC or ETH."}

def get_alternative_top_tokens(limit=5):
    """
    Alternative method to get top tokens using trading signals
    """
    if not API_KEY:
        logging.error("Token Metrics API key not found")
        return {"error": "API key not configured"}
    
    # FIXED: Increase the limit to find more tokens
    # Request more tokens initially to filter and get the best ones
    signals = get_trading_signals(limit=100)
    
    if "error" in signals:
        return signals
    
    if "data" in signals and signals["data"]:
        # Filter signals with TRADING_SIGNAL=1 (bullish)
        bullish_tokens = [token for token in signals["data"] if token.get("TRADING_SIGNAL") == 1]
        
        # If we don't have enough bullish tokens, include neutral ones too
        if len(bullish_tokens) < limit:
            neutral_tokens = [token for token in signals["data"] if token.get("TRADING_SIGNAL") == 0]
            bullish_tokens.extend(neutral_tokens)
        
        # Sort by TM_TRADER_GRADE in descending order
        sorted_tokens = sorted(bullish_tokens, key=lambda x: x.get("TM_TRADER_GRADE", 0), reverse=True)
        
        # Return top N tokens
        result = {"data": sorted_tokens[:limit]}
        return result
    
    # Return empty data with better error message
    logging.warning("No tokens found in the trading signals response")
    return {"error": "No token data available. Please check your API key and try again later."}