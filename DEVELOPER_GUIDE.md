# Token Metrics AI API Developer Guide

This guide provides comprehensive information for developers looking to integrate with the Token Metrics AI API. It includes setup instructions, best practices, and examples to help you get started quickly.

## Table of Contents

- [Getting Started](#getting-started)
- [API Key](#api-key)
- [SDK Installation](#sdk-installation)
- [Basic Usage](#basic-usage)
- [Advanced Integration](#advanced-integration)
- [Sample Applications](#sample-applications)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Getting Started

The Token Metrics AI API provides professional investors and traders with comprehensive cryptocurrency analysis, AI-powered trading signals, market data, and advanced insights. This guide will help you integrate the API into your applications.

## API Key

To use the Token Metrics AI API, you need an API key. You can get your API key by signing up at [Token Metrics Developers](https://developers.tokenmetrics.com/).

## SDK Installation

### Python SDK

```bash
pip install tmai-api
```

### JavaScript SDK

```bash
npm install tmai-api
```

## Basic Usage

### Python Example

```python
from tmai_api import TokenMetricsClient

# Initialize the client with your API key
client = TokenMetricsClient(api_key="your-api-key")

# Get information for top cryptocurrencies
tokens = client.tokens.get(symbol="BTC,ETH")

# Get short-term trading grades
trader_grades = client.trader_grades.get(
    symbol="BTC,ETH",
    startDate="2023-10-01",
    endDate="2023-10-10"
)

# Ask the AI agent a question
answer = client.ai_agent.get_answer_text("What is your analysis of Bitcoin?")
```

### JavaScript Example

```javascript
const { TokenMetricsClient } = require('tmai-api');

// Initialize the client with your API key
const client = new TokenMetricsClient('your-api-key');

// Get information for top cryptocurrencies
client.tokens.get({ symbol: 'BTC,ETH' })
  .then(tokens => {
    console.log(tokens);
  });

// Get short-term trading grades
client.traderGrades.get({
  symbol: 'BTC,ETH',
  startDate: '2023-10-01',
  endDate: '2023-10-10'
})
  .then(traderGrades => {
    console.log(traderGrades);
  });

// Ask the AI agent a question
client.aiAgent.getAnswerText('What is your analysis of Bitcoin?')
  .then(answer => {
    console.log(answer);
  });
```

## Advanced Integration

For more advanced integration examples, check out the following resources:

- [Python SDK Examples](python/examples/)
- [JavaScript SDK Examples](js/examples/)
- [Hackathon Projects](examples/hackathon-projects/)

## Sample Applications

We have a collection of sample applications and hackathon projects that demonstrate real-world usage of the Token Metrics AI API. These projects can serve as inspiration or starting points for your own applications.

See the [Hackathon Projects](examples/hackathon-projects/) directory for a comprehensive list of sample applications.

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure your API key is correct and properly configured
   - Check that your API key has the necessary permissions

2. **Rate Limiting**
   - The API has rate limits to prevent abuse
   - Implement proper error handling for rate limit responses

3. **Data Format Issues**
   - Ensure you're using the correct data formats for dates and symbols
   - Check the API documentation for required parameters

### Getting Help

If you encounter issues not covered in this guide, you can:
- Check the [API Documentation](https://api.tokenmetrics.com/docs)
- Submit an issue on the [GitHub repository](https://github.com/token-metrics/tmai-api/issues)
- Contact Token Metrics support

## Contributing

Contributions to the Token Metrics AI API SDK are welcome! Please feel free to submit a Pull Request.

If you've built a project using the Token Metrics API and would like to have it featured in our examples, please submit a pull request with your project details.
