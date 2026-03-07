from openai import OpenAI
from tenacity import retry, stop_after_attempt

import logging
logger = logging.getLogger(__name__)


REQUEST_TIMEOUT_SECS = 60


def create_chat_completion(client, model, **kwargs):
    """Create a chat completion, stripping parameters not supported by GPT-5."""
    unsupported = {"temperature", "top_p", "presence_penalty", "frequency_penalty"}
    if model.startswith("gpt-5"):
        for key in unsupported:
            kwargs.pop(key, None)
    return client.chat.completions.create(model=model, **kwargs)


class MyBotWrapper:
    def __init__(self, parser, model='gpt-4o-mini', temperature=0.5) -> None:
        self.parser = parser
        self.model = model
        self.temperature = temperature
        self.client = OpenAI()
    
    @retry(stop=stop_after_attempt(3))
    def run(self, inputs):
        prompt = self.parser.compose_prompt(inputs=inputs)
        logger.debug(f"PROMPT: {prompt}")
        response = self.get_completion(prompt=prompt)
        logger.debug(f"RAW RESPONSE: {response}")
        res = self.parser.parse_response(prompt=prompt, response=response)
        logger.debug(f"PARSED RESPONSE: {res}")
        return res

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        response = create_chat_completion(
            self.client,
            self.model,
            messages=messages,
            temperature=self.temperature,
            timeout=REQUEST_TIMEOUT_SECS,
            response_format={"type": self.parser.response_format},
        )
        return response.choices[0].message.content

    @property
    def task_name(self):
        return self.parser.task_name if self.parser else ""
