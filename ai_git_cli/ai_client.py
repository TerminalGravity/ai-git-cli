import openai
import logging
import time
from typing import List, Dict

class AIClient:
    def __init__(self, api_key: str, model: str, max_retries: int = 3):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries

    def get_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            except openai.RateLimitError:
                wait_time = 2 ** retries
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            except openai.OpenAIError as e:
                logging.error(f"OpenAI API error: {e}")
                raise e
        raise Exception("Max retries exceeded for OpenAI API.")

    def set_model(self, model: str):
        self.model = model

def get_ai_client(config: Dict) -> AIClient:
    return AIClient(
        api_key=config['ai_provider']['api_key'],
        model=config['ai_provider']['model']
    )
