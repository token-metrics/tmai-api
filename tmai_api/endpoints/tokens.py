from tmai_api.base import BaseEndpoint

class TokensEndpoint(BaseEndpoint):
    """Endpoint for accessing token information"""
    
    def get(self, token_id=None, token_name=None, symbol=None, category=None, 
            exchange=None, blockchain_address=None, limit=1000, page=0):
        """Get the list of tokens supported by Token Metrics.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            token_name (str, optional): Comma-separated Token Names (e.g., "Bitcoin, Ethereum")
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            category (str, optional): Comma-separated category names
            exchange (str, optional): Comma-separated exchange names
            blockchain_address (str, optional): Blockchain name and contract address
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Token information
        """
        params = {
            'token_id': token_id,
            'token_name': token_name,
            'symbol': symbol,
            'category': category,
            'exchange': exchange,
            'blockchain_address': blockchain_address,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'tokens', params)
    
    def get_dataframe(self, **kwargs):
        """Get token information as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing token information
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
