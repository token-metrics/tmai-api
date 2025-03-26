from tmai_api.base import BaseEndpoint

class TraderGradesEndpoint(BaseEndpoint):
    """Endpoint for accessing short-term trading grades"""
    
    def get(self, token_id=None, startDate=None, endDate=None, symbol=None,
            category=None, exchange=None, marketcap=None, fdv=None, 
            volume=None, traderGrade=None, traderGradePercentChange=None,
            limit=1000, page=0):
        """Get the short-term trading grades, including the 24h percent change for the TM Trader Grade.
        
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
            traderGrade (str, optional): Minimum TM Trader Grade
            traderGradePercentChange (str, optional): Minimum 24h percent change in TM Trader Grade
            limit (int, optional): Limit the number of items in response
            page (int, optional): Page number for pagination
            
        Returns:
            dict: Trader grades data
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
            'traderGrade': traderGrade,
            'traderGradePercentChange': traderGradePercentChange,
            'limit': limit,
            'page': page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._request('get', 'trader-grades', params)
    
    def get_dataframe(self, **kwargs):
        """Get trader grades data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing trader grades data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)
