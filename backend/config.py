from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AWS_ACCESS_KEY: str  # Changed from AWS_ACCESS_KEY_ID
    AWS_SECRET_KEY: str  # Changed from AWS_SECRET_ACCESS_KEY
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"

settings = Settings()
