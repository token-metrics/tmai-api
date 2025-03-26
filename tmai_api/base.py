import requests
import pandas as pd

class BaseEndpoint:
    """Base class for all API endpoints"""
    
    def __init__(self, client):
        """Initialize the endpoint with a client instance.
        
        Args:
            client: TokenMetricsClient instance
        """
        self.client = client
        self.base_url = client.BASE_URL
    
    def _request(self, method, endpoint, params=None, json=None):
        """Make a request to the API.
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters for GET requests
            json (dict, optional): JSON payload for POST requests
            
        Returns:
            dict: API response data
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "accept": "application/json",
            "api_key": self.client.api_key
        }
        
        if method.lower() == "get":
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == "post":
            headers["content-type"] = "application/json"
            response = requests.post(url, headers=headers, json=json)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Raise an exception if the request failed
        response.raise_for_status()
        
        return response.json()
    
    def to_dataframe(self, data):
        """Convert API response data to a pandas DataFrame.
        
        Args:
            data (dict): API response data
            
        Returns:
            pandas.DataFrame: DataFrame containing the response data
        """
        # Implementation depends on the specific structure of each endpoint's response
        # This is a placeholder to be overridden by subclasses
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            return pd.DataFrame(data["data"])
        else:
            return pd.DataFrame([data])
