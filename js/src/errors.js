class MissingApiKeyError extends Error {
  constructor() {
    super('An API key is required. Provide it explicitly or set the TMAI_API_KEY environment variable.');
    this.name = 'MissingApiKeyError';
  }
}

class ApiRequestError extends Error {
  constructor({ endpoint, method, params, status, originalError }) {
    const statusLabel = status ? ` status=${status}` : '';
    super(`API request failed:${statusLabel} method=${method} endpoint=${endpoint}`);
    this.name = 'ApiRequestError';
    this.endpoint = endpoint;
    this.method = method;
    this.params = params;
    this.status = status;
    this.originalError = originalError;
  }
}

module.exports = {
  MissingApiKeyError,
  ApiRequestError
};
