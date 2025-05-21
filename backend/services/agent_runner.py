from langchain.agents import AgentExecutor
from ..agents.requirements_parser import RequirementsParser
from ..agents.cloud_retriever import CloudRetriever
from ..agents.architecture_generator import ArchitectureGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRunner:
    def __init__(self):
        self.requirements_parser = RequirementsParser()
        self.cloud_retriever = CloudRetriever()
        self.architecture_generator = ArchitectureGenerator()

    async def run(self, requirements: str, include_costs: bool = False) -> dict:
        try:
            # Validate input
            if not requirements or not isinstance(requirements, str):
                raise ValueError("Invalid requirements input")

            logger.info("Parsing requirements...")
            parsed_reqs = await self.requirements_parser.parse(requirements)
            
            logger.info("Retrieving cloud components...")
            cloud_components = await self.cloud_retriever.get_components(parsed_reqs)
            
            logger.info("Generating architecture diagram...")
            mermaid_diagram = await self.architecture_generator.generate(
                parsed_reqs,
                cloud_components
            )

            result = {
                "mermaid_code": mermaid_diagram,
                "requirements": parsed_reqs
            }
            
            if include_costs:
                logger.info("Estimating costs...")
                costs = await self.cloud_retriever.estimate_costs(cloud_components)
                result["estimated_costs"] = costs

            return result
            
        except Exception as e:
            logger.error(f"Error in agent runner: {str(e)}")
            raise RuntimeError(f"Failed to process request: {str(e)}")
