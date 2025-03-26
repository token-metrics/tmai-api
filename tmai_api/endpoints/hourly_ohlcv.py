from tmai_api.base import BaseEndpoint

class HourlyOHLCVEndpoint(BaseEndpoint):
    """Endpoint for accessing hourly OHLCV (Open, High, Low, Close, Volume) data"""
    
    def get(self, token_id=None, symbol=None, token_name=None, 
            startDate=None, endDate=None, limit=1000, page=0):
        """Get hourly OHLCV data for tokens.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            token_name (str, optional): Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Hourly OHLCV data
        """
        params = {
            'token_id': token_id,
            'symbol': symbol,
            'token_name': token_name,
            'startDate': startDate,
            'endDate': endDate,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'hourly-ohlcv', params)
    
    def get_dataframe(self, **kwargs):
        """Get hourly OHLCV data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing hourly OHLCV data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
