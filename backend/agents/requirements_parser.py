from typing import Dict
import json
import logging
from ..services.openai_service import openai_service  # Import the singleton instance
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class RequirementsParser(BaseAgent):
    def __init__(self):
        super().__init__("requirements")
        self.prompt_template = '''Given this system requirement: "{requirements}"

Generate a structured response as a valid JSON object:
{{
    "functional": ["List of functional requirements"],
    "non_functional": ["List of scalability, reliability, etc. requirements"],
    "constraints": ["List of technical constraints"],
    "load_characteristics": {{
        "users": "expected user count",
        "data": "expected data size",
        "traffic": "expected traffic volume"
    }}
}}'''

    async def parse(self, requirements: str) -> Dict:
        try:
            prompt = self.prompt_template.format(requirements=requirements)
            result = await openai_service.generate_completion(prompt, "requirements")  # Use the service directly
            
            if not result:
                logger.error("Empty response from OpenAI")
                return self._get_default_requirements()
            
            logger.debug(f"Raw response: {result}")
            
            return self._validate_requirements(self._parse_json(result))  # <-- fix here
            
        except Exception as e:
            logger.error(f"Error parsing requirements: {str(e)}", exc_info=True)
            return self._get_default_requirements()

    def _get_default_requirements(self) -> Dict:
        return {
            "functional": ["Basic web application"],
            "non_functional": ["Standard availability"],
            "constraints": [],
            "load_characteristics": {"users": "low", "data": "small", "traffic": "minimal"}
        }

    def _validate_requirements(self, reqs: Dict) -> Dict:
        default = self._get_default_requirements()
        return {
            "functional": reqs.get("functional", default["functional"]),
            "non_functional": reqs.get("non_functional", default["non_functional"]),
            "constraints": reqs.get("constraints", default["constraints"]),
            "load_characteristics": reqs.get("load_characteristics", default["load_characteristics"])
        }
