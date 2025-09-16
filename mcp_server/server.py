from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
import threading
import logging

app = Flask(__name__)
api = Api(app)

# In-memory storage for agents and tasks
agents = {}
tasks = {}

class AgentRegistration(Resource):
    def post(self):
        data = request.get_json()
        agent_id = data.get('agent_id')
        hostname = data.get('hostname')
        ip_address = data.get('ip_address')
        
        if agent_id:
            agents[agent_id] = {
                'hostname': hostname,
                'ip_address': ip_address,
                'last_checkin': datetime.now().isoformat()
            }
            return {'status': 'success', 'message': 'Agent registered'}, 200
        return {'status': 'error', 'message': 'Invalid agent data'}, 400

class TaskResource(Resource):
    def get(self, agent_id):
        if agent_id in tasks and tasks[agent_id]:
            return {'task': tasks[agent_id].pop(0)}, 200
        return {'task': None}, 200
    
    def post(self, agent_id):
        data = request.get_json()
        if agent_id in agents:
            if agent_id not in tasks:
                tasks[agent_id] = []
            tasks[agent_id].append(data['task'])
            return {'status': 'success'}, 200
        return {'status': 'error', 'message': 'Agent not found'}, 404

api.add_resource(AgentRegistration, '/register')
api.add_resource(TaskResource, '/task/<string:agent_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
