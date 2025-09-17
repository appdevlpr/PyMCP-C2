import unittest
import os
import sys

# Add the parent directory to the path so we can import from mcp_server
sys.path.append('../mcp_server')

from crypto import encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):
    def setUp(self):
        # Set a test encryption key
        os.environ['ENCRYPTION_KEY'] = 'test-key-1234567890'
    
    def test_encryption_decryption(self):
        test_data = {"message": "Hello, World!", "number": 42}
        
        encrypted = encrypt_data(test_data)
        decrypted = decrypt_data(encrypted)
        
        self.assertEqual(test_data, decrypted)
    
    def test_string_encryption(self):
        test_string = "This is a test string"
        
        encrypted = encrypt_data(test_string)
        decrypted = decrypt_data(encrypted)
        
        self.assertEqual(test_string, decrypted)

if __name__ == '__main__':
    unittest.main()
