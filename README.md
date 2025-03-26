# Token Metrics AI API Python SDK

[![PyPI version](https://img.shields.io/pypi/v/tmai-api.svg)](https://pypi.org/project/tmai-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/tmai-api.svg)](https://pypi.org/project/tmai-api/)
[![License](https://img.shields.io/github/license/token-metrics/tmai-api.svg)](https://github.com/token-metrics/tmai-api/blob/main/LICENSE)

The official Python SDK for Token Metrics AI API - providing professional investors and traders with comprehensive cryptocurrency analysis, AI-powered trading signals, market data, and advanced insights.

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

## Quick Start

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

# Get long-term investment grades
investor_grades = client.investor_grades.get(
    symbol="BTC,ETH", 
    startDate="2023-10-01",
    endDate="2023-10-10"
)

# Ask the AI agent a question
answer = client.ai_agent.get_answer_text("What is your analysis of Bitcoin?")
```

## Data Analysis with Pandas

Convert API responses directly to Pandas DataFrames for easy analysis:

```python
# Convert to DataFrame
tokens_df = client.tokens.get_dataframe(symbol="BTC,ETH")
trader_grades_df = client.trader_grades.get_dataframe(symbol="BTC,ETH")

# Analyze with Pandas
import pandas as pd

# Filter for specific tokens
bitcoin_data = trader_grades_df[trader_grades_df['TOKEN_SYMBOL'] == 'BTC']

# Plot grades over time
import matplotlib.pyplot as plt
bitcoin_data.plot(x='DATE', y='TM_TRADER_GRADE', figsize=(10, 6))
plt.title('Bitcoin Trading Grade Trend')
plt.show()
```

## Available Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `tokens` | Information about all supported tokens | `client.tokens.get(symbol="BTC,ETH")` |
| `hourly_ohlcv` | Hourly price and volume data | `client.hourly_ohlcv.get(symbol="BTC", startDate="2023-10-01", endDate="2023-10-10")` |
| `investor_grades` | Long-term investment ratings | `client.investor_grades.get(symbol="BTC,ETH", startDate="2023-10-01", endDate="2023-10-10")` |
| `trader_grades` | Short-term trading signals | `client.trader_grades.get(symbol="BTC,ETH", startDate="2023-10-01", endDate="2023-10-10")` |
| `trader_indices` | AI-generated trading portfolios | `client.trader_indices.get(startDate="2023-10-01", endDate="2023-10-10")` |
| `market_metrics` | Overall market data | `client.market_metrics.get(startDate="2023-10-01", endDate="2023-10-10")` |
| `ai_agent` | Interact with Token Metrics AI chatbot | `client.ai_agent.ask("What is your Bitcoin forecast?")` |
| `ai_reports` | AI-generated analysis reports | `client.ai_reports.get(symbol="BTC,ETH")` |
| `trading_signals` | AI-generated trading signals | `client.trading_signals.get(symbol="BTC,ETH", startDate="2023-10-01", endDate="2023-10-10", signal="1")` |

## Detailed Usage Examples

### Working with Trading Signals

```python
# Get bullish trading signals (signal=1) for Bitcoin
signals = client.trading_signals.get_dataframe(
    symbol="BTC", 
    startDate="2023-10-01", 
    endDate="2023-10-10",
    signal="1"  # 1=Bullish, -1=Bearish
)

# Calculate potential returns
print(f"Average signal return: {signals['TRADING_SIGNALS_RETURNS'].mean():.2f}%")
print(f"Average holding return: {signals['HOLDING_RETURNS'].mean():.2f}%")
```

### Getting AI-Generated Reports

```python
# Get comprehensive AI reports for Ethereum
eth_reports = client.ai_reports.get(symbol="ETH")

# Access specific report sections
trader_report = eth_reports['data'][0]['TRADER_REPORT']
tech_report = eth_reports['data'][0]['TECHNOLOGY_REPORT']
fundamental_report = eth_reports['data'][0]['FUNDAMENTAL_REPORT']

print(f"Trading Report Excerpt:\n{trader_report[:200]}...")
```

### Analyzing Market Metrics

```python
# Get market sentiment metrics
metrics = client.market_metrics.get_dataframe(
    startDate="2023-10-01", 
    endDate="2023-10-10"
)

# Analyze Fear & Greed Index trends
plt.figure(figsize=(12, 6))
metrics.plot(x='DATE', y='FEAR_AND_GREED_VALUE', figsize=(10, 6))
plt.title('Crypto Fear & Greed Index')
plt.axhline(y=50, color='r', linestyle='-', alpha=0.3)
plt.show()
```

## Authentication

All API requests require an API key. You can get your API key by signing up at [Token Metrics](https://tokenmetrics.com).

```python
# Initialize with your API key
client = TokenMetricsClient(api_key="your-api-key")
```

## Error Handling

The SDK provides built-in error handling for API requests:

```python
try:
    data = client.tokens.get(symbol="INVALID_SYMBOL")
except Exception as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

## Requirements

- Python 3.6+
- `requests` package
- `pandas` package

## Documentation

For complete API documentation, visit:
- [Token Metrics API Documentation](https://api.tokenmetrics.com/docs)
- [SDK Examples](https://github.com/token-metrics/tmai-api/blob/master/examples/example_usage.ipynb)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

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