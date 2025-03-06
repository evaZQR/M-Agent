from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
import base64
import csv

# OAuth2.0 Gmail　API用スコープ
# 変更する場合は、token.jsonファイルを削除する
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# アクセストークン取得
def get_token():
    creds = None
    # token.json
    # access/refresh tokenを保存
    # 認可フロー完了時に自動で作成。
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file(
            'creds/token.json', SCOPES)
    # トークンが存在しない場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # トークンを保存
        with open('creds/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# メールリスト取得
def get_message_list(service, user_id, query, count):
    messages = []
    try:
        message_ids = (
            service.users()
            .messages()
            .list(userId=user_id, maxResults=count, q=query)
            .execute()
        )

        if message_ids["resultSizeEstimate"] == 0:
            print("No DATA")
            return []

        # 各message内容確認
        for message_id in message_ids["messages"]:
            # 各メッセージ詳細
            detail = (
                service.users()
                .messages()
                .get(userId="me", id=message_id["id"])
                .execute()
            )
            message = {}
            message["id"] = message_id["id"]
            # 本文
            if 'data' in detail['payload']['body']:
                decoded_bytes = base64.urlsafe_b64decode(
                    detail["payload"]["body"]["data"])
                decoded_message = decoded_bytes.decode("UTF-8")
                message["body"] = decoded_message
            else:
                message["body"] = ""
            # 件名
            message["subject"] = [
                header["value"]
                for header in detail["payload"]["headers"]
                if header["name"] == "Subject"
            ][0]
            # 送信元
            message["from"] = [
                header["value"]
                for header in detail["payload"]["headers"]
                if header["name"] == "From"
            ][0]
            messages.append(message)
        return messages

    except errors.HttpError as error:
        print("An error occurred: %s" % error)


# メイン部
# ※クエリや取得数は標準入力などで受け取った値を利用できるとよいが今回は非対応
def main(query="is:unread", count=10):
    # 1. アクセストークン取得
    creds = get_token()

    # 2. Gmail API (メッセージ一覧取得) 呼び出し
    service = build('gmail', 'v1', credentials=creds)
    messages = get_message_list(service, "me", query,
                                count=count)
    if messages:
        field_names = ['id', 'body', 'subject', 'from']
        with open('mails/gmails.csv', 'w', newline='', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(messages)
        
    else:
        return None


if __name__ == '__main__':
    main()

