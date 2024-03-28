import imaplib
import email
import yaml
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flipflop.utils import try_multi_decode

with open("./flipflop/config.yaml",'r', encoding="utf-8") as f:
    cfg = yaml.safe_load(f)['Email']
import email
import imaplib
 
# IMAP服务器信息
imap_host = 'imap.qq.com'
username = cfg['Acount']
password = cfg['Password']
 
# 连接到IMAP服务器
server = imaplib.IMAP4_SSL(imap_host)
server.login(username, password)
 
# 选择收件箱
server.select('INBOX')
 
# 搜索邮件（按需修改搜索条件）
status, messages = server.search(None, 'UNSEEN')    
 

# 获取邮件列表
if messages:
    email_ids = messages[0].split()
    print("邮件数量:", len(email_ids))
    #raise ValueError('EVA edge stop')
    for email_id in email_ids:
        # 获取邮件信息
        status, email_data = server.fetch(email_id, '(RFC822)')
        
        if status == 'OK' and email_data:
            # 解析邮件
            email_message = email.message_from_bytes(email_data[0][1])
            
            # 提取邮件的各个部分
            subject = email.header.decode_header(email_message['subject'])[0][0]
            from_ = email.header.decode_header(email_message['from'])[0][0]
            content_type = email_message.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = email_message.get_payload(decode=True)
                # 解码内容（如果需要）
                content = content.decode()
                
                # 打印邮件信息
                print(f"Subject: {try_multi_decode(subject)}, From: {try_multi_decode(from_)}")
            server.store(email_id, '+FLAGS', '\\Seen')

# 关闭连接
server.close()
server.logout()
