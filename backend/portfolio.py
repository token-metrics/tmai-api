import json
from datetime import datetime, timedelta
from tm_api import TokenMetricsClient

class PortfolioManager:
    """
    Portfolio management class that leverages Token Metrics API for analysis and optimization.
    """
    
    def __init__(self, api_client=None):
        """
        Initialize the portfolio manager.
        
        Args:
            api_client (TokenMetricsClient, optional): Token Metrics API client instance.
        """
        self.client = api_client or TokenMetricsClient()
        
    def analyze_portfolio(self, holdings):
        """
        Analyze a portfolio of cryptocurrency holdings.
        
        Args:
            holdings (dict): Dictionary of holdings {symbol: amount}
            
        Returns:
            dict: Portfolio analysis with values, performance metrics, and recommendations
        """
        if not holdings:
            return {"error": "No holdings provided"}
        
        # Get symbols and fetch token information
        symbols = ",".join(holdings.keys())
        tokens_data = self.client.get_tokens(symbols=symbols)
        
        if "error" in tokens_data:
            return tokens_data
        
        if not tokens_data.get("data"):
            return {"error": "No token data found for the provided symbols"}
        
        # Get token IDs for price lookup
        token_ids = [str(token.get("TOKEN_ID")) for token in tokens_data.get("data", [])]
        token_id_str = ",".join(token_ids)
        
        # Get current prices
        prices = self.client.get_price(token_ids=token_id_str)
        
        if "error" in prices:
            return prices
        
        if not prices.get("data"):
            return {"error": "Could not fetch price data for the provided tokens"}
        
        # Prepare portfolio analysis
        portfolio = {
            "total_value": 0,
            "assets": [],
            "metrics": {},
            "recommendations": []
        }
        
        # Get trading signals for recommendations
        signals = self.client.get_trading_signals(symbols=symbols)
        
        # Create a mapping of TOKEN_ID to data for easy lookup
        price_map = {item.get("TOKEN_ID"): item for item in prices.get("data", [])}
        signal_map = {}
        for signal in signals.get("data", []):
            token_symbol = signal.get("TOKEN_SYMBOL")
            if token_symbol and token_symbol not in signal_map:
                signal_map[token_symbol] = signal
        
        # Calculate portfolio values and recommendations
        for token in tokens_data.get("data", []):
            token_id = token.get("TOKEN_ID")
            symbol = token.get("TOKEN_SYMBOL")
            
            if symbol not in holdings:
                continue
                
            amount = holdings[symbol]
            price_data = price_map.get(token_id, {})
            current_price = price_data.get("PRICE", 0)
            value = amount * current_price
            portfolio["total_value"] += value
            
            # Get signal data for this token
            signal_data = signal_map.get(symbol, {})
            trading_signal = signal_data.get("TRADING_SIGNAL", 0)
            trader_grade = signal_data.get("TM_TRADER_GRADE", 50)
            
            # Generate recommendation based on signal
            recommendation = self._generate_recommendation(symbol, trading_signal, trader_grade)
            if recommendation:
                portfolio["recommendations"].append(recommendation)
            
            # Add asset details to portfolio
            portfolio["assets"].append({
                "symbol": symbol,
                "name": token.get("NAME", ""),
                "amount": amount,
                "price": current_price,
                "value": value,
                "weight": 0,  # Will calculate after total is known
                "signal": trading_signal,
                "grade": trader_grade
            })
        
        # Calculate portfolio weights and metrics
        for asset in portfolio["assets"]:
            if portfolio["total_value"] > 0:
                asset["weight"] = (asset["value"] / portfolio["total_value"]) * 100
                
        # Calculate overall portfolio metrics
        portfolio["metrics"] = self._calculate_metrics(portfolio["assets"])
        
        # Generate rebalancing suggestions
        portfolio["rebalancing"] = self._generate_rebalancing(portfolio["assets"])
        
        return portfolio
    
    def _generate_recommendation(self, symbol, signal, grade):
        """
        Generate a recommendation based on trading signal and trader grade.
        
        Args:
            symbol (str): Token symbol
            signal (int): Trading signal (1: buy, -1: sell, 0: hold)
            grade (float): Trader grade
            
        Returns:
            dict: Recommendation or None if no strong recommendation
        """
        if signal == 1 and grade >= 70:
            return {
                "symbol": symbol,
                "action": "BUY",
                "strength": "Strong",
                "reason": f"Strong buy signal with high trader grade ({grade})"
            }
        elif signal == 1 and grade >= 50:
            return {
                "symbol": symbol,
                "action": "BUY",
                "strength": "Moderate",
                "reason": f"Buy signal with moderate trader grade ({grade})"
            }
        elif signal == -1 and grade <= 30:
            return {
                "symbol": symbol,
                "action": "SELL",
                "strength": "Strong",
                "reason": f"Strong sell signal with low trader grade ({grade})"
            }
        elif signal == -1 and grade <= 50:
            return {
                "symbol": symbol,
                "action": "SELL",
                "strength": "Moderate",
                "reason": f"Sell signal with moderate trader grade ({grade})"
            }
        return None
    
    def _calculate_metrics(self, assets):
        """
        Calculate overall portfolio metrics.
        
        Args:
            assets (list): List of portfolio assets
            
        Returns:
            dict: Portfolio metrics
        """
        avg_grade = 0
        weighted_grade = 0
        buy_signals = 0
        sell_signals = 0
        hold_signals = 0
        total_value = sum(asset["value"] for asset in assets)
        
        for asset in assets:
            grade = asset.get("grade", 50)
            weight = asset.get("weight", 0)
            signal = asset.get("signal", 0)
            
            avg_grade += grade
            weighted_grade += grade * weight / 100
            
            if signal == 1:
                buy_signals += 1
            elif signal == -1:
                sell_signals += 1
            else:
                hold_signals += 1
        
        if assets:
            avg_grade /= len(assets)
        
        return {
            "average_grade": avg_grade,
            "weighted_grade": weighted_grade,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
            "hold_signals": hold_signals,
            "total_assets": len(assets),
            "total_value": total_value,
            "sentiment": "Bullish" if weighted_grade >= 70 else "Bearish" if weighted_grade <= 30 else "Neutral"
        }
    
    def _generate_rebalancing(self, assets):
        """
        Generate portfolio rebalancing suggestions based on trading signals.
        
        Args:
            assets (list): List of portfolio assets
            
        Returns:
            dict: Rebalancing suggestions
        """
        high_grade_assets = []
        low_grade_assets = []
        
        for asset in assets:
            grade = asset.get("grade", 50)
            signal = asset.get("signal", 0)
            
            if signal == 1 and grade >= 70:
                high_grade_assets.append(asset)
            elif signal == -1 and grade <= 30:
                low_grade_assets.append(asset)
        
        # Sort by grade (descending for high grade, ascending for low grade)
        high_grade_assets.sort(key=lambda x: x.get("grade", 0), reverse=True)
        low_grade_assets.sort(key=lambda x: x.get("grade", 0))
        
        rebalance = {
            "increase": [{"symbol": asset["symbol"], "target_weight": min(asset["weight"] * 1.5, asset["weight"] + 10)} for asset in high_grade_assets],
            "decrease": [{"symbol": asset["symbol"], "target_weight": max(asset["weight"] * 0.5, asset["weight"] - 10)} for asset in low_grade_assets]
        }
        
        return rebalance
    
    def optimize_portfolio(self, holdings, risk_tolerance="medium"):
        """
        Optimize a portfolio based on Token Metrics signals and risk tolerance.
        
        Args:
            holdings (dict): Dictionary of holdings {symbol: amount}
            risk_tolerance (str): Risk tolerance level ("low", "medium", "high")
            
        Returns:
            dict: Optimized portfolio allocation
        """
        if not holdings:
            return {"error": "No holdings provided"}
        
        # Analyze current portfolio
        portfolio = self.analyze_portfolio(holdings)
        
        if "error" in portfolio:
            return portfolio
        
        # Risk tolerance factors
        risk_factors = {
            "low": {"grade_threshold": 60, "increase_percent": 5, "decrease_percent": 15},
            "medium": {"grade_threshold": 70, "increase_percent": 10, "decrease_percent": 20},
            "high": {"grade_threshold": 80, "increase_percent": 20, "decrease_percent": 30}
        }
        
        # Use default if invalid risk tolerance
        factor = risk_factors.get(risk_tolerance.lower(), risk_factors["medium"])
        
        # Calculate optimized weights
        total_value = portfolio["total_value"]
        current_allocation = {asset["symbol"]: asset["value"] / total_value for asset in portfolio["assets"]}
        optimized_allocation = current_allocation.copy()
        
        # Find candidates for increase/decrease
        increase_candidates = []
        decrease_candidates = []
        
        for asset in portfolio["assets"]:
            symbol = asset["symbol"]
            grade = asset.get("grade", 50)
            signal = asset.get("signal", 0)
            
            if signal == 1 and grade >= factor["grade_threshold"]:
                increase_candidates.append(asset)
            elif signal == -1 or grade < 40:
                decrease_candidates.append(asset)
        
        # Calculate weight to redistribute
        weight_to_redistribute = 0
        for asset in decrease_candidates:
            symbol = asset["symbol"]
            current_weight = current_allocation[symbol]
            decrease_amount = current_weight * (factor["decrease_percent"] / 100)
            optimized_allocation[symbol] -= decrease_amount
            weight_to_redistribute += decrease_amount
        
        # Redistribute weight to increase candidates
        if increase_candidates and weight_to_redistribute > 0:
            # Normalize by grade
            total_grade_points = sum(max(0, asset["grade"] - 50) for asset in increase_candidates)
            
            if total_grade_points > 0:
                for asset in increase_candidates:
                    symbol = asset["symbol"]
                    grade_points = max(0, asset["grade"] - 50)
                    weight_share = (grade_points / total_grade_points) * weight_to_redistribute
                    optimized_allocation[symbol] += weight_share
        
        # Convert to percentage format and calculate USD values
        optimized_portfolio = {
            "current": {symbol: {"percent": current_allocation[symbol] * 100, "value": current_allocation[symbol] * total_value} for symbol in current_allocation},
            "optimized": {symbol: {"percent": optimized_allocation[symbol] * 100, "value": optimized_allocation[symbol] * total_value} for symbol in optimized_allocation},
            "actions": [],
            "risk_tolerance": risk_tolerance
        }
        
        # Generate actions
        for symbol in optimized_allocation:
            current = current_allocation[symbol]
            optimized = optimized_allocation[symbol]
            
            if abs(optimized - current) < 0.01:  # Less than 1% change
                action = "HOLD"
            elif optimized > current:
                action = "INCREASE"
            else:
                action = "DECREASE"
                
            delta_percent = (optimized - current) * 100
            delta_value = delta_percent * total_value / 100
                
            optimized_portfolio["actions"].append({
                "symbol": symbol,
                "action": action,
                "delta_percent": delta_percent,
                "delta_value": delta_value
            })
        
        return optimized_portfolio
    
    def get_recommended_tokens(self, top_k=10):
        """
        Get recommended tokens based on Token Metrics signals.
        
        Args:
            top_k (int): Number of recommendations to return
            
        Returns:
            dict: Recommended tokens
        """
        # Get top tokens by market cap
        top_tokens = self.client.get_top_tokens(top_k=top_k*3)  # Get more to filter
        
        if "error" in top_tokens or not top_tokens.get("data"):
            return {"error": "Could not fetch top tokens"}
        
        # Extract token symbols
        symbols = [token.get("TOKEN_SYMBOL") for token in top_tokens.get("data", [])]
        symbol_str = ",".join(symbols)
        
        # Get trading signals for these tokens
        signals = self.client.get_trading_signals(symbols=symbol_str)
        
        if "error" in signals or not signals.get("data"):
            return {"error": "Could not fetch trading signals"}
        
        # Filter tokens with buy signals and high grades
        buy_signals = [signal for signal in signals.get("data", []) 
                     if signal.get("TRADING_SIGNAL") == 1 and signal.get("TM_TRADER_GRADE", 0) >= 60]
        
        # Sort by grade (highest first)
        buy_signals.sort(key=lambda x: x.get("TM_TRADER_GRADE", 0), reverse=True)
        
        # Limit to top_k
        recommendations = buy_signals[:top_k]
        
        # Prepare response
        result = {
            "recommendations": []
        }
        
        for rec in recommendations:
            symbol = rec.get("TOKEN_SYMBOL")
            grade = rec.get("TM_TRADER_GRADE", 0)
            
            # Look up additional info from top_tokens
            token_info = next((t for t in top_tokens.get("data", []) if t.get("TOKEN_SYMBOL") == symbol), {})
            
            result["recommendations"].append({
                "symbol": symbol,
                "name": token_info.get("NAME", ""),
                "grade": grade,
                "market_cap": token_info.get("MARKET_CAP", 0),
                "signal": "BUY",
                "confidence": grade
            })
        
        return result


# Example usage
if __name__ == "__main__":
    portfolio_manager = PortfolioManager()
    
    # Test portfolio analysis
    sample_portfolio = {
        "BTC": 0.5,
        "ETH": 5.0,
        "SOL": 10.0,
        "ADA": 1000.0
    }
    
    analysis = portfolio_manager.analyze_portfolio(sample_portfolio)
    print(json.dumps(analysis, indent=2))
    
    # Test portfolio optimization
    optimized = portfolio_manager.optimize_portfolio(sample_portfolio, risk_tolerance="medium")
    print(json.dumps(optimized, indent=2))
    
    # Test getting recommended tokens
    recommendations = portfolio_manager.get_recommended_tokens(top_k=5)
    print(json.dumps(recommendations, indent=2)) 