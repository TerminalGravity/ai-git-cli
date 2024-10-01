```python
import openai
import logging
import time
from typing import List, Dict
from abc import ABC, abstractmethod

class BaseAIClient(ABC):
    @abstractmethod
    def get_response(self, messages: List[Dict[str, str]], temperature: float) -> str:
        pass

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key: str, model: str, max_retries: int = 3):
        openai.api_key = api_key
        self.model = model
        self.max_retries = max_retries

    def get_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        retries = 0
        while retries < self.max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            except openai.error.RateLimitError:
                wait_time = 2 ** retries
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            except openai.error.OpenAIError as e:
                logging.error(f"OpenAI API error: {e}")
                raise e
        raise Exception("Max retries exceeded for OpenAI API.")

def get_ai_client(config: Dict) -> BaseAIClient:
    provider = config['ai_provider']['name'].lower()
    if provider == 'openai':
        return OpenAIClient(
            api_key=config['ai_provider']['api_key'],
            model=config['ai_provider']['model']
        )
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")
```
