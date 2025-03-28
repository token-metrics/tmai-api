from tmai_api.base import BaseEndpoint

class TradingSignalsEndpoint(BaseEndpoint):
    """Endpoint for accessing AI-generated trading signals for long and short positions"""
    
    def get(self, token_id=None, symbol=None, startDate=None, endDate=None, 
            category=None, exchange=None, marketcap=None, volume=None, 
            fdv=None, signal=None):
        """Get AI-generated trading signals with automatic date chunking and pagination.
        
        Args:
            token_id (str, optional): Comma-separated Token IDs
            symbol (str, optional): Comma-separated Token Symbols (e.g., "BTC,ETH")
            startDate (str, optional): Start date in YYYY-MM-DD format
            endDate (str, optional): End date in YYYY-MM-DD format
            category (str, optional): Comma-separated category names (e.g., "layer-1,nft")
            exchange (str, optional): Comma-separated exchange names (e.g., "binance,gate")
            marketcap (str, optional): Minimum MarketCap in $
            volume (str, optional): Minimum 24h trading volume in $
            fdv (str, optional): Minimum fully diluted valuation in $
            signal (str, optional): Signal value: bullish (1), bearish (-1) or no signal (0)
            
        Returns:
            dict: Trading signals data with all pages and date ranges combined
            
        Note:
            This method handles the API's 29-day limit limitation by:
            1. Automatically chunking the date range into 29-day periods
            2. Displaying a progress bar during fetching
            3. Combining all results into a single response
        """
        params = {
            'token_id': token_id,
            'symbol': symbol,
            'startDate': startDate,
            'endDate': endDate,
            'category': category,
            'exchange': exchange,
            'marketcap': marketcap,
            'volume': volume,
            'fdv': fdv,
            'signal': signal
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._paginated_request('get', 'trading-signals', params, max_days=29)
    
    def get_dataframe(self, **kwargs):
        """Get trading signals data as a pandas DataFrame.
        
        Args:
            **kwargs: Arguments to pass to the get method
            
        Returns:
            pandas.DataFrame: DataFrame containing trading signals data
        """
        data = self.get(**kwargs)
        return self.to_dataframe(data)