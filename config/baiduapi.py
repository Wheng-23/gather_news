# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
from config import peizhi

# # Set your own appid/appkey.
# appid = '20240716002100940'
# appkey = '3d1B0ljOKjyZJCsOI08_'
#
# # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
# from_lang = 'auto'
# to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translation_baidu(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(peizhi.baidu_appid + query + str(salt) + peizhi.baidu_appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': peizhi.baidu_appid, 'q': query, 'from': peizhi.from_lang, 'to': peizhi.to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # Show response
    # 解析 JSON 数据
    data = json.loads(json.dumps(result, indent=4, ensure_ascii=False))
    # 获取所需的字符串
    result_string = data["trans_result"][0]["dst"]
    print(result_string)
    return result_string


if __name__ == '__main__':
    translation_baidu('Message to the Congress on the Continuation of the National Emergency With Respect to Hong Kong')
