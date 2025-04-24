/**
 * API Service for communicating with the backend.
 * Handles all API requests to the backend endpoints.
 */

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Helper function to handle fetch requests.
 * 
 * @param {string} endpoint - API endpoint to fetch from
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>} - Response data or error
 */
const fetchData = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'An error occurred');
    }

    return await response.json();
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
};

/**
 * Token API functions
 */
export const tokenAPI = {
  /**
   * Get tokens with optional filtering
   * 
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Token data
   */
  getTokens: (params = {}) => {
    const queryParams = new URLSearchParams();
    
    if (params.symbols) queryParams.append('symbols', params.symbols);
    if (params.tokenIds) queryParams.append('token_ids', params.tokenIds);
    if (params.category) queryParams.append('category', params.category);
    if (params.exchange) queryParams.append('exchange', params.exchange);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.page) queryParams.append('page', params.page);
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return fetchData(`/tokens${query}`);
  },
  
  /**
   * Get top tokens by market cap
   * 
   * @param {number} topK - Number of top tokens to retrieve
   * @param {number} page - Page number
   * @returns {Promise<Object>} - Top tokens data
   */
  getTopTokens: (topK = 20, page = 0) => {
    return fetchData(`/tokens/top?top_k=${topK}&page=${page}`);
  },
  
  /**
   * Get recommended tokens based on Token Metrics signals
   * 
   * @param {number} topK - Number of recommendations to return
   * @returns {Promise<Object>} - Recommended tokens data
   */
  getRecommendedTokens: (topK = 10) => {
    return fetchData(`/tokens/recommended?top_k=${topK}`);
  },
  
  /**
   * Get token prices
   * 
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Price data
   */
  getPrices: (params = {}) => {
    const queryParams = new URLSearchParams();
    
    if (params.symbols) queryParams.append('symbols', params.symbols);
    if (params.tokenIds) queryParams.append('token_ids', params.tokenIds);
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return fetchData(`/price${query}`);
  }
};

/**
 * Market API functions
 */
export const marketAPI = {
  /**
   * Get trading signals for tokens
   * 
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Trading signals data
   */
  getTradingSignals: (params = {}) => {
    const queryParams = new URLSearchParams();
    
    if (params.symbols) queryParams.append('symbols', params.symbols);
    if (params.tokenIds) queryParams.append('token_ids', params.tokenIds);
    if (params.category) queryParams.append('category', params.category);
    if (params.startDate) queryParams.append('start_date', params.startDate);
    if (params.endDate) queryParams.append('end_date', params.endDate);
    if (params.signal) queryParams.append('signal', params.signal);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.page) queryParams.append('page', params.page);
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return fetchData(`/trading-signals${query}`);
  },
  
  /**
   * Get trader grades for tokens
   * 
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Trader grades data
   */
  getTraderGrades: (params = {}) => {
    const queryParams = new URLSearchParams();
    
    if (params.symbols) queryParams.append('symbols', params.symbols);
    if (params.tokenIds) queryParams.append('token_ids', params.tokenIds);
    if (params.category) queryParams.append('category', params.category);
    if (params.startDate) queryParams.append('start_date', params.startDate);
    if (params.endDate) queryParams.append('end_date', params.endDate);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.page) queryParams.append('page', params.page);
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return fetchData(`/trader-grades${query}`);
  },
  
  /**
   * Get market metrics
   * 
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Market metrics data
   */
  getMarketMetrics: (params = {}) => {
    const queryParams = new URLSearchParams();
    
    if (params.startDate) queryParams.append('start_date', params.startDate);
    if (params.endDate) queryParams.append('end_date', params.endDate);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.page) queryParams.append('page', params.page);
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return fetchData(`/market-metrics${query}`);
  }
};

/**
 * Portfolio API functions
 */
export const portfolioAPI = {
  /**
   * Analyze a portfolio of cryptocurrency holdings
   * 
   * @param {Object} holdings - Dictionary of holdings {symbol: amount}
   * @returns {Promise<Object>} - Portfolio analysis
   */
  analyzePortfolio: (holdings) => {
    return fetchData('/portfolio/analyze', {
      method: 'POST',
      body: JSON.stringify({ holdings }),
    });
  },
  
  /**
   * Optimize a portfolio based on Token Metrics signals and risk tolerance
   * 
   * @param {Object} holdings - Dictionary of holdings {symbol: amount}
   * @param {string} riskTolerance - Risk tolerance level ("low", "medium", "high")
   * @returns {Promise<Object>} - Optimized portfolio allocation
   */
  optimizePortfolio: (holdings, riskTolerance = 'medium') => {
    return fetchData('/portfolio/optimize', {
      method: 'POST',
      body: JSON.stringify({ holdings, risk_tolerance: riskTolerance }),
    });
  }
};

/**
 * AI API functions
 */
export const aiAPI = {
  /**
   * Ask a question to the Token Metrics AI agent
   * 
   * @param {string} question - The question to ask
   * @returns {Promise<Object>} - AI agent response
   */
  askQuestion: (question) => {
    return fetchData('/ai/ask', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  }
};

// Export all API modules
export default {
  token: tokenAPI,
  market: marketAPI,
  portfolio: portfolioAPI,
  ai: aiAPI,
}; 