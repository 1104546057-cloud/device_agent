import os

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            raise ValueError("API key not found. Please set the DEEPSEEK_API_KEY environment variable.")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        self.model = "deepseek-flash"

    def chat(self,messages):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            stream = False,
            extra_body = {
                "thinking":{
                    "type":"disabled"
                }
            }
        )
        return response.choices[0].message.content

    def chat_stream(self,messages):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            stream = True,
            extra_body = {
                "thinking":{
                    "type":"disabled"
                }
            }
        )

        for chunk in response:
            content = chunk.choices[0].delta.content

            if content:
                yield content

    def chat_json(self,messages):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            stream = False,
            response_format = {
                "type":"json_object"
            },
            extra_body = {
                "thinking":{
                    "type":"disabled"
                }
            }        
        )
        return response.choices[0].message.content
