import React, { useState, useEffect } from 'react';
import { marketAPI } from '../services/apiService';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const MarketMetrics = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState('30d'); // Default to 30 days

  // Fetch market metrics on component mount and when time range changes
  useEffect(() => {
    fetchMarketMetrics();
  }, [timeRange]);

  // Fetch market metrics from API
  const fetchMarketMetrics = async () => {
    setLoading(true);
    setError(null);

    try {
      // Calculate date range based on selected time range
      const endDate = new Date().toISOString().split('T')[0];
      let startDate;

      switch (timeRange) {
        case '7d':
          startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
          break;
        case '30d':
          startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
          break;
        case '90d':
          startDate = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
          break;
        case '180d':
          startDate = new Date(Date.now() - 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
          break;
        default:
          startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      }

      const response = await marketAPI.getMarketMetrics({
        startDate,
        endDate,
        limit: 180 // Get enough data for the longest time range
      });

      if (response && response.data) {
        // Sort by date in ascending order for charts
        const sortedData = [...response.data].sort((a, b) => new Date(a.DATE) - new Date(b.DATE));
        setMetrics(sortedData);
      }
    } catch (err) {
      console.error('Error fetching market metrics:', err);
      setError('Failed to fetch market metrics. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle time range change
  const handleTimeRangeChange = (e) => {
    setTimeRange(e.target.value);
  };

  // Format date for display
  const formatDate = (dateString) => {
    const options = { month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  // Prepare data for Market Sentiment chart
  const sentimentChartData = {
    labels: metrics.map(item => formatDate(item.DATE)),
    datasets: [
      {
        label: 'Market Sentiment',
        data: metrics.map(item => item.MARKET_SENTIMENT),
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        tension: 0.4
      }
    ]
  };

  // Prepare data for Bitcoin Dominance chart
  const btcDominanceChartData = {
    labels: metrics.map(item => formatDate(item.DATE)),
    datasets: [
      {
        label: 'Bitcoin Dominance',
        data: metrics.map(item => item.BTC_DOMINANCE),
        fill: true,
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        borderColor: 'rgba(255, 159, 64, 1)',
        tension: 0.4
      }
    ]
  };

  // Chart options
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
    elements: {
      point: {
        radius: 1,
      },
    },
  };

  // Helper to get color based on indicator value
  const getIndicatorColor = (value) => {
    if (value >= 75) return 'bg-green-500';
    if (value >= 50) return 'bg-blue-500';
    if (value >= 25) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Helper to get text based on indicator value
  const getIndicatorText = (value) => {
    if (value >= 75) return 'Very Bullish';
    if (value >= 50) return 'Bullish';
    if (value >= 25) return 'Bearish';
    return 'Very Bearish';
  };

  // Get the most recent metric
  const latestMetric = metrics.length > 0 ? metrics[metrics.length - 1] : null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Market Metrics</h2>

      {/* Time range selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Time Range
        </label>
        <div className="flex space-x-4">
          <button
            onClick={() => setTimeRange('7d')}
            className={`px-4 py-2 rounded ${
              timeRange === '7d' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            7D
          </button>
          <button
            onClick={() => setTimeRange('30d')}
            className={`px-4 py-2 rounded ${
              timeRange === '30d' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            30D
          </button>
          <button
            onClick={() => setTimeRange('90d')}
            className={`px-4 py-2 rounded ${
              timeRange === '90d' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            90D
          </button>
          <button
            onClick={() => setTimeRange('180d')}
            className={`px-4 py-2 rounded ${
              timeRange === '180d' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            180D
          </button>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mb-4 rounded">
          {error}
        </div>
      )}

      {/* Loading state */}
      {loading ? (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <>
          {/* Current market metrics */}
          {latestMetric && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold mb-4">Current Market Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Market Sentiment */}
                <div className="bg-gray-50 p-4 rounded-lg shadow">
                  <div className="text-sm text-gray-500 mb-1">Market Sentiment</div>
                  <div className="text-2xl font-bold mb-2">{latestMetric.MARKET_SENTIMENT.toFixed(2)}</div>
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                    <div 
                      className={`h-4 rounded-full ${getIndicatorColor(latestMetric.MARKET_SENTIMENT)}`}
                      style={{ width: `${latestMetric.MARKET_SENTIMENT}%` }}
                    ></div>
                  </div>
                  <div className="text-sm font-medium">
                    {getIndicatorText(latestMetric.MARKET_SENTIMENT)}
                  </div>
                </div>

                {/* BTC Dominance */}
                <div className="bg-gray-50 p-4 rounded-lg shadow">
                  <div className="text-sm text-gray-500 mb-1">BTC Dominance</div>
                  <div className="text-2xl font-bold mb-2">{latestMetric.BTC_DOMINANCE.toFixed(2)}%</div>
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                    <div 
                      className="h-4 rounded-full bg-orange-500"
                      style={{ width: `${latestMetric.BTC_DOMINANCE}%` }}
                    ></div>
                  </div>
                  <div className="text-sm font-medium">
                    {latestMetric.BTC_DOMINANCE > 50 ? 'Bitcoin Dominant' : 'Altcoin Season'}
                  </div>
                </div>

                {/* Last Updated */}
                <div className="bg-gray-50 p-4 rounded-lg shadow">
                  <div className="text-sm text-gray-500 mb-1">Last Updated</div>
                  <div className="text-2xl font-bold mb-2">
                    {new Date(latestMetric.DATE).toLocaleDateString()}
                  </div>
                  <div className="text-sm font-medium">
                    {new Date(latestMetric.DATE).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Charts */}
          <div className="grid grid-cols-1 gap-8">
            {/* Market Sentiment Chart */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Market Sentiment</h3>
              <div className="h-80">
                <Line data={sentimentChartData} options={chartOptions} />
              </div>
            </div>

            {/* BTC Dominance Chart */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Bitcoin Dominance</h3>
              <div className="h-80">
                <Line data={btcDominanceChartData} options={chartOptions} />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default MarketMetrics; 