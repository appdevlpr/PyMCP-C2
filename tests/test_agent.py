import unittest
import os
import sys

# Add the parent directory to the path so we can import from mcp_agent
sys.path.append('../mcp_agent')

from agent import Agent

class TestAgent(unittest.TestCase):
    def test_agent_creation(self):
        agent = Agent('http://test-server:8000', 'test-agent')
        self.assertEqual(agent.agent_id, 'test-agent')
        
    def test_id_generation(self):
        agent = Agent('http://test-server:8000')
        self.assertIsNotNone(agent.agent_id)
        self.assertIn(agent.hostname, agent.agent_id)

if __name__ == '__main__':
    unittest.main()

