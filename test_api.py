# test_api.py
# A simple script to test the Token Metrics API v2 integration

import os
from dotenv import load_dotenv
import tm_api
import json

# Load environment variables
load_dotenv()

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def test_api_connection():
    """Test basic API connectivity"""
    print("Testing Token Metrics API v2 Connection...")
    print("\n1. Testing get_tokens() function...")
    tokens = tm_api.get_tokens(symbols="btc")
    
    if "error" in tokens:
        print(f"❌ Error: {tokens['error']}")
        return False
    
    print("✅ Successfully connected to Token Metrics API v2")
    print(f"Retrieved data for {len(tokens.get('data', []))} tokens")
    return True

def test_signal_generation():
    """Test signal generation for BTC"""
    print("\n2. Testing generate_signal() function...")
    signal = tm_api.generate_signal("btc")
    
    if "error" in signal:
        print(f"❌ Error: {signal['error']}")
        return False
    
    print("✅ Successfully generated signal")
    print(f"Symbol: {signal.get('symbol')}")
    print(f"Action: {signal.get('action')}")
    print(f"Confidence: {signal.get('confidence')}%")
    print(f"Updated at: {signal.get('updated_at')}")
    return True

def test_trading_signals():
    """Test trading signals endpoint"""
    print("\n3. Testing get_trading_signals() function...")
    signals = tm_api.get_trading_signals(symbol="btc", limit=3)
    
    if "error" in signals:
        print(f"❌ Error: {signals['error']}")
        return False
    
    print("✅ Successfully retrieved trading signals")
    
    if "data" in signals and signals["data"]:
        for i, signal in enumerate(signals["data"], 1):
            symbol = signal.get("TOKEN_SYMBOL", "Unknown")
            trading_signal = signal.get("TRADING_SIGNAL", "Unknown")
            date = signal.get("DATE", "Unknown")
            print(f"{i}. {symbol} - Signal: {trading_signal}, Date: {date}")
    else:
        print("No trading signals data available")
    
    return True

def test_market_metrics():
    """Test fetching market metrics"""
    print("\n4. Testing get_market_metrics() function...")
    market = tm_api.get_market_metrics()
    
    if "error" in market:
        print(f"❌ Error: {market['error']}")
        return False
    
    print("✅ Successfully retrieved market metrics")
    
    if "data" in market and market["data"]:
        latest = market["data"][0]
        total_mcap = latest.get("TOTAL_CRYPTO_MCAP", 0)
        high_coins = latest.get("TM_GRADE_PERC_HIGH_COINS", 0)
        date = latest.get("DATE", "Unknown")
        print(f"Date: {date}")
        print(f"Total Market Cap: ${total_mcap/1000000000:.2f}B")
        print(f"Percentage of High Quality Coins: {high_coins:.2f}%")
    else:
        print("No market metrics data available")
    
    return True

def test_top_tokens():
    """Test alternative top tokens function"""
    print("\n5. Testing get_alternative_top_tokens() function...")
    tokens = tm_api.get_alternative_top_tokens(limit=3)
    
    if "error" in tokens:
        print(f"❌ Error: {tokens['error']}")
        return False
    
    print("✅ Successfully retrieved top tokens")
    
    if "data" in tokens and tokens["data"]:
        for i, token in enumerate(tokens["data"], 1):
            symbol = token.get("TOKEN_SYMBOL", "Unknown")
            grade = token.get("TM_TRADER_GRADE", 0)
            trading_signal = token.get("TRADING_SIGNAL", 0)
            print(f"{i}. {symbol} - Grade: {grade}%, Signal: {trading_signal}")
    else:
        print("No top tokens data available")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("TOKEN METRICS API V2 TEST SCRIPT")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("TM_API_KEY")
    if not api_key:
        print("❌ Error: TM_API_KEY environment variable not set")
        print("Please create a .env file with your Token Metrics API key")
        exit(1)
    
    # Run tests
    connection = test_api_connection()
    
    if connection:
        test_signal_generation()
        test_trading_signals()
        test_market_metrics()
        test_top_tokens()
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)