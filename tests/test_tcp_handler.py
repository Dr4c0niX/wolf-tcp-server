import json
import unittest
from unittest.mock import MagicMock, patch
from app.tcp_handler import TCPRequestHandler

class TestTCPHandler(unittest.TestCase):
    @patch('app.tcp_handler.GameEngine')
    def test_valid_request(self, mock_engine):
        handler = TCPRequestHandler()
        handler.request = MagicMock()
        handler.request.recv.return_value = b'{"action":"list"}'
        
        mock_engine.return_value.process_request.return_value = '{"status":"OK"}'
        handler.handle()
        
        handler.request.sendall.assert_called_with(b'{"status":"OK"}')

    def test_invalid_json(self):
        handler = TCPRequestHandler()
        handler.request = MagicMock()
        handler.request.recv.return_value = b'invalid'
        
        handler.handle()
        response = json.loads(handler.request.sendall.call_args[0][0])
        self.assertEqual(response['status'], 'KO')