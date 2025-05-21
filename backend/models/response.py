from pydantic import BaseModel
from typing import Optional, Dict, Union

class ServiceCost(BaseModel):
    monthly: float
    yearly: float
    specs: Dict[str, str]
    tier: str

class DesignResponse(BaseModel):
    mermaid_code: str
    estimated_costs: Optional[Dict[str, ServiceCost]] = None
    error: Optional[str] = None
