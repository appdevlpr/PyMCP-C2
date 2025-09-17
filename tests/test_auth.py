import unittest
import os
import sys
import jwt

# Add the parent directory to the path so we can import from mcp_server
sys.path.append('../mcp_server')

from auth import generate_token, token_required
from flask import Flask, request, jsonify

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        
    def test_token_generation(self):
        with self.app.app_context():
            token = generate_token('test-agent')
            self.assertIsNotNone(token)
            
            decoded = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
            self.assertEqual(decoded['user'], 'test-agent')

if __name__ == '__main__':
    unittest.main()

