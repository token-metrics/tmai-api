# CryptoMetricsDash

![CryptoMetricsDash](https://img.shields.io/badge/Token%20Metrics-API-blue)

CryptoMetricsDash is a full-stack web application that leverages the Token Metrics API to provide cryptocurrency traders and investors with real-time market insights, portfolio optimization, and AI-powered recommendations.

Built for the Token Metrics Innovation Challenge 2025, this application demonstrates how to integrate the Token Metrics API into a user-friendly dashboard that enables data-driven investment decisions.

## 🚀 Features

- **Market Dashboard**: Visualize market sentiment, Bitcoin dominance, and other key metrics
- **Portfolio Analyzer**: Analyze and optimize your portfolio based on Token Metrics AI signals
- **Trading Signals**: Get real-time trading signals with filtering by category, symbol, and signal type
- **AI Assistant**: Chat with Token Metrics AI to get personalized market insights and recommendations

## 🛠️ Technology Stack

### Backend

- **Flask**: Python web framework for the API layer
- **Token Metrics API**: Integration with Token Metrics endpoints
- **Pandas**: Data manipulation and analysis

### Frontend

- **React**: UI library for building the user interface
- **Chart.js**: Data visualization library for charts
- **Tailwind CSS**: Utility-first CSS framework for styling

## 🏗️ Architecture

The application follows a client-server architecture:

1. **Backend API Server**: A Flask application that handles requests from the frontend and communicates with the Token Metrics API.
2. **Frontend Web Application**: A React application that provides the user interface and interacts with the backend API.

## 📋 API Endpoints Used

- `/tokens`: Get token information
- `/trader-grades`: Get trader grades for tokens
- `/trading-signals`: Get trading signals for tokens
- `/market-metrics`: Get market sentiment and metrics
- `/price`: Get current token prices
- `/tmai`: Interact with the Token Metrics AI assistant

## 📦 Project Structure

```
crypto-metrics-dash/
├── backend/
│   ├── app.py                # Flask application
│   ├── tm_api.py             # Token Metrics API client
│   ├── portfolio.py          # Portfolio management logic
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── public/               # Static assets
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── App.js            # Main app component
│   │   └── index.js          # Entry point
│   ├── package.json          # JS dependencies
│   └── tailwind.config.js    # Tailwind CSS configuration
├── .env.example              # Example environment variables
├── .cursorrules              # Cursor editor rules
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.9 or higher)
- Token Metrics API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/crypto-metrics-dash.git
   cd crypto-metrics-dash
   ```

2. **Set up the backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**:
   ```bash
   cd ../frontend
   npm install
   ```

4. **Create a `.env` file in the project root** based on `.env.example`:
   ```
   TM_API_KEY=your_api_key_here
   FLASK_ENV=development
   PORT=5000
   ```

### Running the Application

1. **Start the backend server**:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```

2. **Start the frontend development server**:
   ```bash
   cd ../frontend
   npm start
   ```

3. **Open the application** in your browser at `http://localhost:3000`

## 🔑 API Key

For the Token Metrics Innovation Challenge, use the following API key:
```
hack-b3f7d3e9-421d-47a3-b4e0-44dca99c0f0d
```

## 📚 Usage

### Market Dashboard

The dashboard provides an overview of the current market sentiment, Bitcoin dominance, and other key metrics. You can adjust the time range to view historical data.

### Portfolio Analyzer

1. Add your cryptocurrency holdings by entering the symbol and amount
2. Click "Analyze Portfolio" to get a detailed analysis of your portfolio
3. Click "Optimize Portfolio" to get recommendations for portfolio rebalancing

### Trading Signals

View real-time trading signals from Token Metrics AI. You can filter signals by:
- Category
- Signal type (Buy, Sell, Hold)
- Specific symbols

### AI Assistant

Chat with the Token Metrics AI assistant to get personalized market insights and recommendations. Ask questions about:
- Token fundamentals
- Market trends
- Trading strategies
- Token Metrics indicators

## 🔒 Security

This application does not store any user data. Your portfolio information is only stored in your browser's memory and is never sent to any server except for analysis with the Token Metrics API.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Token Metrics](https://tokenmetrics.com) for providing the powerful API
- The Token Metrics Innovation Challenge for the opportunity to showcase our work

---

Built with ❤️ for the Token Metrics Innovation Challenge 2025