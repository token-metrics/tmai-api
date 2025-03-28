from tmai_api.base import BaseEndpoint

class MarketMetricsEndpoint(BaseEndpoint):
    """Endpoint for accessing market sentiment metrics"""
    
    def get(self, startDate=None, endDate=None):
        """Get the Market Analytics from Token Metrics with automatic date chunking and pagination.
        
        These provide insight into the full Crypto Market, including the Bullish/Bearish Market indicator.
        
        Args:
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            
        Returns:
            dict: Market metrics data with all pages and date ranges combined
            
        Note:
            This method handles the API's 29-day limit limitation by:
            1. Automatically chunking the date range into 29-day periods
            2. Displaying a progress bar during fetching
            3. Combining all results into a single response
        """
        params = {
            'startDate': startDate,
            'endDate': endDate
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._paginated_request('get', 'market-metrics', params, max_days=29)
    
    def get_dataframe(self, **kwargs):
        """Get market metrics data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing market metrics data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
