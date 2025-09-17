import logging
from flask import Flask, request, jsonify, current_app
from flask_restful import Api, Resource
from datetime import datetime, timedelta
import jwt
from functools import wraps
from logging_config import setup_logging
from crypto import encrypt_data, decrypt_data
from auth import token_required, generate_token

# Initialize logging
logger = setup_logging('server')

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'your-secret-key'  # Should be set from environment variable

# In-memory storage for agents and tasks
agents = {}
tasks = {}
results = {}

class AgentRegistration(Resource):
    def post(self):
        try:
            encrypted_data = request.get_json().get('data')
            if not encrypted_data:
                return {'message': 'No data provided'}, 400
            
            data = decrypt_data(encrypted_data)
            
            agent_id = data.get('agent_id')
            hostname = data.get('hostname')
            ip_address = data.get('ip_address')
            
            if agent_id:
                agents[agent_id] = {
                    'hostname': hostname,
                    'ip_address': ip_address,
                    'last_checkin': datetime.now().isoformat(),
                    'status': 'active'
                }
                logger.info(f"New agent registered: {agent_id}")
                
                # Create token for agent
                token = generate_token(agent_id)
                
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
            encrypted_data = request.get_json().get('data')
            if not encrypted_data:
                return {'message': 'No data provided'}, 400
            
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

class ResultResource(Resource):
    @token_required
    def post(self, current_user, agent_id):
        try:
            encrypted_data = request.get_json().get('data')
            if not encrypted_data:
                return {'message': 'No data provided'}, 400
            
            data = decrypt_data(encrypted_data)
            
            if agent_id not in results:
                results[agent_id] = []
            results[agent_id].append(data)
            logger.info(f"Result received from agent {agent_id}")
            return {'message': 'success'}, 200
            
        except Exception as e:
            logger.error(f"Result handling error: {str(e)}")
            return {'message': 'Internal server error'}, 500

class StatusResource(Resource):
    def get(self):
        return {'status': 'online', 'timestamp': datetime.now().isoformat()}, 200

api.add_resource(AgentRegistration, '/register')
api.add_resource(TaskResource, '/task/<string:agent_id>')
api.add_resource(ResultResource, '/result/<string:agent_id>')
api.add_resource(StatusResource, '/status')

if __name__ == '__main__':
    # For production, use proper SSL certificates
    context = ('cert.pem', 'key.pem')  # Generate these with OpenSSL
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=False)
