const axios = require('axios');

const { MissingApiKeyError } = require('./errors');

/**
 * Main client for interacting with the Token Metrics AI API.
 */
class TokenMetricsClient {
  /**
   * Base URL for the Token Metrics API
   */
  static BASE_URL = "https://api.tokenmetrics.com/v2";

  /**
   * Initialize the Token Metrics client.
   *
   * @param {string} apiKey - Your Token Metrics API key
   * @param {Object} options - Optional configuration overrides
   */
  constructor(apiKey, options = {}) {
    const resolvedKey = apiKey || process.env.TMAI_API_KEY || process.env.TM_API_KEY;
    if (!resolvedKey) {
      throw new MissingApiKeyError();
    }

    const {
      baseUrl = TokenMetricsClient.BASE_URL,
      timeout = 10000,
      retries = 3,
      retryDelay = 300,
      retryStatusCodes = [429, 500, 502, 503, 504],
      httpClient,
      allowPartialResults = false,
      progressCallback = null
    } = options;

    this.apiKey = resolvedKey;
    this.baseUrl = baseUrl.replace(/\/?$/, '');
    this.timeout = timeout;
    this.allowPartialResults = allowPartialResults;
    this.progressCallback = progressCallback;

    this.http = httpClient || this._createHttpClient({ timeout, retries, retryDelay, retryStatusCodes });

    const TokensEndpoint = require('./endpoints/tokens');
    const AIAgentEndpoint = require('./endpoints/ai_agent');
    const TradingSignalsEndpoint = require('./endpoints/trading_signals');
    const HourlyOHLCVEndpoint = require('./endpoints/hourly_ohlcv');
    const DailyOHLCVEndpoint = require('./endpoints/daily_ohlcv');
    const InvestorGradesEndpoint = require('./endpoints/investor_grades');
    const TraderGradesEndpoint = require('./endpoints/trader_grades');
    const TraderIndicesEndpoint = require('./endpoints/trader_indices');
    const MarketMetricsEndpoint = require('./endpoints/market_metrics');
    const AIReportsEndpoint = require('./endpoints/ai_reports');

    const InvestorIndicesEndpoint = require('./endpoints/investor_indices');
    const CryptoInvestorsEndpoint = require('./endpoints/crypto_investors');
    const TopMarketCapTokensEndpoint = require('./endpoints/top_market_cap_tokens');
    const ResistanceSupportEndpoint = require('./endpoints/resistance_support');
    const PriceEndpoint = require('./endpoints/price');
    const SentimentEndpoint = require('./endpoints/sentiment');
    const QuantmetricsEndpoint = require('./endpoints/quantmetrics');
    const ScenarioAnalysisEndpoint = require('./endpoints/scenario_analysis');
    const CorrelationEndpoint = require('./endpoints/correlation');
    const IndexHoldingsEndpoint = require('./endpoints/index_holdings');
    const SectorIndicesHoldingsEndpoint = require('./endpoints/sector_indices_holdings');
    const IndicesPerformanceEndpoint = require('./endpoints/indices_performance');
    const SectorIndicesPerformanceEndpoint = require('./endpoints/sector_indices_performance');
    const IndexTransactionEndpoint = require('./endpoints/index_transaction');
    const SectorIndexTransactionEndpoint = require('./endpoints/sector_index_transaction');

    this.tokens = new TokensEndpoint(this);
    this.aiAgent = new AIAgentEndpoint(this);
    this.tradingSignals = new TradingSignalsEndpoint(this);
    this.hourlyOhlcv = new HourlyOHLCVEndpoint(this);
    this.dailyOhlcv = new DailyOHLCVEndpoint(this);
    this.investorGrades = new InvestorGradesEndpoint(this);
    this.traderGrades = new TraderGradesEndpoint(this);
    this.traderIndices = new TraderIndicesEndpoint(this);
    this.marketMetrics = new MarketMetricsEndpoint(this);
    this.aiReports = new AIReportsEndpoint(this);

    this.investorIndices = new InvestorIndicesEndpoint(this);
    this.cryptoInvestors = new CryptoInvestorsEndpoint(this);
    this.topMarketCapTokens = new TopMarketCapTokensEndpoint(this);
    this.resistanceSupport = new ResistanceSupportEndpoint(this);
    this.price = new PriceEndpoint(this);
    this.sentiment = new SentimentEndpoint(this);
    this.quantmetrics = new QuantmetricsEndpoint(this);
    this.scenarioAnalysis = new ScenarioAnalysisEndpoint(this);
    this.correlation = new CorrelationEndpoint(this);
    this.indexHoldings = new IndexHoldingsEndpoint(this);
    this.sectorIndicesHoldings = new SectorIndicesHoldingsEndpoint(this);
    this.indicesPerformance = new IndicesPerformanceEndpoint(this);
    this.sectorIndicesPerformance = new SectorIndicesPerformanceEndpoint(this);
    this.indexTransaction = new IndexTransactionEndpoint(this);
    this.sectorIndexTransaction = new SectorIndexTransactionEndpoint(this);
  }

  _createHttpClient({ timeout, retries, retryDelay, retryStatusCodes }) {
    const instance = axios.create({
      baseURL: this.baseUrl,
      timeout
    });

    instance.interceptors.response.use(
      (response) => response,
      async (error) => {
        const config = error.config || {};
        const status = error.response ? error.response.status : null;

        config.__retryCount = config.__retryCount || 0;

        if (config.__retryCount >= retries || !status || !retryStatusCodes.includes(status)) {
          return Promise.reject(error);
        }

        config.__retryCount += 1;
        const delay = Math.pow(2, config.__retryCount - 1) * retryDelay;
        await new Promise((resolve) => setTimeout(resolve, delay));
        return instance.request(config);
      }
    );

    return instance;
  }

  buildHeaders() {
    return {
      accept: 'application/json',
      api_key: this.apiKey
    };
  }
}

module.exports = TokenMetricsClient;
