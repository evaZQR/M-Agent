
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import json
import importlib
importlib.reload(sys)

import time


YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '5841964cca4206da'
APP_SECRET = 'ouxNuJbiKmv7IYfxNHDgcCZF1xxZCm29'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(text):
    q = text

    data = {}
    data['from'] = 'auto'
    data['to'] = '	zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        res = response.content.decode('utf-8')
        data_json = json.loads(res)
        translation = data_json["translation"][0]
        return translation


if __name__ == '__main__':
    connect('carnivore')