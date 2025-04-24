# TM Signals Bot

![Token Metrics Banner](./image/TM_challenge_cover.webp)

## 🚀 Project Overview

TM Signals Bot is a Telegram bot that leverages the Token Metrics API to provide real-time cryptocurrency trading signals, market insights, and automated alerts to users. The standout feature is a fully-functional portfolio simulator that lets users practice trading based on Token Metrics AI signals without risking real money. This project was developed for the Token Metrics Innovation Challenge 2025.

### 📊 Core Features

- **Real-time Trading Signals**: Get buy/sell recommendations for any cryptocurrency with confidence scores
- **Virtual Portfolio Simulation**: Practice trading with $10,000 virtual money based on TM signals
- **Performance Tracking**: Compare your trading decisions with Token Metrics AI recommendations
- **Top Tokens Ranking**: Discover the highest-rated tokens according to Token Metrics AI
- **Market Sentiment Analysis**: Monitor overall crypto market conditions
- **Automated Alerts**: Subscribe to regular updates for top crypto signals and market summaries
- **Interactive Interface**: Inline buttons for seamless user experience

## 📋 Technical Implementation

TM Signals Bot is built with Python and integrates directly with the Token Metrics API v2 to fetch real-time data. The application consists of the following components:

1. **Telegram Bot Interface**: Built with python-telegram-bot library
2. **Token Metrics API Integration**: Custom module for interacting with Token Metrics endpoints
3. **Portfolio Simulation System**: Virtual trading platform with real-time pricing
4. **Subscription Manager**: Handles user subscriptions for automated alerts 
5. **Background Scheduler**: Delivers periodic updates to subscribed users

### 🛠️ API Endpoints Used

The bot leverages several Token Metrics API endpoints:

- `/v2/tokens`: Retrieves detailed token information
- `/v2/trading-signals`: Gets AI-generated trading signals (buy/sell recommendations)
- `/v2/market-metrics`: Fetches overall market sentiment and conditions
- `/v2/trader-indices`: Obtains trader grade information to rank tokens

## 💰 Portfolio Simulator

The portfolio simulator is our standout feature that demonstrates the practical value of Token Metrics API signals:

- **Virtual Trading**: Start with $10,000 and build your portfolio
- **Real-time Pricing**: Uses CoinGecko API to get current market prices
- **Signal Integration**: Every trade shows relevant Token Metrics AI signals
- **Performance Metrics**: Track win rate, profit factor, and overall returns
- **Signal Comparison**: Compare your trading decisions against TM AI recommendations
- **Transaction History**: Review all your past trades and their outcomes
- **Interactive UI**: Buy and sell with inline buttons for a seamless experience

### Key Benefits:

1. **Educational Value**: Users learn to trade without financial risk
2. **API Showcase**: Demonstrates the practical value of Token Metrics signals
3. **User Engagement**: Encourages regular interaction with the bot
4. **Feedback Loop**: Users see how following TM signals impacts performance

## 🧠 How It Works

### Command System

The bot responds to the following commands:

- `/start`: Introduces the bot and lists available commands
- `/signal <symbol>`: Returns a trading signal for a specific token (e.g., `/signal btc`)
- `/top`: Shows the top-performing tokens ranked by Token Metrics AI
- `/market`: Provides current market sentiment analysis
- `/portfolio`: Manages your virtual portfolio
- `/buy <symbol> <amount>`: Buys tokens for your portfolio (e.g., `/buy btc 500`)
- `/sell <symbol> <amount>`: Sells tokens from your portfolio (e.g., `/sell eth 0.5`)
- `/subscribe`: Enables automated hourly and daily alerts
- `/unsubscribe`: Disables automated alerts
- `/help`: Displays help information

### Sample Responses

#### Trading Signal
```
📊 Token: BTC
Signal: BUY ✅
Confidence: 82%
Updated: 2025-04-23
```

#### Portfolio Summary
```
🗂 PORTFOLIO SUMMARY

💰 Total Value: $12,450.75
💵 Cash: $5,230.50
📈 Holdings: $7,220.25
✅ Profit: $2,450.75 (+24.51%)

📊 HOLDINGS:
📈 BTC: 0.125000 ($6,125.25)
    P/L: +22.50% ($1,125.25)
    Signal: BUY ✅ (85%)
📉 ETH: 0.500000 ($1,095.00)
    P/L: -4.35% ($-50.00)
    Signal: HOLD ⏹️ (55%)
```

#### Performance Analysis
```
📊 PERFORMANCE ANALYSIS

Initial Investment: $10,000.00
Current Value: $12,450.75
Overall Profit: $2,450.75 (+24.51%)

Total Trades: 8
Winning Trades: 6
Losing Trades: 2
Win Rate: 75.00%
Profit Factor: 3.25x

📡 TOKEN METRICS SIGNALS
Signals Followed: 5
Correct Signals: 4
Signal Accuracy: 80.00%

✨ Following TM signals would have improved your performance!
```

## 🔧 Technical Architecture

The project is structured as follows:

```
TM-Signals-Bot/
├── bot.py                  # Main Telegram bot application
├── tm_api.py               # Token Metrics API integration
├── portfolio_manager.py    # Portfolio simulation system
├── subscription_manager.py # Manages user subscriptions
├── scheduler.py            # Handles scheduled alerts
├── test_api.py             # Test script for API integration
├── requirements.txt        # Project dependencies
├── .env.example            # Example environment variables
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Telegram Bot Token (from BotFather)
- Token Metrics API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tm-signals-bot.git
cd tm-signals-bot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TM_API_KEY=your_token_metrics_api_key
```

4. Test the API connection:
```bash
python test_api.py
```

5. Run the bot:
```bash
python bot.py
```

## 🌟 Innovation & Impact

This project demonstrates how the Token Metrics API can be leveraged to create accessible, user-friendly tools for crypto traders of all experience levels. Key innovations include:

1. **Practical API Integration**: Demonstrates real-world application of Token Metrics AI signals
2. **Risk-Free Learning Environment**: Allows users to develop trading skills without financial risk
3. **Signal Performance Validation**: Provides quantifiable metrics on TM signal accuracy
4. **Accessible Trading Interface**: Makes sophisticated AI signals accessible through a familiar messaging platform
5. **Interactive Decision Making**: Users can immediately act on signals with a few taps

## 🔮 Future Enhancements

- Add NLP understanding for natural language queries
- Implement multi-portfolio strategies (conservative, aggressive)
- Add historical backtest against TM signals
- Create leaderboards to compare user performance
- Develop more advanced visualization of portfolio performance
- Add custom alert thresholds for specific tokens

## 📝 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgements

- Token Metrics for providing the powerful API and hosting this challenge
- The python-telegram-bot team for their excellent framework
- CoinGecko for their reliable price API used in the portfolio simulator