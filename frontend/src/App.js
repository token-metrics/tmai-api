import React, { useState } from 'react';
import PortfolioAnalyzer from './components/PortfolioAnalyzer';
import TradingSignals from './components/TradingSignals';
import MarketMetrics from './components/MarketMetrics';
import AiAssistant from './components/AiAssistant';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  // Navigation items
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: 'chart-pie' },
    { id: 'portfolio', label: 'Portfolio', icon: 'briefcase' },
    { id: 'signals', label: 'Signals', icon: 'signal' },
    { id: 'ai-assistant', label: 'AI Assistant', icon: 'robot' },
  ];

  // Render appropriate component based on active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <MarketMetrics />;
      case 'portfolio':
        return <PortfolioAnalyzer />;
      case 'signals':
        return <TradingSignals />;
      case 'ai-assistant':
        return <AiAssistant />;
      default:
        return <MarketMetrics />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">CryptoMetricsDash</h1>
          <div className="text-sm">
            Powered by <a href="https://tokenmetrics.com" target="_blank" rel="noopener noreferrer" className="underline">Token Metrics API</a>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Sidebar */}
          <nav className="w-full md:w-64 bg-white rounded-lg shadow-md p-4">
            <ul>
              {navItems.map((item) => (
                <li key={item.id} className="mb-2">
                  <button
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg flex items-center ${
                      activeTab === item.id
                        ? 'bg-blue-100 text-blue-600'
                        : 'hover:bg-gray-100'
                    }`}
                  >
                    <i className={`fas fa-${item.icon} mr-3`}></i>
                    {item.label}
                  </button>
                </li>
              ))}
            </ul>
            
            {/* Footer links */}
            <div className="mt-8 pt-4 border-t border-gray-200">
              <h4 className="text-sm font-semibold text-gray-500 mb-2">Resources</h4>
              <ul className="text-sm">
                <li className="mb-1">
                  <a 
                    href="https://developers.tokenmetrics.com/docs" 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    API Documentation
                  </a>
                </li>
                <li className="mb-1">
                  <a 
                    href="https://tokenmetrics.com" 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    Token Metrics
                  </a>
                </li>
              </ul>
            </div>
          </nav>

          {/* Main content area */}
          <main className="flex-1">
            {renderContent()}
          </main>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h2 className="text-xl font-bold">CryptoMetricsDash</h2>
              <p className="text-gray-400 text-sm mt-1">
                Built for the Token Metrics Hackathon 2025
              </p>
            </div>
            <div className="text-sm text-gray-400">
              <p>Powered by Token Metrics API</p>
              <p className="mt-1">
                API Key: hack-b3f7d3e9-421d-47a3-b4e0-44dca99c0f0d
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 