# Token Metrics AI API

The official SDK for Token Metrics AI API - providing professional investors and traders with comprehensive cryptocurrency analysis, AI-powered trading signals, market data, and advanced insights.

Build AI-driven trading agents for real crypto alpha. Empowering you to build AI-driven trading agents that capture market-leading alpha trading.

[Watch our team's presentation at ETH Bucharest: Build AI Crypto Trading Bots & Agents in 2 Lines](https://www.youtube.com/watch?v=1qVuIwmeZJE)

## Core Value Proposition

- **AI-Driven Precision for Crypto**: Utilize advanced machine learning models trained on crypto market dynamics to generate actionable trading signals
- **Crypto Trading Agents**: Build agents that can take consistently winning trades on exchanges—both centralized and decentralized
- **Real Crypto Alpha Generation**: Rely on backtested AI grades to drive decisions that yield tangible profitability in the crypto space

## Features

- **Comprehensive Market Data**: Access detailed information on thousands of cryptocurrencies
- **AI-Powered Analysis**: Get trading and investment grades based on advanced AI models
- **Technical Indicators**: Access technical analysis grades and quantitative metrics
- **Price Data**: Retrieve historical OHLCV (Open, High, Low, Close, Volume) data 
- **Trading Signals**: Receive AI-generated long and short trading signals
- **AI Agent**: Interact with Token Metrics' AI chatbot for market insights
- **AI Reports**: Access detailed technical, fundamental, and trading reports
- **Simple Interface**: Intuitive API with Pandas DataFrame integration

## Installation

```bash
pip install tmai-api
```
```bash
npm install tmai-api
```

## Quick Start

### Python
```python
from tmai_api import TokenMetricsClient

# Initialize the client with your API key
client = TokenMetricsClient(api_key="your-api-key")

# Get information for top cryptocurrencies
tokens = client.tokens.get(symbol="BTC,ETH")
```

### JavaScript
```javascript
const { TokenMetricsClient } = require('tmai-api');

// Initialize the client with your API key
const client = new TokenMetricsClient('your-api-key');

// Get information for top cryptocurrencies
client.tokens.get({ symbol: 'BTC,ETH' })
  .then(tokens => {
    console.log(tokens);
  });
```

## Documentation

- [Token Metrics API Documentation](https://app.tokenmetrics.com/en/api)
- [Developer Guide](DEVELOPER_GUIDE.md) - Comprehensive guide for developers
- [Python SDK Documentation](python/README.md)
- [JavaScript SDK Documentation](js/README.md)

## Target Audiences

### Developers
Create market-leading trading tools, DeFAI apps, and agentic dashboards.

### Traders & Hedge Funds
Deploy autonomous agents that maximize returns with real-time crypto data.

### Institutions
Command unbelievable scale when you infuse AI Agents into your profit strategies.

## Use Cases

- **CEX Trading Agents**: Automate profitable trades on centralized exchanges
- **DEX Trading Agents**: Execute on-chain trades on decentralized exchanges
- **Market Prediction Dashboards**: Build real-time dashboards with market insights
- **Telegram/Discord Agents**: Create interactive agents for trading alerts
- **Web/Mobile/Desktop Applications**: Develop user-friendly applications for crypto trading

## Sample Applications

We have a collection of sample applications and hackathon projects that demonstrate real-world usage of the Token Metrics AI API:

- [Hackathon Projects](examples/hackathon-projects/) - Collection of projects from hackathons
- [Python Examples](python/examples/) - Example scripts using the Python SDK
- [JavaScript Examples](js/examples/) - Example scripts using the JavaScript SDK

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

If you've built a project using the Token Metrics API and would like to have it featured in our examples, please submit a pull request with your project details.

## License

This SDK is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <a href="https://tokenmetrics.com">
    <img src="https://files.readme.io/6141d8ec9ddb9dd233e52357e7526ba5fea3dacafab20cd042bc20a2de070beb-dark_mode_1.svg" alt="Token Metrics Logo" width="300">
  </a>
</p>
<p align="center">
  <i>Empowering investors with AI-powered crypto insights</i>
</p>
