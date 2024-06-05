import os
import openai
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
BASE_URL = os.getenv("BASE_URL")
llm = OpenAI(api_key = API_SECRET_KEY, api_base = BASE_URL, temperature=0.1, model="gpt-3.5-turbo")
response = llm.chat(messages = [ChatMessage(content = "你好")])
print(response)