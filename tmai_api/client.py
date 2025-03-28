from tmai_api.endpoints.tokens import TokensEndpoint
from tmai_api.endpoints.hourly_ohlcv import HourlyOHLCVEndpoint
from tmai_api.endpoints.daily_ohlcv import DailyOHLCVEndpoint
from tmai_api.endpoints.investor_grades import InvestorGradesEndpoint
from tmai_api.endpoints.trader_grades import TraderGradesEndpoint
from tmai_api.endpoints.trader_indices import TraderIndicesEndpoint
from tmai_api.endpoints.market_metrics import MarketMetricsEndpoint
from tmai_api.endpoints.ai_agent import AIAgentEndpoint
from tmai_api.endpoints.ai_reports import AIReportsEndpoint
from tmai_api.endpoints.trading_signals import TradingSignalsEndpoint

class TokenMetricsClient:
    """Main client for interacting with the Token Metrics AI API."""
    
    BASE_URL = "https://api.tokenmetrics.com/v2"
    
    def __init__(self, api_key=None):
        """Initialize the Token Metrics client.
        
        Args:
            api_key (str): Your Token Metrics API key
        """
        self.api_key = api_key
        self.tokens = TokensEndpoint(self)
        self.hourly_ohlcv = HourlyOHLCVEndpoint(self)
        self.daily_ohlcv = DailyOHLCVEndpoint(self)
        self.investor_grades = InvestorGradesEndpoint(self)
        self.trader_grades = TraderGradesEndpoint(self)
        self.trader_indices = TraderIndicesEndpoint(self)
        self.market_metrics = MarketMetricsEndpoint(self)
        self.ai_agent = AIAgentEndpoint(self)
        self.ai_reports = AIReportsEndpoint(self)
        self.trading_signals = TradingSignalsEndpoint(self)
