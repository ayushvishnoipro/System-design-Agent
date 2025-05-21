from typing import Dict
import json
import logging
import re
from ..services.openai_service import openai_service  # Import the singleton instance
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class CloudRetriever(BaseAgent):
    def __init__(self):
        super().__init__("costs")
        self.component_prompt = '''Based on these requirements: {requirements}

Generate a valid JSON response in this format:
{{
    "components": [
        {{
            "service": "service_name",
            "purpose": "description",
            "tier": "size/tier",
            "specs": {{
                "instance_type": "...",
                "storage": "...",
                "region": "..."
            }}
        }}
    ],
    "connections": [
        {{
            "from": "service1",
            "to": "service2",
            "type": "sync/async"
        }}
    ]
}}'''

        self.cost_prompt = """Generate a JSON cost estimate for these AWS services:
{components}

Respond with ONLY a valid JSON object in this exact format:
{{
    "service_name": {{
        "monthly": 100.00,
        "yearly": 1200.00,
        "specs": {{
            "instance_type": "t3.medium",
            "storage": "100GB",
            "region": "us-east-1"
        }},
        "tier": "standard"
    }}
}}"""

    async def get_components(self, requirements: Dict) -> Dict:
        try:
            reqs_str = json.dumps(requirements, indent=2)
            prompt = self.component_prompt.format(requirements=reqs_str)
            
            response = await openai_service.generate_completion(prompt, "architecture")
            return self._parse_components(response)
        except Exception as e:
            logger.error(f"Error getting components: {str(e)}", exc_info=True)
            return {"components": [], "connections": []}

    def _parse_components(self, response: str) -> Dict:
        try:
            return self._parse_json(response)  # Use base class method
        except Exception as e:
            logger.error(f"Error parsing components: {str(e)}", exc_info=True)
            return {"components": [], "connections": []}

    async def estimate_costs(self, architecture: Dict) -> Dict[str, Dict]:
        try:
            components_str = json.dumps(architecture.get("components", []), indent=2)
            prompt = self.cost_prompt.format(components=components_str)
            
            response = await openai_service.generate_completion(prompt, "costs")  # Added system_type
            return self._parse_costs(response)
        except Exception as e:
            logger.error(f"Error estimating costs: {str(e)}", exc_info=True)
            return self._get_default_costs(architecture)

    def _parse_costs(self, response: str) -> Dict:
        try:
            # First try to find a JSON object in the response
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            
            # If no JSON found, return empty dict
            return {}
        except Exception as e:
            logger.error(f"Cost parsing error: {str(e)}")
            return {}

    def _get_default_costs(self, architecture: Dict) -> Dict:
        costs = {}
        for component in architecture.get("components", []):
            service = component["service"]
            costs[service] = {
                "monthly": 50.0,  # Default estimate
                "yearly": 600.0,
                "specs": component.get("specs", {}),
                "tier": component.get("tier", "standard")
            }
        return costs
