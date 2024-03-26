import os
from streamcall import stream_chat
import yaml
with open("/Users/eva/Desktop/M-Agent/prompt.yaml","r",encoding="utf-8") as file:
    prompt_data = yaml.safe_load(file)

SELFWOM,OBSERVATION,HISTORY =   prompt_data["obserchatprompt"]["selfwom"],\
                                prompt_data["obserchatprompt"]["observation"],\
                                prompt_data["obserchatprompt"]["history"],
print(SELFWOM,OBSERVATION,HISTORY)

def emerge_chat_prompt_wo_memory(language,observation,history):
    return f"{SELFWOM.format(language)}{OBSERVATION.format(observation)}{HISTORY.format(history)}"

final_prompt = emerge_chat_prompt_wo_memory("chinese","接收到来自好友江海共余生的QQ信息:签到了吗？","")
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
    history += "ZQR:" + message + "\n"
    final_prompt = emerge_chat_prompt_wo_memory("chinese","接收到来自好友江海共余生的QQ信息:签到了吗？",history)
    print("changshengEVA:")
    response = stream_chat(final_prompt)
    print("")
    displayed = "changshengEVA:" + response + "\n"
    history += displayed
