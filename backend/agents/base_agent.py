from typing import Dict, Any
import json
import logging
from ..services.openai_service import openai_service

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all agents with common functionality"""
    
    def __init__(self, system_type: str):
        self.system_type = system_type

    async def _generate(self, prompt: str) -> str:
        """Generate completion using OpenAI service"""
        return await openai_service.generate_completion(prompt, self.system_type)

    def _clean_json_string(self, text: str) -> str:
        """Clean and validate JSON string"""
        if not text:
            raise ValueError("Empty response")
            
        text = text.replace('```json', '').replace('```', '')
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in response")
            
        return text[start:end].strip()

    def _parse_json(self, text: str) -> Dict:
        """Parse JSON with error handling"""
        try:
            cleaned = self._clean_json_string(text)
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return {}
