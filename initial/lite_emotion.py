# coding: utf-8
import _thread as thread

import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from config.mysqlop import Mysqlop


import websocket

total_emotion = []
received_messages = []
class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content,end='')
        received_messages.append(content)
        if status == 2:
            print("#### 关闭会话")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": query}]
            }
        }
    }
    return data


def main(appid, api_secret, api_key, Spark_url, domain, query):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def transform_string(input_string):
    if '消极' in input_string:
        return '消极'
    elif '积极' in input_string:
        return '积极'
    elif '中立' in input_string:
        return '中立'
    else:
        return input_string  # 如果都不包含，则返回原字符串

if __name__ == "__main__":
    a = Mysqlop()
    for i in range(a.get_row_count()):
        received_messages = []
        data_str = a.getData(i, 1, "summary")
        if data_str is None:
            data_str = ''
        main(
            appid="04cfabb6",
            api_secret="MjRiMzBiMDhhYTU0YzVhN2M1ZmJmOWQ5",
            api_key="3ed8a031885b6e8cc9425f1304696ee3",
            #appid、api_secret、api_key三个服务认证信息请前往开放平台控制台查看（https://console.xfyun.cn/services/bm35）
            # gpt_url="wss://spark-api.xf-yun.com/v3.5/chat",      # Max环境的地址
            # Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # Pro环境的地址
            Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat",  # Lite环境的地址
            # domain="generalv3.5",     # Max版本
            # domain = "generalv3"    # Pro版本
            domain = "general",      # Lite版本址
            # query=data_str+"请在1-10分之间给出一个打分，其中10分是最积极，0分是最消极,只要结果"
            query = "请评价冒号后的新闻对于中国的积极程度，从0-10打分，0是消极，1是积极，只回复一个分数值：" + data_str
        )
        emotion = ''.join(received_messages)
        # summary = summary.replace("'", "''")
        print(emotion)
        print(type(emotion))
        total_emotion.append(transform_string(emotion))
    for index, item in enumerate(total_emotion):
        print(index)
        print(type(index))
        print(item)
        print(type(item))
        a.updateEmotion('emotion', item, index + 1)


#Lite模型