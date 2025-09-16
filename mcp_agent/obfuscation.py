import base64
import zlib
import random
import string

def obfuscate_string(s):
    """Obfuscate a string using multiple techniques"""
    # First compress
    compressed = zlib.compress(s.encode())
    # Then base64 encode
    encoded = base64.b64encode(compressed)
    # Add random padding to vary length
    padding = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
    return f"{encoded.decode()}{padding}"

def deobfuscate_string(s):
    """Deobfuscate a string"""
    try:
        # Remove padding (last 5-15 characters are random)
        encoded = s[:-random.randint(5, 15)] if len(s) > 15 else s
        # Base64 decode
        decoded = base64.b64decode(encoded)
        # Decompress
        return zlib.decompress(decoded).decode()
    except:
        # If deobfuscation fails, return original string
        return s

def obfuscate_code(code):
    """Obfuscate Python code by encoding and compressing"""
    compressed = zlib.compress(code.encode())
    return base64.b64encode(compressed).decode()

def deobfuscate_code(obfuscated_code):
    """Deobfuscate Python code"""
    try:
        decoded = base64.b64decode(obfuscated_code)
        return zlib.decompress(decoded).decode()
    except:
        return obfuscated_code

