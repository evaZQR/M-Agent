# -*- coding: utf-8 -*-
import http.client, urllib, json
conn = http.client.HTTPSConnection('apis.tianapi.com')  #接口域名
def translate(word):
    params = urllib.parse.urlencode({'key':'de5520ee196d7683f9e5da093b12e17a','word':word})
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    conn.request('POST','/enwords/index',params,headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)
    return dict_data['result']['content']

if __name__ == '__main__':
    print(translate('worm'))