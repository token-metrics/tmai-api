import requests
import jwt
from datetime import datetime, timedelta

class TokenMetricsOpenAI:
    """
    Token Metrics AI helper library for OpenAI Agents
    """
    
    BASE_URL = "https://api.tokenmetrics.com/v2"
    
    def __init__(self, api_key=None, jwt_token=None):
        """
        Initialize the Token Metrics OpenAI client
        
        Args:
            api_key (str): Your Token Metrics API key
            jwt_token (str): JWT token with required claims
        """
        self.api_key = api_key
        self.jwt_token = jwt_token
    
    def _get_headers(self):
        """
        Get headers for API requests
        
        Returns:
            dict: Headers for API requests
        """
        headers = {
            "accept": "application/json",
        }
        
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        elif self.api_key:
            headers["api_key"] = self.api_key
        
        return headers
    
    def get_ratings(self, symbol, start_date=None, end_date=None):
        """
        Get cryptocurrency ratings
        
        Args:
            symbol (str): Token symbol (e.g., "BTC")
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Ratings data
        """
        params = {"symbol": symbol}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = requests.get(
            f"{self.BASE_URL}/ratings",
            headers=self._get_headers(),
            params=params
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self, symbol, start_date=None, end_date=None):
        """
        Get cryptocurrency metrics
        
        Args:
            symbol (str): Token symbol (e.g., "BTC")
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Factors data
        """
        params = {"symbol": symbol}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = requests.get(
            f"{self.BASE_URL}/metrics",
            headers=self._get_headers(),
            params=params
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_sentiment(self, symbol, start_date=None, end_date=None):
        """
        Get cryptocurrency sentiment
        
        Args:
            symbol (str): Token symbol (e.g., "BTC")
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Sentiment data
        """
        params = {"symbol": symbol}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = requests.get(
            f"{self.BASE_URL}/sentiments",
            headers=self._get_headers(),
            params=params
        )
        
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def create_jwt(plan, payment_method, stake_score, secret_key, expiration_hours=1):
        """
        Create a JWT token with required claims
        
        Args:
            plan (str): User subscription plan
            payment_method (str): Payment method used
            stake_score (float): Staking score for discounts
            secret_key (str): Secret key for signing the JWT
            expiration_hours (int): Token expiration in hours
            
        Returns:
            str: JWT token
        """
        payload = {
            "plan": plan,
            "payment_method": payment_method,
            "stake_score": stake_score,
            "exp": datetime.utcnow() + timedelta(hours=expiration_hours)
        }
        
        return jwt.encode(payload, secret_key, algorithm="HS256")
