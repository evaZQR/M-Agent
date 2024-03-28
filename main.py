import os
from dotenv import load_dotenv
from streamcall import stream_chat
import yaml
import json
import time
from flipflop.utils import *
load_dotenv()
with open("/Users/eva/Desktop/M-Agent/prompt.yaml","r",encoding="utf-8") as file:
    prompt_data = yaml.safe_load(file)

SELFWOM,OBSERVATION,HISTORY  =   prompt_data["obserchatprompt"]["selfwom"],\
                                prompt_data["obserchatprompt"]["observation"],\
                                prompt_data["obserchatprompt"]["history"],
#print(SELFWOM,OBSERVATION,HISTORY)
LANGUAGE = os.getenv("LANGUAGE")

import json

def store_the_history(history, **kwargs):
    # 创建一个包含所有信息的字典
    data_to_store = {
        'history': history,
        'kwargs': kwargs
    }
    
    # 打印所有关键字参数
    print("The history is storing, find the following args:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    
    # 指定要写入的文件名
    filename = "dialog_history.json"
    
    # 读取现有文件内容，如果文件不存在，则创建一个新的空数组
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 读取JSON数据
            existing_data = json.load(file)
            # 确保existing_data是一个列表
            if not isinstance(existing_data, list):
                raise ValueError("Existing data is not a list")
    except (FileNotFoundError, ValueError):
        # 文件不存在或数据格式不正确，创建一个新的列表
        existing_data = []
    
    # 将新数据添加到列表中
    existing_data.append(data_to_store)
    
    # 将整个列表转换为JSON格式字符串
    json_data = json.dumps(existing_data, ensure_ascii=False, indent=4)
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_data)
    
    print("OK!! Data saved to", filename)



def emerge_chat_prompt_wo_memory(observation,history): 
    return f"{SELFWOM.format(LANGUAGE)}{OBSERVATION.format(observation)}{HISTORY.format(history)}"

def chat_wo_memory(observation):
    """
    start to chat with the observation
    observation: the observation that input for changshengEVA who wants to talk about it.
    """
    final_prompt = emerge_chat_prompt_wo_memory(observation,"")
    #print(final_prompt,end="")
    print("changshengEVA:")
    response = stream_chat(final_prompt)
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
        response = stream_chat(final_prompt)
        print("")
        displayed = "changshengEVA:" + response + "\n"
        history += displayed
    print("OK")
    print("The following is you talked with the changshengEVA:")
    print(history)
    store_the_history(history, observation=observation, time=get_current_time())
    

if __name__ == "__main__":
    chat_wo_memory("接收到来自好友江海共余生的QQ信息:签到了吗？")