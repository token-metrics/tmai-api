import os
import unittest
from unittest import mock

import requests

from tmai_api import TokenMetricsClient
from tmai_api.exceptions import MissingAPIKeyError

class TestTokenMetricsClient(unittest.TestCase):
    
    def setUp(self):
        self.session = mock.Mock(spec=requests.Session)
        # Ensure the mock session exposes a request method for the HTTP layer
        self.session.request = mock.Mock()
        self.client = TokenMetricsClient(api_key="test-api-key", session=self.session)
    
    def test_client_initialization(self):
        self.assertEqual(self.client.api_key, "test-api-key")
        self.assertEqual(self.client.BASE_URL, "https://api.tokenmetrics.com/v2")
        self.assertEqual(self.client.base_url, "https://api.tokenmetrics.com/v2")
        
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

    def test_tokens_endpoint(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"symbol": "BTC", "name": "Bitcoin"}]}
        mock_response.raise_for_status.return_value = None
        self.session.request.return_value = mock_response

        result = self.client.tokens.get(symbol="BTC")

        self.assertEqual(result, {"data": [{"symbol": "BTC", "name": "Bitcoin"}]})

        self.session.request.assert_called_once()
        _, kwargs = self.session.request.call_args
        self.assertEqual(kwargs['params'], {'symbol': 'BTC'})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')
        self.assertEqual(kwargs['method'], 'GET')

    def test_ai_agent_endpoint(self):
        mock_response = mock.Mock()
        payload = {
            "success": True,
            "message": "AI Chatbot response successful",
            "answer": "This is a test answer from the AI chatbot.",
            "thread": [
                {"user": "What is the next 100x coin?"},
                {"chatbot": "This is a test answer from the AI chatbot."}
            ]
        }
        mock_response.json.return_value = payload
        mock_response.raise_for_status.return_value = None
        self.session.request.return_value = mock_response

        question = "What is the next 100x coin?"
        result = self.client.ai_agent.ask(question)

        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("answer"), "This is a test answer from the AI chatbot.")

        self.assertGreaterEqual(self.session.request.call_count, 1)
        _, kwargs = self.session.request.call_args_list[0]
        self.assertEqual(kwargs['json'], {'messages': [{'user': question}]})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')
        self.assertEqual(kwargs['method'], 'POST')

        answer_text = self.client.ai_agent.get_answer_text(question)
        self.assertEqual(answer_text, "This is a test answer from the AI chatbot.")
        self.assertEqual(self.session.request.call_count, 2)

    def test_ai_reports_endpoint(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"report_id": "123", "token": "BTC"}]}
        mock_response.raise_for_status.return_value = None
        self.session.request.return_value = mock_response

        result = self.client.ai_reports.get(symbol="BTC")

        self.assertEqual(result, {"data": [{"report_id": "123", "token": "BTC"}]})

        self.session.request.assert_called()
        _, kwargs = self.session.request.call_args
        self.assertEqual(kwargs['params'], {'symbol': 'BTC'})
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')
        self.assertEqual(kwargs['method'], 'GET')

    def test_trading_signals_endpoint(self):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"data": [{"signal": "1", "token": "BTC"}]}
        mock_response.raise_for_status.return_value = None
        self.session.request.return_value = mock_response

        result = self.client.trading_signals.get(
            symbol="BTC",
            startDate="2023-10-01",
            endDate="2023-10-10",
            signal="1"
        )

        self.assertEqual(result, {"data": [{"signal": "1", "token": "BTC"}]})

        self.session.request.assert_called()
        _, kwargs = self.session.request.call_args
        self.assertEqual(kwargs['params'], {
            'symbol': 'BTC',
            'startDate': '2023-10-01',
            'endDate': '2023-10-10',
            'signal': '1'
        })
        self.assertEqual(kwargs['headers']['api_key'], 'test-api-key')
        self.assertEqual(kwargs['method'], 'GET')

    def test_api_key_from_environment(self):
        with mock.patch.dict(os.environ, {"TMAI_API_KEY": "env-api-key"}):
            client = TokenMetricsClient(session=self.session)
            self.assertEqual(client.api_key, "env-api-key")

    def test_missing_api_key_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(MissingAPIKeyError):
                TokenMetricsClient(session=self.session)

if __name__ == '__main__':
    unittest.main()