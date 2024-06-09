from chat import *
import time
from datetime import datetime
print("启动前置工具...")
from flipflop.utils import *
from flipflop.ReceiveEmail import read_unseen_emails
import asyncio

def check_email_and_start_chat(args):
    T = 0
    while True:
        T_c = time.time()
        if T_c - T >= 1000:
            observation = read_unseen_emails(use_llm=args.llm, delete=False)
            if observation:
                start_chat(observation, args.llm, args.embed_model, args.memory)
            else:
                print("未检测到邮件...")
            T = T_c  # 更新时间戳
        time.sleep(100)

def start_server(args):
    T = time.time()
    print("[{}]".format(get_current_time()), "启动服务器...")
    print("邮件监视器启动...")
    check_email_and_start_chat(args)
        
if __name__ == "__main__":
    start_server()