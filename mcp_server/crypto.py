from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

# Generate or load encryption key
def get_encryption_key():
    key_env = os.getenv('ENCRYPTION_KEY')
    if key_env:
        # Derive key from environment variable
        salt = b'fixed_salt_use_random_in_production'  # Change this!
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(key_env.encode()))
    else:
        # Generate a new key (for development)
        return Fernet.generate_key()

fernet = Fernet(get_encryption_key())

def encrypt_data(data):
    if isinstance(data, dict):
        data = str(data)
    encrypted = fernet.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    try:
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = fernet.decrypt(decoded).decode()
        # Try to convert back to dict if possible
        try:
            return eval(decrypted)
        except:
            return decrypted
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

