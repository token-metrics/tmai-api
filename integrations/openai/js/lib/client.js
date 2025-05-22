const axios = require('axios');
const jwt = require('jsonwebtoken');

/**
 * Token Metrics AI helper library for OpenAI Agents
 */
class TokenMetricsOpenAI {
  /**
   * Initialize the Token Metrics OpenAI client
   * 
   * @param {Object} options - Client options
   * @param {string} options.apiKey - Your Token Metrics API key
   * @param {string} options.jwtToken - JWT token with required claims
   */
  constructor(options = {}) {
    this.apiKey = options.apiKey;
    this.jwtToken = options.jwtToken;
    this.baseUrl = 'https://api.tokenmetrics.com/v2';
  }
  
  /**
   * Get headers for API requests
   * 
   * @returns {Object} - Headers for API requests
   */
  _getHeaders() {
    const headers = {
      'accept': 'application/json'
    };
    
    if (this.jwtToken) {
      headers['Authorization'] = `Bearer ${this.jwtToken}`;
    } else if (this.apiKey) {
      headers['api_key'] = this.apiKey;
    }
    
    return headers;
  }
  
  /**
   * Get cryptocurrency ratings
   * 
   * @param {Object} options - Query parameters
   * @param {string} options.symbol - Token symbol (e.g., "BTC")
   * @param {string} options.startDate - Start date in YYYY-MM-DD format
   * @param {string} options.endDate - End date in YYYY-MM-DD format
   * @returns {Promise<Object>} - Ratings data
   */
  async getRatings(options = {}) {
    if (!options.symbol) {
      throw new Error('Symbol parameter is required');
    }
    
    const response = await axios.get(`${this.baseUrl}/ratings`, {
      headers: this._getHeaders(),
      params: options
    });
    
    return response.data;
  }
  
  /**
   * Get cryptocurrency metrics
   * 
   * @param {Object} options - Query parameters
   * @param {string} options.symbol - Token symbol (e.g., "BTC")
   * @param {string} options.startDate - Start date in YYYY-MM-DD format
   * @param {string} options.endDate - End date in YYYY-MM-DD format
   * @returns {Promise<Object>} - Factors data
   */
  async getMetrics(options = {}) {
    if (!options.symbol) {
      throw new Error('Symbol parameter is required');
    }
    
    const response = await axios.get(`${this.baseUrl}/metrics`, {
      headers: this._getHeaders(),
      params: options
    });
    
    return response.data;
  }
  
  /**
   * Get cryptocurrency sentiment
   * 
   * @param {Object} options - Query parameters
   * @param {string} options.symbol - Token symbol (e.g., "BTC")
   * @param {string} options.startDate - Start date in YYYY-MM-DD format
   * @param {string} options.endDate - End date in YYYY-MM-DD format
   * @returns {Promise<Object>} - Sentiment data
   */
  async getSentiment(options = {}) {
    if (!options.symbol) {
      throw new Error('Symbol parameter is required');
    }
    
    const response = await axios.get(`${this.baseUrl}/sentiments`, {
      headers: this._getHeaders(),
      params: options
    });
    
    return response.data;
  }
  
  /**
   * Create a JWT token with required claims
   * 
   * @param {Object} options - JWT options
   * @param {string} options.plan - User subscription plan
   * @param {string} options.paymentMethod - Payment method used
   * @param {number} options.stakeScore - Staking score for discounts
   * @param {string} options.secretKey - Secret key for signing the JWT
   * @param {number} options.expirationHours - Token expiration in hours
   * @returns {string} - JWT token
   */
  static createJWT(options = {}) {
    const { plan, paymentMethod, stakeScore, secretKey, expirationHours = 1 } = options;
    
    if (!plan || !paymentMethod || stakeScore === undefined || !secretKey) {
      throw new Error('Missing required parameters for JWT creation');
    }
    
    const payload = {
      plan,
      payment_method: paymentMethod,
      stake_score: stakeScore,
      exp: Math.floor(Date.now() / 1000) + (expirationHours * 60 * 60)
    };
    
    return jwt.sign(payload, secretKey);
  }
}

module.exports = TokenMetricsOpenAI;
