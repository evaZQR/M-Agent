import imaplib
import email
import yaml
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flipflop.utils import try_multi_decode
from streamcall import stream_chat

with open("./flipflop/config.yaml",'r', encoding="utf-8") as f:
    cfg = yaml.safe_load(f)['Email']
import email
import imaplib
 
# IMAP服务器信息
imap_host = 'imap.qq.com'
username = cfg['Acount']
password = cfg['Password']
 
def read_unseen_emails(delete = False):

    email_get = ''
    # 连接到IMAP服务器
    server = imaplib.IMAP4_SSL(imap_host)
    server.login(username, password)
    
    # 选择收件箱
    server.select('INBOX')
    
    # 搜索邮件（按需修改搜索条件）
    status, messages = server.search(None, 'UNSEEN')    
    
    def conclude(email_message):
        prompt = cfg['conclude_prompt'].format(str(email_message))
        response = stream_chat(prompt)
        return response
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
                print("\n---------------------------")
                print(f"Subject: {try_multi_decode(subject)}, From: {try_multi_decode(from_)}",subject)
                email_get += "\n---------------------------\n"
                email_get += f"Subject: {try_multi_decode(subject)}, From: {try_multi_decode(from_)}"
                print(content_type)
                # 检查是否为 multipart/alternative 类型
                if content_type == 'multipart/alternative':
                    # 遍历邮件的所有部分
                    for part in email_message.walk():
                        sub_content_type = part.get_content_type()
                        if sub_content_type == 'text/plain':
                            # 纯文本内容
                            plain_text = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                            #print("纯文本内容：", plain_text)
                            conclude_plain_text = conclude(plain_text)
                            print("concluded:",conclude_plain_text)
                            email_get += "\n纯文本内容：" + conclude_plain_text
                        elif sub_content_type == 'text/html':
                            # HTML 内容
                            html_text = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                        #print("HTML 内容：", html_text)
                elif content_type == 'text/plain' or content_type == 'text/html':
                    content = email_message.get_payload(decode=True)
                    # 解码内容（如果需要）
                    content = content.decode()
                    #print("纯文本内容：",content)
                    conclude_content = conclude(content)
                    print("conclude:", conclude_content)
                    email_get += "\n纯文本内容：" + conclude_content
                if delete: server.store(email_id, '+FLAGS', '\\Seen')

    # 关闭连接
    server.close()
    server.logout()
    return email_get
if __name__ == '__main__':
    read_unseen_emails()