from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    MODEL_ID: str = "qwen/qwen3.6-plus-preview:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
