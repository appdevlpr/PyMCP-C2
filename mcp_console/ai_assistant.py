import openai
import os
from logging_config import setup_logging

logger = setup_logging('ai_assistant')

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        if not self.api_key:
            logger.warning("OpenAI API key not set. AI features will be disabled.")
    
    def analyze_data(self, data):
        if not self.api_key:
            return "AI features disabled. Set OPENAI_API_KEY environment variable."
        
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a security analyst assisting with penetration testing. Provide concise, actionable analysis."},
                    {"role": "user", "content": f"Analyze this security data: {data}"}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return f"Analysis failed: {str(e)}"
    
    def get_suggestions(self, context):
        if not self.api_key:
            return "AI features disabled. Set OPENAI_API_KEY environment variable."
        
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a security analyst assisting with penetration testing. Provide concise, actionable suggestions."},
                    {"role": "user", "content": f"Based on this context: {context}, what should I do next?"}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI suggestion failed: {str(e)}")
            return f"Suggestion failed: {str(e)}"
