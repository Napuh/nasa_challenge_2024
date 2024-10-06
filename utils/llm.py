from os import getenv
from typing import List

from openai import OpenAI


class simpleLLM:
    def __init__(self, model="openai/gpt-4o-2024-08-06") -> None:
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=getenv("OPENROUTER_API_KEY"),
        )

        self.model = model

    def generate_completion(
        self,
        system_message,
        messages: List[dict],
        streaming=False,
    ):
        system_message = [{"role": "system", "content": system_message}]

        messages_to_send = system_message + messages

        if streaming:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages_to_send,
                stream=True,
                temperature=0.1,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        else:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages_to_send,
                temperature=0.1,
            )

            return completion.choices[0].message.content
