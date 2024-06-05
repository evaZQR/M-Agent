import os
from openai import OpenAI
import time
from dotenv import load_dotenv
load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
BASE_URL = os.getenv("BASE_URL")
client = OpenAI(api_key = API_SECRET_KEY, base_url = BASE_URL)

print(API_SECRET_KEY,BASE_URL)
def stream_chat(prompt: str,model = "gpt-3.5-turbo",chat = False):
    ans = ''
    for chunk in client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,
            temperature=0,
            stream=True
        ):
        content = chunk.choices[0].text
        if chat: print(content,end='')
        ans += content
    return ans

if __name__ == '__main__':
    stream_chat("你是谁？,我是",chat = True)