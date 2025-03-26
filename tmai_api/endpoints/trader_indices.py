from tmai_api.base import BaseEndpoint

class TraderIndicesEndpoint(BaseEndpoint):
    """Endpoint for accessing AI-generated trading portfolios"""
    
    def get(self, startDate=None, endDate=None, limit=1000, page=0):
        """Get the AI-generated portfolio for Traders, updated Daily.
        
        Args:
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Trader indices data
        """
        params = {
            'startDate': startDate,
            'endDate': endDate,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'trader-indices', params)
    
    def get_dataframe(self, **kwargs):
        """Get trader indices data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing trader indices data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
