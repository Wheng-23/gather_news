import json

import requests

from apidemo.utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '7a12a0b382b55712'
# 您的应用密钥
APP_SECRET = 'tE4ivAWPAZDWS7vKDKAj1AG9QwM5v8Cl'


def createRequest(q):
    '''
    note: 将下列变量替换为需要请求的参数
    '''

    lang_from = 'auto'
    lang_to = 'zh-CHS'
    vocab_id = '您的用户词表ID'

    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    print(str(res.content, 'utf-8'))
    # 解析 JSON 字符串
    data = json.loads(str(res.content, 'utf-8'))

    # 获取 "translation" 字段的值
    translation = data.get("translation")

    print(translation)
    print(translation[0])
    return translation[0]



def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    q = 'First Lady Jill Biden'
    result = createRequest(q)
    print(result)
