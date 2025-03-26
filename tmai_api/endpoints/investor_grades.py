from tmai_api.base import BaseEndpoint

class InvestorGradesEndpoint(BaseEndpoint):
    """Endpoint for accessing long-term investment grades"""
    
    def get(self, token_id=None, startDate=None, endDate=None, symbol=None,
            category=None, exchange=None, marketcap=None, fdv=None, 
            volume=None, investorGrade=None, limit=1000, page=0):
        """Get the long-term investment grades, including Technology and Fundamental metrics.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            category (str, optional): Comma-separated category names
            exchange (str, optional): Comma-separated exchange names
            marketcap (str, optional): Minimum MarketCap in $
            fdv (str, optional): Minimum fully diluted valuation in $
            volume (str, optional): Minimum 24h trading volume in $
            investorGrade (str, optional): Minimum TM Investor Grade
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Investor grades data
        """
        params = {
            'token_id': token_id,
            'startDate': startDate,
            'endDate': endDate,
            'symbol': symbol,
            'category': category,
            'exchange': exchange,
            'marketcap': marketcap,
            'fdv': fdv,
            'volume': volume,
            'investorGrade': investorGrade,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'investor-grades', params)
    
    def get_dataframe(self, **kwargs):
        """Get investor grades data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing investor grades data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
