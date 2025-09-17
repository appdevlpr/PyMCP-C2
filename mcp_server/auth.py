import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from logging_config import setup_logger

logger = setup_logger('auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Unauthorized access attempt - no token provided")
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
                
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token attempt")
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid token attempt")
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id, expiration_hours=24):
    try:
        if 'SECRET_KEY' not in current_app.config:
            logger.error("SECRET_KEY not configured in application")
            raise ValueError("Server configuration error: SECRET_KEY not set")
            
        secret_key = current_app.config['SECRET_KEY']
        # Rest of the function...
        
        token = jwt.encode({
            'user': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours)
        }, secret_key, algorithm="HS256")
        
        return token
    except Exception as e:
        logger.error(f"Token generation failed: {str(e)}")
        raise


def refresh_token(old_token, expiration_hours=24):
    try:
        # Decode without verification to get user info
        data = jwt.decode(old_token, options={"verify_signature": False})
        user_id = data['user']
        
        # Generate a new token
        return generate_token(user_id, expiration_hours)
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise
