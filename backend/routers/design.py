from fastapi import APIRouter, HTTPException
from backend.models.request import DesignRequest
from backend.models.response import DesignResponse
from backend.services.agent_runner import AgentRunner
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
agent_runner = AgentRunner()

@router.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    try:
        if not request.requirements.strip():
            raise HTTPException(status_code=400, detail="Requirements cannot be empty")

        logger.info(f"Processing design request: {request.requirements[:100]}...")
        
        result = await agent_runner.run(
            requirements=request.requirements,
            include_costs=request.include_costs
        )
        
        # Ensure we have a valid Mermaid diagram
        if not result.get("mermaid_code"):
            raise HTTPException(status_code=500, detail="Failed to generate diagram")

        return DesignResponse(**result)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
