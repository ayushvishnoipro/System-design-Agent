from openai import AsyncOpenAI
import httpx
from ..config import settings
from ..constants import OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS, SYSTEM_MESSAGES
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            http_client=httpx.AsyncClient()
        )

    async def generate_completion(
        self, 
        prompt: str, 
        system_type: str,
        model: str = OPENAI_MODEL,
        temperature: float = OPENAI_TEMPERATURE,
        max_tokens: int = OPENAI_MAX_TOKENS
    ) -> str:
        """
        Generate completion using OpenAI API
        
        Args:
            prompt: The user prompt
            system_type: Type of system message to use
            model: OpenAI model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGES[system_type]},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise RuntimeError(f"Failed to generate completion: {str(e)}")

# Create a singleton instance
openai_service = OpenAIService()

# Add this function for backwards compatibility
async def generate_completion(prompt: str, system_type: str = "requirements") -> str:
    return await openai_service.generate_completion(prompt, system_type)

# Export both the class and the convenience function
__all__ = ['OpenAIService', 'openai_service', 'generate_completion']
