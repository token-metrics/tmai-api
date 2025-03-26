from tmai_api.base import BaseEndpoint

class AIReportsEndpoint(BaseEndpoint):
    """Endpoint for accessing AI-generated trading and investment reports"""
    
    def get(self, token_id=None, symbol=None, limit=1000, page=0):
        """Get the latest AI-generated trading and investment reports.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: AI reports data
        """
        params = {
            'token_id': token_id,
            'symbol': symbol,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'ai-reports', params)
    
    def get_dataframe(self, **kwargs):
        """Get AI reports data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing AI reports data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)