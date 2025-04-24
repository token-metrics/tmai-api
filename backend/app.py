from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta

from tm_api import TokenMetricsClient
from portfolio import PortfolioManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize our API client and portfolio manager
client = TokenMetricsClient()
portfolio_manager = PortfolioManager(client)

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/api/tokens", methods=["GET"])
def get_tokens():
    """Get tokens with optional filtering."""
    symbols = request.args.get("symbols")
    token_ids = request.args.get("token_ids")
    category = request.args.get("category")
    exchange = request.args.get("exchange")
    limit = int(request.args.get("limit", 100))
    page = int(request.args.get("page", 0))
    
    result = client.get_tokens(
        symbols=symbols,
        token_ids=token_ids,
        category=category,
        exchange=exchange,
        limit=limit,
        page=page
    )
    
    return jsonify(result)

@app.route("/api/tokens/top", methods=["GET"])
def get_top_tokens():
    """Get top tokens by market cap."""
    top_k = int(request.args.get("top_k", 20))
    page = int(request.args.get("page", 0))
    
    result = client.get_top_tokens(top_k=top_k, page=page)
    
    return jsonify(result)

@app.route("/api/trading-signals", methods=["GET"])
def get_trading_signals():
    """Get trading signals for tokens."""
    symbols = request.args.get("symbols")
    token_ids = request.args.get("token_ids")
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    signal = request.args.get("signal")
    limit = int(request.args.get("limit", 100))
    page = int(request.args.get("page", 0))
    
    result = client.get_trading_signals(
        symbols=symbols,
        token_ids=token_ids,
        category=category,
        start_date=start_date,
        end_date=end_date,
        signal=signal,
        limit=limit,
        page=page
    )
    
    return jsonify(result)

@app.route("/api/trader-grades", methods=["GET"])
def get_trader_grades():
    """Get trader grades for tokens."""
    symbols = request.args.get("symbols")
    token_ids = request.args.get("token_ids")
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    limit = int(request.args.get("limit", 100))
    page = int(request.args.get("page", 0))
    
    result = client.get_trader_grades(
        symbols=symbols,
        token_ids=token_ids,
        category=category,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        page=page
    )
    
    return jsonify(result)

@app.route("/api/market-metrics", methods=["GET"])
def get_market_metrics():
    """Get market metrics."""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    limit = int(request.args.get("limit", 30))
    page = int(request.args.get("page", 0))
    
    result = client.get_market_metrics(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        page=page
    )
    
    return jsonify(result)

@app.route("/api/portfolio/analyze", methods=["POST"])
def analyze_portfolio():
    """Analyze a portfolio of cryptocurrency holdings."""
    data = request.json
    
    if not data or "holdings" not in data:
        return jsonify({"error": "No holdings provided"}), 400
    
    holdings = data.get("holdings", {})
    
    result = portfolio_manager.analyze_portfolio(holdings)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route("/api/portfolio/optimize", methods=["POST"])
def optimize_portfolio():
    """Optimize a portfolio based on Token Metrics signals and risk tolerance."""
    data = request.json
    
    if not data or "holdings" not in data:
        return jsonify({"error": "No holdings provided"}), 400
    
    holdings = data.get("holdings", {})
    risk_tolerance = data.get("risk_tolerance", "medium")
    
    result = portfolio_manager.optimize_portfolio(holdings, risk_tolerance)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route("/api/tokens/recommended", methods=["GET"])
def get_recommended_tokens():
    """Get recommended tokens based on Token Metrics signals."""
    top_k = int(request.args.get("top_k", 10))
    
    result = portfolio_manager.get_recommended_tokens(top_k=top_k)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route("/api/ai/ask", methods=["POST"])
def ask_ai_agent():
    """Ask a question to the Token Metrics AI agent."""
    data = request.json
    
    if not data or "question" not in data:
        return jsonify({"error": "No question provided"}), 400
    
    question = data.get("question")
    
    result = client.ask_ai_agent(question)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

@app.route("/api/price", methods=["GET"])
def get_price():
    """Get current prices for tokens."""
    symbols = request.args.get("symbols")
    token_ids = request.args.get("token_ids")
    
    result = client.get_price(token_ids=token_ids, symbols=symbols)
    
    return jsonify(result)

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Debug mode for development
    debug = os.environ.get("FLASK_ENV") == "development"
    
    app.run(host="0.0.0.0", port=port, debug=debug) 