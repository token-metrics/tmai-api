# Token Metrics Cursor IDE Connector

This connector integrates the Token Metrics AI API with Cursor IDE, providing cryptocurrency ratings, metrics, and sentiment analysis directly in your development environment.

## Features

- Access Token Metrics cryptocurrency ratings
- View cryptocurrency metrics and sentiment analysis
- OAuth authentication flow for secure API access
- Sample code snippets for quick integration

## Installation

1. Open Cursor IDE
2. Navigate to the "Import API" wizard
3. Search for "Token Metrics" or import the `cursor.json` file
4. Follow the authentication flow to connect your Token Metrics account

## Usage

```javascript
// Example: Get Bitcoin ratings
const ratings = await tokenMetricsApi.getRatings({ symbol: 'BTC' });
console.log(ratings);

// Example: Get Ethereum metrics
const metrics = await tokenMetricsApi.getMetrics({ 
  symbol: 'ETH', 
  startDate: '2023-01-01', 
  endDate: '2023-01-31' 
});
console.log(metrics);
```

## Authentication

The connector uses OAuth 2.0 for authentication, which securely converts your OAuth credentials to a JWT token with the required claims:
- `plan`: User subscription plan
- `payment_method`: Payment method used
- `stake_score`: Staking score for discounts

## Testing

The connector has been tested with the Cursor IDE "Import API" wizard to ensure it runs sample code with valid responses.
