import os
import openai
import requests
import time
import json
import time

API_SECRET_KEY = "sk-zk2f1bf5d82ad12aa356ed0aca32e1b31de66017ff6a710b";  # 你在智增增的key
BASE_URL = "https://flag.smarttrot.com/v1"

def stream_chat(prompt: str):
    openai.api_key = API_SECRET_KEY
    openai.api_base = BASE_URL
    ans = ""
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            print(content,end='')
            ans += content
    return ans

if __name__ == '__main__':
    stream_chat("你是谁？")