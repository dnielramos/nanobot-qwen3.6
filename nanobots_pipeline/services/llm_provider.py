import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    """Exception raised for HTTP 429 Rate Limit errors."""
    pass

class LLMProvider:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "NanoBots Pipeline",
            "Content-Type": "application/json"
        }

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((httpx.RequestError, RateLimitError)),
        reraise=True
    )
    async def generate_response(self, messages: list[dict], tools: list[dict] = None) -> dict:
        """
        Sends a request to OpenRouter API to generate a response.
        Handles rate limits (429) with exponential backoff.
        """
        payload = {
            "model": settings.MODEL_ID,
            "messages": messages,
        }

        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                )

                if response.status_code == 429:
                    logger.warning("Rate limit hit (429). Retrying...")
                    raise RateLimitError("OpenRouter API rate limit exceeded.")

                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error: {e.response.text}")
                raise
