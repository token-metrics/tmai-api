from tmai_api.base import BaseEndpoint

class DailyOHLCVEndpoint(BaseEndpoint):
    """Endpoint for accessing daily OHLCV (Open, High, Low, Close, Volume) data"""
    
    def get(self, token_id=None, symbol=None, token_name=None, 
            startDate=None, endDate=None):
        """Get daily OHLCV data for tokens with automatic date chunking and pagination.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            token_name (str, optional): Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            
        Returns:
            dict: Daily OHLCV data with all pages and date ranges combined
            
        Note:
            This method handles the API's 29-day limit limitation by:
            1. Automatically chunking the date range into 29-day periods
            2. Displaying a progress bar during fetching
            3. Combining all results into a single response
        """
        params = {
            'token_id': token_id,
            'symbol': symbol,
            'token_name': token_name,
            'startDate': startDate,
            'endDate': endDate
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        # Use custom pagination logic with a 29-day maximum range
        return self._paginated_request('get', 'daily-ohlcv', params, max_days=29)
    
    def get_dataframe(self, **kwargs):
        """Get daily OHLCV data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing daily OHLCV data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)