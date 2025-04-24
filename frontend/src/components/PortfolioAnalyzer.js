import React, { useState, useEffect } from 'react';
import { portfolioAPI, tokenAPI } from '../services/apiService';

const PortfolioAnalyzer = () => {
  const [holdings, setHoldings] = useState({});
  const [portfolioData, setPortfolioData] = useState(null);
  const [optimizedData, setOptimizedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableTokens, setAvailableTokens] = useState([]);
  const [newTokenSymbol, setNewTokenSymbol] = useState('');
  const [newTokenAmount, setNewTokenAmount] = useState('');
  const [riskTolerance, setRiskTolerance] = useState('medium');

  // Fetch available tokens on component mount
  useEffect(() => {
    const fetchTopTokens = async () => {
      try {
        const response = await tokenAPI.getTopTokens(50);
        if (response.data) {
          const tokens = response.data.map(token => ({
            symbol: token.TOKEN_SYMBOL,
            name: token.NAME,
            id: token.TOKEN_ID
          }));
          setAvailableTokens(tokens);
        }
      } catch (err) {
        setError('Failed to fetch available tokens');
        console.error(err);
      }
    };

    fetchTopTokens();
  }, []);

  // Handle adding a new token to the portfolio
  const handleAddToken = (e) => {
    e.preventDefault();
    if (!newTokenSymbol || !newTokenAmount || isNaN(newTokenAmount) || Number(newTokenAmount) <= 0) {
      setError('Please enter a valid token symbol and amount');
      return;
    }

    // Check if token exists in available tokens
    const tokenExists = availableTokens.some(token => 
      token.symbol.toLowerCase() === newTokenSymbol.toLowerCase()
    );

    if (!tokenExists) {
      setError(`Token ${newTokenSymbol} not found in available tokens`);
      return;
    }

    // Add or update token in holdings
    setHoldings(prev => ({
      ...prev,
      [newTokenSymbol.toUpperCase()]: Number(newTokenAmount)
    }));

    // Clear inputs
    setNewTokenSymbol('');
    setNewTokenAmount('');
    setError(null);
  };

  // Handle removing a token from the portfolio
  const handleRemoveToken = (symbol) => {
    const updatedHoldings = { ...holdings };
    delete updatedHoldings[symbol];
    setHoldings(updatedHoldings);
  };

  // Analyze the portfolio
  const analyzePortfolio = async () => {
    if (Object.keys(holdings).length === 0) {
      setError('Please add at least one token to your portfolio');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await portfolioAPI.analyzePortfolio(holdings);
      setPortfolioData(result);
      setOptimizedData(null); // Clear previous optimization
    } catch (err) {
      setError('Failed to analyze portfolio: ' + (err.message || 'Unknown error'));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Optimize the portfolio
  const optimizePortfolio = async () => {
    if (Object.keys(holdings).length === 0) {
      setError('Please add at least one token to your portfolio');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await portfolioAPI.optimizePortfolio(holdings, riskTolerance);
      setOptimizedData(result);
    } catch (err) {
      setError('Failed to optimize portfolio: ' + (err.message || 'Unknown error'));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Format numbers for display
  const formatNumber = (num, decimals = 2) => {
    if (num === undefined || num === null) return 'N/A';
    return Number(num).toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  // Format currency for display
  const formatCurrency = (num, decimals = 2) => {
    if (num === undefined || num === null) return 'N/A';
    return '$' + formatNumber(num, decimals);
  };

  // Helper to get color based on signal
  const getSignalColor = (signal) => {
    if (signal === 1) return 'text-green-600';
    if (signal === -1) return 'text-red-600';
    return 'text-gray-600';
  };

  // Get text for signal
  const getSignalText = (signal) => {
    if (signal === 1) return 'BUY';
    if (signal === -1) return 'SELL';
    return 'HOLD';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Portfolio Analyzer</h2>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mb-4 rounded">
          {error}
        </div>
      )}

      {/* Add token form */}
      <div className="mb-6 bg-gray-50 p-4 rounded">
        <h3 className="text-lg font-semibold mb-3">Add Token to Portfolio</h3>
        <form onSubmit={handleAddToken} className="flex flex-wrap gap-3">
          <div className="flex-grow">
            <label className="block text-sm font-medium text-gray-700 mb-1">Token Symbol</label>
            <input
              type="text"
              value={newTokenSymbol}
              onChange={(e) => setNewTokenSymbol(e.target.value)}
              placeholder="e.g. BTC"
              className="px-3 py-2 border border-gray-300 rounded w-full"
              list="available-tokens"
            />
            <datalist id="available-tokens">
              {availableTokens.map(token => (
                <option key={token.id} value={token.symbol}>
                  {token.name}
                </option>
              ))}
            </datalist>
          </div>
          <div className="flex-grow">
            <label className="block text-sm font-medium text-gray-700 mb-1">Amount</label>
            <input
              type="number"
              step="any"
              min="0"
              value={newTokenAmount}
              onChange={(e) => setNewTokenAmount(e.target.value)}
              placeholder="e.g. 0.5"
              className="px-3 py-2 border border-gray-300 rounded w-full"
            />
          </div>
          <div className="flex-shrink-0 self-end">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              Add Token
            </button>
          </div>
        </form>
      </div>

      {/* Current holdings */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3">Current Holdings</h3>
        {Object.keys(holdings).length === 0 ? (
          <p className="text-gray-500">No tokens added yet. Add some tokens to analyze your portfolio.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="px-4 py-2 border">Token</th>
                  <th className="px-4 py-2 border">Amount</th>
                  <th className="px-4 py-2 border">Actions</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(holdings).map(([symbol, amount]) => (
                  <tr key={symbol}>
                    <td className="px-4 py-2 border">{symbol}</td>
                    <td className="px-4 py-2 border">{formatNumber(amount, 8)}</td>
                    <td className="px-4 py-2 border">
                      <button
                        onClick={() => handleRemoveToken(symbol)}
                        className="text-red-500 hover:text-red-700"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Risk tolerance selection */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3">Risk Tolerance</h3>
        <div className="flex gap-4">
          <label className="inline-flex items-center">
            <input
              type="radio"
              name="riskTolerance"
              value="low"
              checked={riskTolerance === 'low'}
              onChange={() => setRiskTolerance('low')}
              className="form-radio"
            />
            <span className="ml-2">Low</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              name="riskTolerance"
              value="medium"
              checked={riskTolerance === 'medium'}
              onChange={() => setRiskTolerance('medium')}
              className="form-radio"
            />
            <span className="ml-2">Medium</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              name="riskTolerance"
              value="high"
              checked={riskTolerance === 'high'}
              onChange={() => setRiskTolerance('high')}
              className="form-radio"
            />
            <span className="ml-2">High</span>
          </label>
        </div>
      </div>

      {/* Action buttons */}
      <div className="mb-6 flex gap-3">
        <button
          onClick={analyzePortfolio}
          disabled={loading || Object.keys(holdings).length === 0}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
        >
          {loading ? 'Loading...' : 'Analyze Portfolio'}
        </button>
        <button
          onClick={optimizePortfolio}
          disabled={loading || Object.keys(holdings).length === 0}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
        >
          {loading ? 'Loading...' : 'Optimize Portfolio'}
        </button>
      </div>

      {/* Portfolio analysis results */}
      {portfolioData && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Portfolio Analysis</h3>
          
          {/* Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-blue-50 p-4 rounded">
              <p className="text-sm text-gray-600">Total Value</p>
              <p className="text-xl font-bold">{formatCurrency(portfolioData.total_value)}</p>
            </div>
            <div className="bg-blue-50 p-4 rounded">
              <p className="text-sm text-gray-600">Assets</p>
              <p className="text-xl font-bold">{portfolioData.assets.length}</p>
            </div>
            <div className="bg-blue-50 p-4 rounded">
              <p className="text-sm text-gray-600">Portfolio Sentiment</p>
              <p className="text-xl font-bold">
                {portfolioData.metrics.sentiment}
              </p>
            </div>
          </div>
          
          {/* Assets table */}
          <div className="overflow-x-auto mb-4">
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="px-4 py-2 border">Token</th>
                  <th className="px-4 py-2 border">Amount</th>
                  <th className="px-4 py-2 border">Price</th>
                  <th className="px-4 py-2 border">Value</th>
                  <th className="px-4 py-2 border">Weight</th>
                  <th className="px-4 py-2 border">Signal</th>
                  <th className="px-4 py-2 border">Grade</th>
                </tr>
              </thead>
              <tbody>
                {portfolioData.assets.map((asset) => (
                  <tr key={asset.symbol}>
                    <td className="px-4 py-2 border">{asset.symbol}</td>
                    <td className="px-4 py-2 border">{formatNumber(asset.amount, 8)}</td>
                    <td className="px-4 py-2 border">{formatCurrency(asset.price)}</td>
                    <td className="px-4 py-2 border">{formatCurrency(asset.value)}</td>
                    <td className="px-4 py-2 border">{formatNumber(asset.weight)}%</td>
                    <td className={`px-4 py-2 border ${getSignalColor(asset.signal)}`}>
                      {getSignalText(asset.signal)}
                    </td>
                    <td className="px-4 py-2 border">{formatNumber(asset.grade)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Recommendations */}
          {portfolioData.recommendations.length > 0 && (
            <div className="mb-4">
              <h4 className="text-md font-semibold mb-2">Recommendations</h4>
              <ul className="list-disc pl-5">
                {portfolioData.recommendations.map((rec, index) => (
                  <li key={index} className="mb-1">
                    <span className={rec.action === 'BUY' ? 'text-green-600' : 'text-red-600'}>
                      {rec.action}
                    </span>
                    {` ${rec.symbol}: ${rec.reason}`}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Portfolio optimization results */}
      {optimizedData && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Portfolio Optimization</h3>
          <p className="mb-3">
            Optimized portfolio based on {optimizedData.risk_tolerance} risk tolerance.
          </p>
          
          {/* Actions table */}
          <div className="overflow-x-auto mb-4">
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="px-4 py-2 border">Token</th>
                  <th className="px-4 py-2 border">Action</th>
                  <th className="px-4 py-2 border">Current Weight</th>
                  <th className="px-4 py-2 border">Optimized Weight</th>
                  <th className="px-4 py-2 border">Change</th>
                </tr>
              </thead>
              <tbody>
                {optimizedData.actions.map((action) => (
                  <tr key={action.symbol}>
                    <td className="px-4 py-2 border">{action.symbol}</td>
                    <td className={`px-4 py-2 border ${
                      action.action === 'INCREASE' ? 'text-green-600' : 
                      action.action === 'DECREASE' ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {action.action}
                    </td>
                    <td className="px-4 py-2 border">
                      {formatNumber(optimizedData.current[action.symbol].percent)}%
                    </td>
                    <td className="px-4 py-2 border">
                      {formatNumber(optimizedData.optimized[action.symbol].percent)}%
                    </td>
                    <td className={`px-4 py-2 border ${
                      action.delta_percent > 0 ? 'text-green-600' : 
                      action.delta_percent < 0 ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {action.delta_percent > 0 ? '+' : ''}{formatNumber(action.delta_percent)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default PortfolioAnalyzer; 