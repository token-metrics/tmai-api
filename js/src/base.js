const { ApiRequestError } = require('./errors');

/**
 * Base class for all API endpoints
 */
class BaseEndpoint {
  /**
   * Initialize the endpoint with a client instance.
   * 
   * @param {Object} client - TokenMetricsClient instance
   */
  constructor(client) {
    this.client = client;
    this.baseUrl = client.baseUrl;
  }

  /**
   * Make a request to the API.
   * 
   * @param {string} method - HTTP method (get, post, etc.)
   * @param {string} endpoint - API endpoint path
   * @param {Object} params - Query parameters for GET requests
   * @param {Object} json - JSON payload for POST requests
   * @returns {Promise<Object>} - API response data
   * @private
   */
  async _request(method, endpoint, params = null, json = null) {
    const normalizedMethod = method.toUpperCase();
    if (!['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'].includes(normalizedMethod)) {
      throw new Error(`Unsupported HTTP method: ${method}`);
    }

    const headers = this.client.buildHeaders();
    if (['POST', 'PUT', 'PATCH'].includes(normalizedMethod)) {
      headers['content-type'] = 'application/json';
    }

    try {
      const response = await this.client.http.request({
        method: normalizedMethod,
        url: endpoint.startsWith('/') ? endpoint : `/${endpoint}`,
        headers,
        params: params || undefined,
        data: json || undefined
      });
      return response.data;
    } catch (error) {
      const status = error.response ? error.response.status : undefined;
      throw new ApiRequestError({
        endpoint,
        method: normalizedMethod,
        params,
        status,
        originalError: error
      });
    }
  }

  /**
   * Split a date range into chunks of max_days.
   * 
   * @param {string} startDate - Start date in YYYY-MM-DD format
   * @param {string} endDate - End date in YYYY-MM-DD format
   * @param {number} maxDays - Maximum number of days in each chunk
   * @returns {Array<Array<string>>} - List of [chunkStartDate, chunkEndDate] arrays
   * @private
   */
  _chunkDateRange(startDate, endDate, maxDays = 29) {
    if (!startDate || !endDate) {
      return [[startDate, endDate]]; // If dates not provided, return as is
    }

    try {
      const start = new Date(startDate);
      const end = new Date(endDate);

      const daysDiff = Math.floor((end - start) / (1000 * 60 * 60 * 24));
      if (daysDiff <= maxDays) {
        return [[startDate, endDate]];
      }

      const result = [];
      let chunkStart = new Date(start);

      while (chunkStart < end) {
        const chunkEnd = new Date(chunkStart);
        chunkEnd.setDate(chunkEnd.getDate() + maxDays);

        if (chunkEnd > end) {
          result.push([
            chunkStart.toISOString().split('T')[0],
            endDate
          ]);
        } else {
          result.push([
            chunkStart.toISOString().split('T')[0],
            chunkEnd.toISOString().split('T')[0]
          ]);
        }

        chunkStart = new Date(chunkEnd);
        chunkStart.setDate(chunkStart.getDate() + 1);
      }

      return result;
    } catch (error) {
      return [[startDate, endDate]];
    }
  }

