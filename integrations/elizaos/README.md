# Token Metrics ElizaOS Plugin

This plugin integrates the Token Metrics AI API with ElizaOS, providing cryptocurrency ratings, metrics, and sentiment analysis.

## Features

- Access Token Metrics cryptocurrency ratings
- Authentication with JWT tokens
- Fast response times (< 800ms for 95th percentile)

## Installation

1. Install the plugin through the ElizaOS plugin marketplace
2. Configure your Token Metrics API key
3. Start accessing cryptocurrency ratings

## Usage

```javascript
// Example usage in ElizaOS
const ratings = await elizaos.plugins.tokenMetricsRatings.getRatings({
  symbol: "BTC,ETH",
  startDate: "2023-10-01",
  endDate: "2023-10-10"
});

console.log(ratings);
```

## Authentication

The plugin uses Bearer JWT authentication with the following required claims:
- `plan`: User subscription plan
- `payment_method`: Payment method used
- `stake_score`: Staking score for discounts

## Performance

This plugin is optimized for performance, with a 95th percentile response time of less than 800ms for ratings queries.
