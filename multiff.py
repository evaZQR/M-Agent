from observation_chat import *
import time
from datetime import datetime
print("启动前置工具...")
from flipflop.utils import *
from flipflop.ReceiveEmail import read_unseen_emails
import asyncio
def read_mem():
    import json
    # 初始化一个空列表来存储memory值
    memory_list = []

    # 打开并读取JSON文件
    with open('./data/memory/dialog_history.json', 'r', encoding='utf-8') as file:
        # 加载JSON内容
        data = json.load(file)
        
        # 遍历数据列表
        for item in data:
            # 提取每个字典中的'memory'值
            memory_value = item.get('memory', None)
            
            # 如果'memory'值存在，则添加到列表中
            if memory_value:
                memory_list.append(memory_value)

    return memory_list
def check_email_and_start_chat(args):
    print(args)
    T = 0
    try:
        while True:
            T_c = time.time()
            if T_c - T >= 1000:
                observation = read_unseen_emails(use_llm=args.llm, delete=True)
                if observation:
                    start_chat(args.llm, args.embed_model, args.memory, args.store, observation)
                else:
                    print("未检测到邮件...")
                T = T_c  # 更新时间戳
            time.sleep(100)
    except KeyboardInterrupt:
        if args.store is False:
            print("服务器已停止...")
        else:
            print("服务器已停止,正在记录index中...")
            from llama_index.core import Document,Settings
            Settings.embed_model = args.embed_model
            Settings.llm = args.llm
            documents = [Document(text=intro) for intro in read_mem()]
            from llama_index.core import VectorStoreIndex
            index = VectorStoreIndex.from_documents(documents,)
            #print(index)
            index.storage_context.persist(persist_dir="./data/memory/index")
            print('index已保存...')
            

def start_server(args):
    T = time.time()
    print("[{}]".format(get_current_time()), "启动服务器...")
    print("邮件监视器启动...")
    check_email_and_start_chat(args)
        
if __name__ == "__main__":
    start_server()