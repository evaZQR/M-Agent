import os
import openai
import requests
import time
import json
import time
from dotenv import load_dotenv
load_dotenv()


API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
BASE_URL = os.getenv("BASE_URL")
print(API_SECRET_KEY,BASE_URL)
def stream_chat(prompt: str,model = "gpt-3.5-turbo",chat = False):
    openai.api_key = API_SECRET_KEY
    openai.api_base = BASE_URL
    ans = ""
    for chunk in openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            if chat: print(content,end='')
            ans += content
    return ans

if __name__ == '__main__':
    stream_chat("你是谁？",chat = True)