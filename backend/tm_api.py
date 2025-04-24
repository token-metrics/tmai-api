import os
import requests
from datetime import datetime, timedelta
import logging

class TokenMetricsClient:
    """
    Client for interacting with the Token Metrics API.
    Handles authentication and provides methods for accessing different endpoints.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Token Metrics API client.
        
        Args:
            api_key (str, optional): API key for Token Metrics. Defaults to environment variable.
        """
        self.api_key = api_key or os.getenv("TM_API_KEY", "hack-b3f7d3e9-421d-47a3-b4e0-44dca99c0f0d")
        self.base_url = "https://api.tokenmetrics.com/v2"
        self.headers = {
            "accept": "application/json",
            "api_key": self.api_key
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_tokens(self, symbols=None, token_ids=None, category=None, exchange=None, limit=100, page=0):
        """
        Get information about tokens.
        
        Args:
            symbols (str, optional): Comma-separated token symbols (e.g., "BTC,ETH").
            token_ids (str, optional): Comma-separated token IDs.
            category (str, optional): Filter by category.
            exchange (str, optional): Filter by exchange.
            limit (int, optional): Maximum number of results to return.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Token data response.
        """
        url = f"{self.base_url}/tokens"
        params = {"limit": limit, "page": page}
        
        if symbols:
            params["symbol"] = symbols
        if token_ids:
            params["token_id"] = token_ids
        if category:
            params["category"] = category
        if exchange:
            params["exchange"] = exchange
            
        return self._make_request(url, params)
    
    def get_top_tokens(self, top_k=20, page=0):
        """
        Get top tokens by market cap.
        
        Args:
            top_k (int, optional): Number of top tokens to retrieve.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Top tokens data response.
        """
        url = f"{self.base_url}/top-market-cap-tokens"
        params = {"top_k": top_k, "page": page}
        
        return self._make_request(url, params)
    
    def get_trading_signals(self, symbols=None, token_ids=None, category=None, 
                          start_date=None, end_date=None, signal=None, limit=100, page=0):
        """
        Get trading signals for tokens.
        
        Args:
            symbols (str, optional): Comma-separated token symbols.
            token_ids (str, optional): Comma-separated token IDs.
            category (str, optional): Filter by category.
            start_date (str, optional): Start date in YYYY-MM-DD format.
            end_date (str, optional): End date in YYYY-MM-DD format.
            signal (str, optional): Filter by signal value (1: bullish, -1: bearish, 0: neutral).
            limit (int, optional): Maximum number of results to return.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Trading signals data response.
        """
        url = f"{self.base_url}/trading-signals"
        
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "page": page
        }
        
        if symbols:
            params["symbol"] = symbols
        if token_ids:
            params["token_id"] = token_ids
        if category:
            params["category"] = category
        if signal:
            params["signal"] = signal
            
        return self._make_request(url, params)
    
    def get_trader_grades(self, symbols=None, token_ids=None, category=None,
                         start_date=None, end_date=None, limit=100, page=0):
        """
        Get trader grades for tokens.
        
        Args:
            symbols (str, optional): Comma-separated token symbols.
            token_ids (str, optional): Comma-separated token IDs.
            category (str, optional): Filter by category.
            start_date (str, optional): Start date in YYYY-MM-DD format.
            end_date (str, optional): End date in YYYY-MM-DD format.
            limit (int, optional): Maximum number of results to return.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Trader grades data response.
        """
        url = f"{self.base_url}/trader-grades"
        
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "page": page
        }
        
        if symbols:
            params["symbol"] = symbols
        if token_ids:
            params["token_id"] = token_ids
        if category:
            params["category"] = category
            
        return self._make_request(url, params)
    
    def get_price(self, token_ids=None, symbols=None):
        """
        Get current prices for tokens.
        
        Args:
            token_ids (str, optional): Comma-separated token IDs.
            symbols (str, optional): Comma-separated token symbols.
            
        Returns:
            dict: Price data response.
        """
        url = f"{self.base_url}/price"
        params = {}
        
        if token_ids:
            params["token_id"] = token_ids
        elif symbols:
            # If symbols are provided, first fetch token_ids
            tokens_data = self.get_tokens(symbols=symbols)
            if 'data' in tokens_data and tokens_data['data']:
                token_id_list = [str(token.get('TOKEN_ID')) for token in tokens_data['data']]
                params["token_id"] = ",".join(token_id_list)
            else:
                self.logger.warning(f"No token IDs found for symbols: {symbols}")
                return {"error": f"No token IDs found for symbols: {symbols}"}
                
        return self._make_request(url, params)
    
    def get_market_metrics(self, start_date=None, end_date=None, limit=30, page=0):
        """
        Get market metrics.
        
        Args:
            start_date (str, optional): Start date in YYYY-MM-DD format.
            end_date (str, optional): End date in YYYY-MM-DD format.
            limit (int, optional): Maximum number of results to return.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Market metrics data response.
        """
        url = f"{self.base_url}/market-metrics"
        
        # Set default dates if not provided
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "page": page
        }
            
        return self._make_request(url, params)
    
    def get_crypto_investors(self, limit=100, page=0):
        """
        Get crypto investors data.
        
        Args:
            limit (int, optional): Maximum number of results to return.
            page (int, optional): Page number for pagination.
            
        Returns:
            dict: Crypto investors data response.
        """
        url = f"{self.base_url}/crypto-investors"
        params = {
            "limit": limit,
            "page": page
        }
            
        return self._make_request(url, params)
    
    def ask_ai_agent(self, question):
        """
        Ask a question to the Token Metrics AI agent.
        
        Args:
            question (str): The question to ask.
            
        Returns:
            dict: AI agent response.
        """
        url = f"{self.base_url}/tmai"
        payload = {
            "messages": [
                {"user": question}
            ]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error querying AI agent: {e}")
            return {"error": str(e)}
    
    def _make_request(self, url, params=None):
        """
        Make a request to the Token Metrics API.
        
        Args:
            url (str): The API endpoint URL.
            params (dict, optional): Query parameters.
            
        Returns:
            dict: API response data.
        """
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request error: {e}")
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    client = TokenMetricsClient()
    
    # Test getting top tokens
    top_tokens = client.get_top_tokens(top_k=5)
    print("Top Tokens:", top_tokens)
    
    # Test getting price data for Bitcoin
    btc_price = client.get_price(symbols="BTC")
    print("BTC Price:", btc_price) 