from enum import Enum

class OutputFormat(Enum):
    MERMAID = "mermaid"
    JSON = "json"

class ServiceTier(Enum):
    STANDARD = "standard"
    PREMIUM = "premium"

# OpenAI Configuration
OPENAI_MODEL = "gpt-4"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 2000

# Default Values
DEFAULT_REGION = "us-east-1"
DEFAULT_MONTHLY_COST = 50.0

# System Messages
SYSTEM_MESSAGES = {
    "requirements": "You are a system requirements analyst. Extract key requirements and constraints.",
    "architecture": "You are a system architect. Design scalable cloud architectures.",
    "costs": "You are a cloud pricing specialist. Provide realistic cost estimates."
}