  /**
   * Make paginated requests to handle date ranges and custom pagination logic.
   * 
   * This method handles two forms of pagination:
   * 1. Date chunking: Splitting long date ranges into <= maxDays chunks
   * 2. Offset-based pagination: Since the API's page parameter doesn't work as expected
   * 
   * @param {string} method - HTTP method (get, post, etc.)
   * @param {string} endpoint - API endpoint path
   * @param {Object} params - Query parameters including startDate and endDate
   * @param {number} maxDays - Maximum number of days allowed between startDate and endDate
   * @param {number} customLimit - Custom limit value. If null, uses endpoint-specific defaults.
   * @returns {Promise<Object>} - Combined API response data
   * @private
   */
  async _paginatedRequest(method, endpoint, params = {}, maxDays = 29, customLimit = null) {
    const endpointLimits = {
      'daily-ohlcv': 100,
      'hourly-ohlcv': 1000,
      'trader-grades': 1000,
      'investor-grades': 1000,
      'market-metrics': 1000,
      'trader-indices': 1000,
      'trading-signals': 1000,
      'investor-indices': 1000,
      'crypto-investors': 1000,
      'top-market-cap-tokens': 1000,
      'resistance-support': 1000,
      'price': 1000,
      'sentiments': 1000,
      'quantmetrics': 1000,
      'scenario-analysis': 1000,
      'correlation': 1000,
      'index-holdings': 1000,
      'sector-indices-holdings': 1000,
      'indices-performance': 1000,
      'index-specific-performance': 1000,
      'indices-transaction': 1000,
      'sector-index-transaction': 1000,
      'default': 1000
    };

    const workingParams = { ...(params || {}) };

    const startDate = workingParams.startDate;
    const endDate = workingParams.endDate;

    const limit = customLimit !== null ? customLimit :
      (endpointLimits[endpoint] || endpointLimits.default);

    workingParams.limit = limit;

    const pageSeed = workingParams.page ?? 0;
    if (workingParams.page !== undefined) {
      delete workingParams.page;
    }

    const dateChunks = !startDate || !endDate ? 
      [[startDate, endDate]] : 
      this._chunkDateRange(startDate, endDate, maxDays);

    const allData = [];
    const combinedMeta = {};
    const errors = [];

    for (const [chunkStart, chunkEnd] of dateChunks) {
      const chunkParams = { ...workingParams };
      if (chunkStart) {
        chunkParams.startDate = chunkStart;
      }
      if (chunkEnd) {
        chunkParams.endDate = chunkEnd;
      }

      chunkParams.limit = limit;

      let nextPage = pageSeed;

      while (true) {
        chunkParams.page = nextPage;

        try {
          const response = await this._request(method, endpoint, chunkParams, null);
          const { dataItems, metadata } = this._extractData(response);

          if (dataItems.length) {
            allData.push(...dataItems);
          }

          Object.assign(combinedMeta, metadata);

          if (typeof this.client.progressCallback === 'function') {
            this.client.progressCallback({
              endpoint,
              chunk: { startDate: chunkStart, endDate: chunkEnd },
              page: nextPage,
              itemsFetched: dataItems.length
            });
          }

          nextPage = this._calculateNextPage(metadata, nextPage, dataItems.length, limit);
          if (nextPage === null || nextPage === undefined) {
            break;
          }
        } catch (error) {
          if (this.client.allowPartialResults) {
            errors.push({
              chunk: { startDate: chunkStart, endDate: chunkEnd, page: nextPage },
              error: error.message
            });
            break;
          }

          throw error;
        }
      }
    }

    if (allData.length === 0) {
      return { data: [] };
    }

    let result;
    if (Object.keys(combinedMeta).length > 0) {
      result = {
        ...combinedMeta,
        data: allData
      };
    } else if (allData.length > 0 && typeof allData[0] === 'object') {
      result = { data: allData };
    } else {
      result = allData;
    }

    if (errors.length) {
      if (result && typeof result === 'object' && !Array.isArray(result)) {
        return { ...result, errors };
      }

      return { data: result, errors };
    }

    return result;
  }

  _extractData(response) {
    if (response && typeof response === 'object' && !Array.isArray(response)) {
      const { data, ...metadata } = response;
      if (Array.isArray(data)) {
        return { dataItems: data, metadata };
      }
      if (data === null || data === undefined) {
        return { dataItems: [], metadata };
      }
      return { dataItems: [data], metadata };
    }

    if (Array.isArray(response)) {
      return { dataItems: response, metadata: {} };
    }

    if (response === null || response === undefined) {
      return { dataItems: [], metadata: {} };
    }

    return { dataItems: [response], metadata: {} };
  }

  _calculateNextPage(metadata, previousPage, received, pageSize) {
    const directKeys = ['next_page', 'nextPage', 'next_page_token', 'nextPageToken'];
    for (const key of directKeys) {
      if (metadata[key]) {
        return metadata[key];
      }
    }

    const totalPages = metadata.total_pages ?? metadata.totalPages;
    const currentPage = metadata.page ?? metadata.current_page ?? metadata.currentPage;

    if (totalPages !== undefined && currentPage !== undefined) {
      const total = Number(totalPages);
      const current = Number(currentPage);
      if (!Number.isNaN(total) && !Number.isNaN(current) && current + 1 < total) {
        return current + 1;
      }
      return null;
    }

    const hasMore = metadata.has_more ?? metadata.hasMore;
    if (hasMore === false) {
      return null;
    }
    if (hasMore === true) {
      const previousNumeric = Number(previousPage);
      const base = Number.isNaN(previousNumeric) ? 0 : previousNumeric;
      return base + 1;
    }

    if (received < pageSize || pageSize === 0) {
      return null;
    }

    const previousNumeric = Number(previousPage);
    if (Number.isNaN(previousNumeric)) {
      return null;
    }

    return previousNumeric + 1;
  }
}

module.exports = BaseEndpoint;
