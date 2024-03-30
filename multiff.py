from chat import *
import time
from datetime import datetime
print("启动前置工具...")
from flipflop.utils import *


def start_server():
    T = time.time()
    print("[{}]".format(get_current_time()), "启动服务器...")
    print("邮件监视器启动...")
    from flipflop.ReceiveEmail import read_unseen_emails

    while True:
        T_c = time.time()
        if int(T_c - T)%10 == 0:
            observation = read_unseen_emails()
            if observation != "" :start_chat_wo_memory(observation, "gpt-4")

        
if __name__ == "__main__":
    start_server()