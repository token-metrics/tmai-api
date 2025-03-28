import requests
import pandas as pd
import datetime
from tqdm import tqdm

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
    
    def _chunk_date_range(self, startDate, endDate, max_days=29):
        """Split a date range into chunks of max_days.
        
        Args:
            startDate (str): Start date in YYYY-MM-DD format
            endDate (str): End date in YYYY-MM-DD format
            max_days (int): Maximum number of days in each chunk
            
        Returns:
            list: List of (chunk_start_date, chunk_end_date) tuples
        """
        if not startDate or not endDate:
            return [(startDate, endDate)]  # If dates not provided, return as is
            
        try:
            start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
            end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        except ValueError:
            # If date parsing fails, return as is
            return [(startDate, endDate)]
            
        # Check if the range is already within limits
        if (end - start).days <= max_days:
            return [(startDate, endDate)]
            
        # Split into chunks
        result = []
        chunk_start = start
        
        while chunk_start < end:
            # Calculate chunk end date (chunk_start + max_days or end date, whichever is earlier)
            chunk_end = min(chunk_start + datetime.timedelta(days=max_days), end)
            
            # Add to result as strings
            result.append((
                chunk_start.strftime("%Y-%m-%d"),
                chunk_end.strftime("%Y-%m-%d")
            ))
            
            # Move to next chunk
            chunk_start = chunk_end
            
        return result
    
    def _paginated_request(self, method, endpoint, params=None, max_days=29, custom_limit=None):
        """Make paginated requests to handle date ranges and custom pagination logic.
        
        This method handles two forms of pagination:
        1. Date chunking: Splitting long date ranges into <= max_days chunks
        2. Offset-based pagination: Since the API's page parameter doesn't work as expected
        
        Args:
            method (str): HTTP method (get, post, etc.)
            endpoint (str): API endpoint path
            params (dict): Query parameters including startDate and endDate
            max_days (int): Maximum number of days allowed between startDate and endDate
            custom_limit (int, optional): Custom limit value. If None, uses endpoint-specific defaults.
            
        Returns:
            dict: Combined API response data
        """
        # Default limits for different endpoints
        endpoint_limits = {
            'daily-ohlcv': 100,
            'hourly-ohlcv': 1000,
            'trader-grades': 1000,
            'investor-grades': 1000,
            'market-metrics': 1000,
            'trader-indices': 1000,
            'trading-signals': 1000,
            # Default for any other endpoint
            'default': 1000
        }
        if params is None:
            params = {}
            
        # Extract date parameters
        startDate = params.get('startDate')
        endDate = params.get('endDate')
        
        # Determine the limit to use
        if custom_limit is not None:
            limit = custom_limit
        else:
            # Use endpoint-specific limit
            limit = endpoint_limits.get(endpoint, endpoint_limits['default'])
        
        # Override user-provided limit with our internal limit
        params['limit'] = limit
        
        # We'll remove page parameter since we're handling pagination ourselves
        if 'page' in params:
            del params['page']
            
        # If no date range or already within limits, we still need to handle pagination
        if not startDate or not endDate:
            date_chunks = [(startDate, endDate)]
        else:
            # Split date range into chunks
            date_chunks = self._chunk_date_range(startDate, endDate, max_days)
        
        # Initialize combined results
        all_data = []
        combined_meta = {}
        
        # Calculate total iterations for progress bar
        total_iterations = len(date_chunks)
        
        # Setup progress bar
        with tqdm(total=total_iterations, desc=f"Fetching {endpoint} data", unit="chunk") as pbar:
            # Process each date chunk
            for chunk_start, chunk_end in date_chunks:
                # Update date parameters
                chunk_params = params.copy()
                if chunk_start:
                    chunk_params['startDate'] = chunk_start
                if chunk_end:
                    chunk_params['endDate'] = chunk_end
                
                # Set a high limit to get as much data as possible in one request
                chunk_params['limit'] = limit
                
                # Always start with page 0 for each chunk
                chunk_params['page'] = 0
                
                # Get the first batch of data
                response = self._request(method, endpoint, chunk_params)
                
                # Extract and store the data
                if isinstance(response, dict):
                    if "data" in response:
                        data_items = response["data"]
                        if isinstance(data_items, list):
                            all_data.extend(data_items)
                        else:
                            all_data.append(data_items)
                    
                    # Store metadata for later if it exists
                    for key, value in response.items():
                        if key != "data":
                            combined_meta[key] = value
                else:
                    # If the response is not a dict with a data field, append it directly
                    if isinstance(response, list):
                        all_data.extend(response)
                    else:
                        all_data.append(response)
                
                # Update progress bar
                pbar.update(1)
        
        # Construct the final response
        if combined_meta:
            result = combined_meta.copy()
            result["data"] = all_data
            return result
        elif all_data and isinstance(all_data[0], dict) and not isinstance(response, list):
            # If we have data items and the original response was a dict
            return {"data": all_data}
        else:
            # Otherwise, return just the data array
            return all_data
    
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
