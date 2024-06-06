import os
from dotenv import load_dotenv
from opanai_call import stream_chat
import yaml
import json
import time
from flipflop.utils import *
load_dotenv()
with open("./prompt.yaml","r",encoding="utf-8") as file:
    prompt_data = yaml.safe_load(file)

SELFWOM,OBSERVATION,HISTORY  =   prompt_data["obserchatprompt"]["selfwom"],\
                                prompt_data["obserchatprompt"]["observation"],\
                                prompt_data["obserchatprompt"]["history"],
#print(SELFWOM,OBSERVATION,HISTORY)
LANGUAGE = os.getenv("LANGUAGE")

import json

def store_the_history(history, **kwargs):
    data_to_store = {
        'history': history,
        'kwargs': kwargs
    }
    print("The history is storing, find the following args:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    
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



def emerge_chat_prompt_wo_memory(observation,history): 
    return f"{SELFWOM.format(LANGUAGE)}{OBSERVATION.format(observation)}{HISTORY.format(history)}"

def start_chat_wo_memory(observation, model = "gpt-3.5-turbo"):
    """
    start to chat with the observation
    observation: the observation that input for changshengEVA who wants to talk about it.
    """
    final_prompt = emerge_chat_prompt_wo_memory(observation,"")
    #print(final_prompt)
    #raise ValueError("EVA error...")
    print("changshengEVA:")
    response = stream_chat(final_prompt,model,chat=True)
    print("")
    displayed = "changshengEVA:" + response + "\n"
    history = ""
    history += displayed
    while 1:
        print("ZQR:")
        message = input()
        if message.lower() == "exit": break
        history += "ZQR:" + message + "\n"
        final_prompt = emerge_chat_prompt_wo_memory(observation,history)
        print("changshengEVA:")
        response = stream_chat(final_prompt,model,chat=True)
        print("")
        displayed = "changshengEVA:" + response + "\n"
        history += displayed
    print("OK")
    print("The following is you talked with the changshengEVA:")
    print(history)
    store_the_history(history, observation=observation, time=get_current_time())
    
if __name__ == "__main__":
    start_chat_wo_memory("接收到来自好友江海共余生的QQ信息:签到了吗？")