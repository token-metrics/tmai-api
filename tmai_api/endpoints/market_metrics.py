from tmai_api.base import BaseEndpoint

class MarketMetricsEndpoint(BaseEndpoint):
    """Endpoint for accessing market sentiment metrics"""
    
    def get(self, startDate=None, endDate=None, limit=1000, page=0):
        """Get the Market Analytics from Token Metrics.
        
        These provide insight into the full Crypto Market, including the Bullish/Bearish Market indicator.
        
        Args:
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Market metrics data
        """
        params = {
            'startDate': startDate,
            'endDate': endDate,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'market-metrics', params)
    
    def get_dataframe(self, **kwargs):
        """Get market metrics data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing market metrics data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
