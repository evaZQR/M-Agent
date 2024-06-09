import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.llms import ChatMessage
from multiff import start_server
import argparse
parser = argparse.ArgumentParser(description='处理方法选择。')
parser.add_argument('--method', type=str, choices=['local', 'azure', 'openai'], required=True, help='选择处理方法,参照README。')
parser.add_argument('--memory', type=bool, default = False, help='是否使用记忆')
parser.add_argument('--store', type=bool, default = False, help='是否使用保存记忆')
args = parser.parse_args()
if args.method == 'local':
    """
    this needs you put the llm model and embed model in the same folder as this file -> checkpoint and change the local.py.
    """
    from load_model.local import get_llm,get_embed_model
    args.llm = get_llm()
    args.embed_model = get_embed_model()
elif args.method == 'azure':
    from load_model.azure import get_llm,get_embed_model
    args.llm = get_llm(model_temperature = 0)
    args.embed_model = get_embed_model()
elif args.method == 'openai':
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
    BASE_URL = os.getenv("BASE_URL")
    args.llm = OpenAI(api_key = API_SECRET_KEY, api_base = BASE_URL, temperature=0.1, model="gpt-3.5-turbo")
    args.embed_model = OpenAIEmbedding(api_key = API_SECRET_KEY, api_base = BASE_URL, model="text-embedding-3-small")

def test():
    response = args.llm.chat(messages = [ChatMessage(content = "你好")])
    print(response)


def main():
    #test()
    start_server(args)

if __name__ == '__main__':
    main()


