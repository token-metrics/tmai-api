import React, { useState, useRef, useEffect } from 'react';
import { aiAPI } from '../services/apiService';

const AiAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Sample suggested questions
  const suggestedQuestions = [
    "What's your prediction for Bitcoin in the next month?",
    "Which altcoins have the best fundamentals right now?",
    "Should I invest in DeFi tokens?",
    "What indicators should I watch for the next bull run?",
    "Explain the Token Metrics Trader Grade"
  ];

  // Scroll to bottom of messages when new ones are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Add initial greeting message
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: "Hello! I'm your Token Metrics AI Assistant. Ask me anything about cryptocurrencies, market trends, or specific tokens, and I'll provide you with AI-powered insights.",
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  // Handle sending a question to the AI agent
  const handleSendMessage = async (question = inputValue) => {
    if (!question.trim()) return;

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: question,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      // Send question to AI agent
      const response = await aiAPI.askQuestion(question);
      
      // Add AI response to chat
      if (response && response.response) {
        const aiMessage = {
          role: 'assistant',
          content: response.response,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Handle error response
        const errorMessage = {
          role: 'assistant',
          content: "I'm sorry, I couldn't process your request. Please try again.",
          timestamp: new Date().toISOString(),
          isError: true
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error querying AI agent:', error);
      
      // Add error message to chat
      const errorMessage = {
        role: 'assistant',
        content: "I'm sorry, an error occurred while processing your request. Please try again.",
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Handle clicking a suggested question
  const handleSuggestedQuestion = (question) => {
    setInputValue(question);
    handleSendMessage(question);
  };

  // Format timestamp
  const formatTimestamp = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Helper to format message content with links, etc.
  const formatMessage = (content) => {
    // Simple markdown-like link formatting
    const formattedContent = content.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g, 
      '<a href="$2" target="_blank" class="text-blue-500 hover:underline">$1</a>'
    );
    
    return { __html: formattedContent };
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md h-full flex flex-col">
      <h2 className="text-2xl font-bold mb-4">Token Metrics AI Assistant</h2>
      
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto mb-4 border border-gray-200 rounded p-4 bg-gray-50">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`mb-4 ${message.role === 'user' ? 'text-right' : ''}`}
          >
            <div 
              className={`inline-block max-w-3/4 px-4 py-2 rounded-lg ${
                message.role === 'user' 
                  ? 'bg-blue-500 text-white rounded-br-none' 
                  : message.isError 
                    ? 'bg-red-100 text-red-700 rounded-bl-none' 
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
              }`}
            >
              <div dangerouslySetInnerHTML={formatMessage(message.content)} />
              <div className={`text-xs mt-1 ${
                message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
              }`}>
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Suggested questions */}
      {messages.length <= 2 && (
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuestion(question)}
                className="bg-gray-100 hover:bg-gray-200 rounded-full px-3 py-1 text-sm text-gray-700"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Input area */}
      <div className="flex items-center">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about crypto..."
          className="flex-1 border border-gray-300 rounded-l px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={1}
          disabled={loading}
        />
        <button
          onClick={() => handleSendMessage()}
          disabled={!inputValue.trim() || loading}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-r disabled:bg-gray-400"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Thinking...
            </span>
          ) : (
            'Send'
          )}
        </button>
      </div>
    </div>
  );
};

export default AiAssistant; 