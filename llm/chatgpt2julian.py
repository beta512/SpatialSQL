import json.decoder
import time
import requests
import json


def ask_llm(model: str, message: str, temperature: float, n: int):
    sql = ''
    n_repeat = 0
    while n_repeat < n:
        try:
            url = 'https://chat.julianwl.com/api/chatgpt/chat-process'
            requests.packages.urllib3.disable_warnings()
            headers = {
                'Host': 'chat.julianwl.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Content-Type': 'application/json',
                'X-Website-Domain': 'https://chat.julianwl.com',
                # 'Fingerprint': 1274379873
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IueUqOaItzhkNTQyOTNjNCIsImlkIjo0NTY4NCwiZW1haWwiOiJ6aGFuZ2p5ODZAaWhlcC5hYy5jbiIsInJvbGUiOiJ2aWV3ZXIiLCJvcGVuSWQiOiJvOUJOUzZiUVJSZFo3bktXam9TcnMtRk9OOXhnIiwiY2xpZW50IjpudWxsLCJpYXQiOjE3MjgzNTM1MjAsImV4cCI6MTcyODk1ODMyMH0.jnJ4nwRRIquJSiKhj0E6OxruuvdnyTOrPTMgdtftOf4',
                'Origin': 'https://chat.julianwl.com',
                'Connection': 'keep-alive',
                'Referer': 'https://chat.julianwl.com/chat',
                'Cookie': 'Hm_lvt_35ba5ea97a17eeae7cba298cd0bda898=1728353507,1728372195; Hm_lpvt_35ba5ea97a17eeae7cba298cd0bda898=1728372195; HMACCOUNT=107DC5BA5401FEDD',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
                }
            # message = 'what is your version?'
            # message = '你的版本是多少？'
            data = {"model":"gpt-4o-2024-08-06",
                    "modelName":"Julian-4o",
                    "modelType":1,
                    "prompt": message}
            #
            #response = requests.request('POST', url, headers = headers, data = data,verify = False)
            response = requests.request('POST', url, headers = headers, data = json.dumps(data),verify = False)
            text = response.text
            #
            # index1 = text.rfind('","text":"')
            # if index1 > 0:
            #     index2 = text.rfind('","detail"', index1)
            #     if index2 > 0:
            #         sql = text[index1 + 10:index2]
            index1 = text.rfind('"answer":"')
            if index1 > 0:
                index2 = text.rfind('","errMsg"', index1)
                if index2 > 0:
                    sql = text[index1 + 10:index2]
            #
            break
        except Exception as e:
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for exception: {e}")
            time.sleep(5)
    #
    time.sleep(2)
    return sql

