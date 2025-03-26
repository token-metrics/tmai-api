import unittest
from unittest import mock
from tmai_api import TokenMetricsClient

class TestTokenMetricsClient(unittest.TestCase):
    
    def setUp(self):
        self.client = TokenMetricsClient(api_key="test-api-key")
    
    def test_client_initialization(self):
        self.assertEqual(self.client.api_key, "test-api-key")
        self.assertEqual(self.client.BASE_URL, "https://api.tokenmetrics.com/v2")
        
        # Check that all endpoints are initialized
        self.assertIsNotNone(self.client.tokens)
        self.assertIsNotNone(self.client.hourly_ohlcv)
        self.assertIsNotNone(self.client.investor_grades)
        self.assertIsNotNone(self.client.trader_grades)
        self.assertIsNotNone(self.client.trader_indices)
        self.assertIsNotNone(self.client.market_metrics)
        
        # Check new endpoints are initialized
        self.assertIsNotNone(self.client.ai_agent)
        self.assertIsNotNone(self.client.ai_reports)
        self.assertIsNotNone(self.client.trading_signals)

    @mock.patch('requests.get')
    def test_tokens_endpoint(self, mock_get):
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"symbol": "BTC", "name": "Bitcoin"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.tokens.get(symbol="BTC")
        
        # Verify the result
        self.assertEqual(result, {"data": [{"symbol": "BTC", "name": "Bitcoin"}]})
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params'], {'symbol': 'BTC'})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')

    @mock.patch('requests.post')
    def test_ai_agent_endpoint(self, mock_post):
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "success": True,
            "message": "AI Chatbot response successful",
            "answer": "This is a test answer from the AI chatbot.",
            "thread": [
                {"user": "What is the next 100x coin?"},
                {"chatbot": "This is a test answer from the AI chatbot."}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the endpoint
        question = "What is the next 100x coin?"
        result = self.client.ai_agent.ask(question)
        
        # Verify the result
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("answer"), "This is a test answer from the AI chatbot.")
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], {'messages': [{'user': question}]})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')
        
        # Test get_answer_text method
        answer_text = self.client.ai_agent.get_answer_text(question)
        self.assertEqual(answer_text, "This is a test answer from the AI chatbot.")

    @mock.patch('requests.get')
    def test_ai_reports_endpoint(self, mock_get):
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"report_id": "123", "token": "BTC"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.ai_reports.get(symbol="BTC")
        
        # Verify the result
        self.assertEqual(result, {"data": [{"report_id": "123", "token": "BTC"}]})
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params'], {'symbol': 'BTC'})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')

    @mock.patch('requests.get')
    def test_trading_signals_endpoint(self, mock_get):
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"signal": "1", "token": "BTC"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.trading_signals.get(
            symbol="BTC", 
            startDate="2023-10-01", 
            endDate="2023-10-10",
            signal="1"
        )
        
        # Verify the result
        self.assertEqual(result, {"data": [{"signal": "1", "token": "BTC"}]})
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params'], {
            'symbol': 'BTC', 
            'startDate': '2023-10-01', 
            'endDate': '2023-10-10',
            'signal': '1'
        })
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')

if __name__ == '__main__':
    unittest.main()