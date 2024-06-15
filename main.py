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
    args.llm = get_llm("./checkpoint/chatglm3-6b")
    args.embed_model = get_embed_model("./checkpoint/bge-large-en-v1.5")
elif args.method == 'azure':
    from load_model.azure import get_llm,get_embed_model
    args.llm = get_llm(model_temperature = 0)
    args.embed_model = get_embed_model()
elif args.method == 'openai':
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from load_model.local import get_embed_model
    API_SECRET_KEY = os.getenv("API_SECRET_KEY").encode().decode('utf-8')
    BASE_URL = os.getenv("BASE_URL")
    args.llm = OpenAI(api_key = API_SECRET_KEY, api_base = BASE_URL, temperature=0.1, model="gpt-3.5-turbo")
    #args.embed_model = OpenAIEmbedding(api_key = API_SECRET_KEY, api_base = BASE_URL, model="text-embedding-3-small")
    # if the api embed is not working, use the local embed model.
    args.embed_model = get_embed_model("./checkpoint/bge-large-en-v1.5")

from llama_index.core import VectorStoreIndex
from llama_index.core import Document
import json
def pre_load():
    from llama_index.core import Settings
    Settings.llm = args.llm
    Settings.embed_model = args.embed_model
    with open('./data/memory/dialog_history.json','r',encoding = 'utf-8') as f:
        dialog_history = json.load(f)
    documents = [Document(text = t['history'].replace('\n', '')) for t in dialog_history]
    index = VectorStoreIndex.from_documents(documents,)
    index.storage_context.persist(persist_dir="./data/memory/index")
def main():
    #pre_load()
    start_server(args)
    pass

if __name__ == '__main__':
    main()


