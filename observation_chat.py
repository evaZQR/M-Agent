import os
from dotenv import load_dotenv
import yaml
import json
import time
from flipflop.utils import *
from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
load_dotenv()
with open("./prompt.yaml","r",encoding="utf-8") as file:
    prompt_data = yaml.safe_load(file)

SELFWOM,OBSERVATION,HISTORY,MEMORY,FIND  =   prompt_data["obserchatprompt"]["selfwom"],\
                                prompt_data["obserchatprompt"]["observation"],\
                                prompt_data["obserchatprompt"]["history"],\
                                prompt_data["obserchatprompt"]["memory"],\
                                prompt_data['obserchatprompt']['findmemory']
#print(SELFWOM,OBSERVATION,HISTORY)
LANGUAGE = os.getenv("LANGUAGE")

import json

def store_the_history(history, llm, **kwargs):
    
    memory_o = ""
    for key, value in kwargs.items():
        content = f"{key}: {value}"
        memory_o += content + "\n"
        print(content)
    memory_o += "The following is the conversation history:\n" + history
    memory_o += f"\nThis is the basic memory of a conversation, please summarize the content in {LANGUAGE} taking changshengEVA's perspective, only talk about the key information, such as time...\n"
    print("Start to memory...")
    mem = str(llm.chat([ChatMessage(content=memory_o)])).split('assistant:')[-1]
    #print(mem)
    #raise ValueError('Stop')
    print("The history is storing, find the following args:")
    data_to_store = {
        'history': history,
        'kwargs': kwargs,
        'memory': mem
    }
    filename = "./data/memory/dialog_history.json"
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                raise ValueError("Existing data is not a list")
    except (FileNotFoundError, ValueError):
        existing_data = []
    
    existing_data.append(data_to_store)
    
    json_data = json.dumps(existing_data, ensure_ascii=False, indent=4)
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_data)
    
    print("OK!! Data saved to", filename)



def emerge_chat_prompt_wo_memory(history,observation = None): 
    if observation: return f"{SELFWOM.format(LANGUAGE)}{OBSERVATION.format(observation)}{HISTORY.format(history)}"
    else : return f"{SELFWOM.format(LANGUAGE)}{HISTORY.format(history)}"

from llama_index.core import StorageContext, load_index_from_storage
def find_memory(index, find):
    query_engine = index.as_query_engine()
    response = query_engine.query(FIND.format(find))
    return response
    
def emerge_chat_prompt_w_memory(history,memory,observation = None): 
    if observation: return f"{SELFWOM.format(LANGUAGE)}{MEMORY.format(memory)}{OBSERVATION.format(observation)}{HISTORY.format(history)}"
    else : return f"{SELFWOM.format(LANGUAGE)}{MEMORY.format(memory)}{HISTORY.format(history)}"

def start_chat(llm, embed, memory = False, store = False, observation = None):
    """
    start to chat with the observation
    observation: the observation that input for changshengEVA who wants to talk about it.
    """
    if memory is False:
        final_prompt = emerge_chat_prompt_wo_memory("",observation)
    else:
        Settings.llm = llm
        Settings.embed_model = embed
        storage_context = StorageContext.from_defaults(persist_dir="./data/memory/index")
        index = load_index_from_storage(storage_context)
        final_prompt = emerge_chat_prompt_w_memory("",find_memory(index, observation),observation)
    print(final_prompt)
    #raise ValueError("EVA error...")
    print("changshengEVA:")
    response = str(llm.chat([ChatMessage(content = final_prompt)])).split('assistant:')[-1]
    print(response)
    displayed = "changshengEVA:" + response + "\n"
    history = ""
    history += displayed
    while 1:
        print("ZQR:")
        message = input()
        if message.lower() == "exit": break
        history += "ZQR:" + message + "\n"
        if memory:
            final_prompt = emerge_chat_prompt_w_memory(history,find_memory(index, message),observation)
        else:
            final_prompt = emerge_chat_prompt_wo_memory(history,observation)
        print("changshengEVA:")
        response = str(llm.chat([ChatMessage(content = final_prompt)])).split('assistant:')[-1]
        print(response)
        displayed = "changshengEVA:" + response + "\n"
        history += displayed
    print("OK")
    print("The following is you talked with the changshengEVA:")
    print(history)
    if store: 
        store_the_history(history, llm, observation=observation, time=get_current_time())




if __name__ == "__main__":
    start_chat("接收到来自好友江海共余生的QQ信息:签到了吗？")