# Token Metrics OpenAI Agents Tool

This integration provides a tool for OpenAI Agents to access the Token Metrics AI API for cryptocurrency ratings, metrics, and sentiment analysis.

## Features

- Tool definition in YAML format for OpenAI Agents
- Helper libraries for Python and JavaScript
- OAuth authentication with JWT token conversion
- Access to ratings, metrics, and sentiment endpoints

## Components

### Tool Definition

The `tool.yaml` file defines the OpenAI Agents tool with:
- Authentication configuration
- Endpoint definitions
- Parameter specifications
- Example responses

### Helper Libraries

#### Python

```python
from tmai_openai import TokenMetricsOpenAI

# Initialize with API key
client = TokenMetricsOpenAI(api_key="your_api_key")

# Or initialize with JWT token
client = TokenMetricsOpenAI(jwt_token="your_jwt_token")

# Get cryptocurrency ratings
ratings = client.get_ratings(symbol="BTC")
print(ratings)

# Get cryptocurrency metrics
metrics = client.get_metrics(symbol="ETH", start_date="2023-01-01", end_date="2023-01-31")
print(metrics)

# Get cryptocurrency sentiment
sentiment = client.get_sentiment(symbol="BTC")
print(sentiment)

# Create a JWT token with required claims
jwt_token = TokenMetricsOpenAI.create_jwt(
    plan="premium",
    payment_method="tmai_token",
    stake_score=0.15,
    secret_key="your_secret_key"
)
```

#### JavaScript

```javascript
const TokenMetricsOpenAI = require('@tmai/openai');

// Initialize with API key
const client = new TokenMetricsOpenAI({ apiKey: 'your_api_key' });

// Or initialize with JWT token
const client = new TokenMetricsOpenAI({ jwtToken: 'your_jwt_token' });

// Get cryptocurrency ratings
client.getRatings({ symbol: 'BTC' })
  .then(ratings => console.log(ratings))
  .catch(error => console.error(error));

// Get cryptocurrency metrics
client.getFactors({ symbol: 'ETH', startDate: '2023-01-01', endDate: '2023-01-31' })
  .then(metrics => console.log(metrics))
  .catch(error => console.error(error));

// Get cryptocurrency sentiment
client.getSentiment({ symbol: 'BTC' })
  .then(sentiment => console.log(sentiment))
  .catch(error => console.error(error));

// Create a JWT token with required claims
const jwtToken = TokenMetricsOpenAI.createJWT({
  plan: 'premium',
  paymentMethod: 'tmai_token',
  stakeScore: 0.15,
  secretKey: 'your_secret_key'
});
```

## Installation

### Python

```bash
pip install tmai-openai
```

### JavaScript

```bash
npm install @tmai/openai
```

## Testing

The integration has been tested to ensure it meets the acceptance criteria:
- Tool installs in ChatGPT
- Tool fetches ratings via JWT authentication
