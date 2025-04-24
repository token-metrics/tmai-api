import React, { useState, useEffect } from 'react';
import { marketAPI, tokenAPI } from '../services/apiService';

const TradingSignals = () => {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    category: '',
    signal: '',
    symbols: ''
  });
  const [categories, setCategories] = useState([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  // Fetch initial data on component mount
  useEffect(() => {
    fetchTradingSignals();
    fetchCategories();
  }, []);

  // Fetch data when filters or page changes
  useEffect(() => {
    fetchTradingSignals();
  }, [filters, page]);

  // Fetch trading signals from API
  const fetchTradingSignals = async () => {
    setLoading(true);
    setError(null);

    try {
      // Get current date and date 7 days ago for default range
      const endDate = new Date().toISOString().split('T')[0];
      const startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

      const params = {
        startDate,
        endDate,
        limit: 20,
        page
      };

      // Add filters if provided
      if (filters.category) params.category = filters.category;
      if (filters.signal) params.signal = filters.signal;
      if (filters.symbols) params.symbols = filters.symbols;

      const response = await marketAPI.getTradingSignals(params);

      if (response && response.data) {
        // If this is the first page, replace signals, otherwise append
        if (page === 0) {
          setSignals(response.data);
        } else {
          setSignals(prev => [...prev, ...response.data]);
        }

        // Check if there are more results to fetch
        setHasMore(response.data.length === 20);
      } else {
        setHasMore(false);
      }
    } catch (err) {
      console.error('Error fetching trading signals:', err);
      setError('Failed to fetch trading signals. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch available categories
  const fetchCategories = async () => {
    try {
      const tokens = await tokenAPI.getTokens({ limit: 5 });
      if (tokens && tokens.data) {
        // Extract unique categories
        const categoriesSet = new Set();
        tokens.data.forEach(token => {
          if (token.CATEGORIES) {
            const tokenCategories = token.CATEGORIES.split(',').map(cat => cat.trim());
            tokenCategories.forEach(cat => categoriesSet.add(cat));
          }
        });
        
        setCategories(Array.from(categoriesSet).sort());
      }
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  // Handle filter changes
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
    setPage(0); // Reset to first page when filters change
  };

  // Handle load more
  const handleLoadMore = () => {
    setPage(prev => prev + 1);
  };

  // Format date for display
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Helper to get signal text and color
  const getSignalInfo = (signal) => {
    if (signal === 1) {
      return { text: 'BUY', color: 'text-green-600' };
    } else if (signal === -1) {
      return { text: 'SELL', color: 'text-red-600' };
    } else {
      return { text: 'HOLD', color: 'text-gray-600' };
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Trading Signals</h2>

      {/* Filters */}
      <div className="bg-gray-50 p-4 rounded mb-6">
        <h3 className="text-lg font-semibold mb-3">Filters</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              name="category"
              value={filters.category}
              onChange={handleFilterChange}
              className="px-3 py-2 border border-gray-300 rounded w-full"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Signal
            </label>
            <select
              name="signal"
              value={filters.signal}
              onChange={handleFilterChange}
              className="px-3 py-2 border border-gray-300 rounded w-full"
            >
              <option value="">All Signals</option>
              <option value="1">Buy</option>
              <option value="-1">Sell</option>
              <option value="0">Hold</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Symbols (comma-separated)
            </label>
            <input
              type="text"
              name="symbols"
              value={filters.symbols}
              onChange={handleFilterChange}
              placeholder="e.g., BTC,ETH,SOL"
              className="px-3 py-2 border border-gray-300 rounded w-full"
            />
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mb-4 rounded">
          {error}
        </div>
      )}

      {/* Loading state */}
      {loading && page === 0 && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      )}

      {/* Signals table */}
      {signals.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead>
              <tr>
                <th className="px-4 py-2 border">Token</th>
                <th className="px-4 py-2 border">Signal</th>
                <th className="px-4 py-2 border">Trader Grade</th>
                <th className="px-4 py-2 border">Date</th>
              </tr>
            </thead>
            <tbody>
              {signals.map((signal, index) => {
                const signalInfo = getSignalInfo(signal.TRADING_SIGNAL);
                return (
                  <tr key={index}>
                    <td className="px-4 py-2 border">
                      <div className="font-semibold">{signal.TOKEN_SYMBOL}</div>
                      <div className="text-xs text-gray-500">{signal.NAME}</div>
                    </td>
                    <td className={`px-4 py-2 border ${signalInfo.color} font-semibold`}>
                      {signalInfo.text}
                    </td>
                    <td className="px-4 py-2 border">
                      <div className="w-full bg-gray-200 rounded-full h-4">
                        <div 
                          className={`h-4 rounded-full ${
                            signal.TM_TRADER_GRADE >= 70 ? 'bg-green-500' : 
                            signal.TM_TRADER_GRADE >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${signal.TM_TRADER_GRADE}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-center mt-1">
                        {signal.TM_TRADER_GRADE}/100
                      </div>
                    </td>
                    <td className="px-4 py-2 border">
                      {formatDate(signal.DATE)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : !loading ? (
        <div className="text-center py-8 text-gray-500">
          No trading signals found matching your criteria.
        </div>
      ) : null}

      {/* Load more button */}
      {signals.length > 0 && hasMore && (
        <div className="mt-6 text-center">
          <button
            onClick={handleLoadMore}
            disabled={loading}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
          >
            {loading ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}
    </div>
  );
};

export default TradingSignals; 