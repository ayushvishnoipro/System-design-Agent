from pydantic import BaseModel

class DesignRequest(BaseModel):
    requirements: str
    include_costs: bool = False
    output_format: str = "mermaid"
