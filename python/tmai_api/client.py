import os
from typing import Callable, Optional, Tuple

import requests
from urllib3.util import Retry

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
from tmai_api.exceptions import MissingAPIKeyError

class TokenMetricsClient:
    """Main client for interacting with the Token Metrics AI API."""
    
    BASE_URL = "https://api.tokenmetrics.com/v2"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        status_forcelist: Optional[Tuple[int, ...]] = None,
        session: Optional[requests.Session] = None,
        allow_partial_results: bool = False,
        progress_callback: Optional[Callable[[dict], None]] = None,
    ):
        """Initialize the Token Metrics client.
        
        Args:
            api_key (str): Your Token Metrics API key
        """
        self.api_key = api_key or os.getenv("TMAI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyError(
                "An API key is required. Provide it explicitly or set the TMAI_API_KEY environment variable."
            )

        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.timeout = timeout
        self.allow_partial_results = allow_partial_results
        self.progress_callback = progress_callback

        self._session = session or self._build_session(
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

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

    @property
    def session(self) -> requests.Session:
        return self._session

    def _build_session(
        self,
        *,
        max_retries: int,
        backoff_factor: float,
        status_forcelist: Optional[Tuple[int, ...]],
    ) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=max_retries,
            read=max_retries,
            connect=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist or (429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"),
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def build_headers(self) -> dict:
        return {
            "accept": "application/json",
            "api_key": self.api_key,
        }
