# llm/client.py
"""LLM client using Google's Gemini generate-content API."""

import time
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY
from utils import get_logger

logger = get_logger(__name__)


class LLMClient:
    """Gemini API client with retry handling."""

    def __init__(self, model_name: str = DEFAULT_MODEL, max_retries: int = MAX_RETRIES, retry_delay: int = RETRY_DELAY):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set. Add it to the project .env file.")
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def call(self, prompt: str, **kwargs) -> str:
        """Send a prompt to the LLM and return the generated text.

        Parameters
        ----------
        prompt: str
            The user message to send.
        kwargs: dict
            Optional parameters like ``max_tokens``.
        """
        config = types.GenerateContentConfig(
            max_output_tokens=kwargs.get("max_tokens", 2048),
            temperature=kwargs.get("temperature", 0.2),
            top_p=kwargs.get("top_p", 0.7),
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "label": {
                        "type": "STRING",
                        "enum": ["Scam", "Not Scam", "Uncertain"],
                    },
                    "reasoning": {"type": "STRING"},
                    "intent": {"type": "STRING"},
                    "risk_factors": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                    },
                },
                "required": ["label", "reasoning", "intent", "risk_factors"],
            },
        )
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )
                if response.text:
                    return response.text.strip()
                raise ValueError("Gemini returned no text content")
            except Exception as e:
                logger.error(f"LLM call attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries:
                    raise
                time.sleep(self.retry_delay * (2 ** attempt))

    def call_batch(self, prompts: list, **kwargs) -> list:
        """Process a list of prompts sequentially (simple batch)."""
        results = []
        for p in prompts:
            results.append(self.call(p, **kwargs))
        return results