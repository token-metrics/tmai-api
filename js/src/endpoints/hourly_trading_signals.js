const BaseEndpoint = require('../base');

/**
 * Endpoint for accessing hourly AI-generated trading signals for long and short positions
 */
class HourlyTradingSignalsEndpoint extends BaseEndpoint {
  /**
   * Get hourly AI-generated trading signals with automatic pagination.
   * 
   * @param {Object} options - Query parameters
   * @param {string} options.token_id - Comma-separated Token IDs (required)
   * @param {number} options.limit - Limit the number of items in response (defaults to 50)
   * @param {number} options.page - Page number for pagination (defaults to 1)
   * @returns {Promise<Object>} - Hourly trading signals data with pagination handled automatically
   */
  async get(options = {}) {
    return this._paginatedRequest('get', 'hourly-trading-signals', options, 29);
  }
}

module.exports = HourlyTradingSignalsEndpoint;
