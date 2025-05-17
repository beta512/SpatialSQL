import json.decoder
import time
import requests
import json
import re

def ask_llm(model: str, message: str, temperature: float, n: int):
    sql = ''
    n_repeat = 0
    while n_repeat < n:
        try:
            url = 'https://chat.ihep.ac.cn/backend/api/chat/completions'
            requests.packages.urllib3.disable_warnings()
            headers = {
                'Host': 'chat.ihep.ac.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Referer': 'https://chat.ihep.ac.cn/v3/',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3Zjc3ZTYyLTU5ODItNGY1NS04MDdhLWI5ODkzZDI1MTljZCJ9.f6fQnFViby-JByNukKK8jfwutZHSRkfQYm6vj1KzY2Y',
                'Content-Type': 'application/json',
                'Origin': 'https://chat.ihep.ac.cn',
                'Connection': 'keep-alive',
                'Cookie': 'oui-session=eyJfc3RhdGVfaWhlcF9KSGNJenc0TlFOZWpSSlRIN09KTjV1OUpOMGdnSjkiOiB7ImRhdGEiOiB7InJlZGlyZWN0X3VyaSI6ICJodHRwczovL2NoYXQuaWhlcC5hYy5jbi9jYWxsYmFjayIsICJ1cmwiOiAiaHR0cHM6Ly9sb2dpbi5paGVwLmFjLmNuL29hdXRoMi9hdXRob3JpemU/cmVzcG9uc2VfdHlwZT1jb2RlJmNsaWVudF9pZD0zNjE5OCZyZWRpcmVjdF91cmk9aHR0cHMlM0ElMkYlMkZjaGF0LmloZXAuYWMuY24lMkZjYWxsYmFjayZzdGF0ZT1KSGNJenc0TlFOZWpSSlRIN09KTjV1OUpOMGdnSjkifSwgImV4cCI6IDE3Mjg4ODk4MTMuMjQ2MjUyOH19.Zw0bMA.hPuGb34zSkA4_rAu53aSZe1tE0g; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3Zjc3ZTYyLTU5ODItNGY1NS04MDdhLWI5ODkzZDI1MTljZCJ9.f6fQnFViby-JByNukKK8jfwutZHSRkfQYm6vj1KzY2Y',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
                }
            # message = 'what is your version?'
            # message = '你的版本是多少？'
            # data = {"model":"gpt-4o-2024-08-06",
            #         "modelName":"Julian-4o",
            #         "modelType":1,
            #         "prompt": message}
            data = {
                "stream": True,
                "model": "openai/gpt-4o-mini",
                "messages": [
                                {"role": "user",
                                 "content":message
                                }
                            ]
                }
            #
            #response = requests.request('POST', url, headers = headers, data = data,verify = False)
            response = requests.request('POST', url, headers = headers, data = json.dumps(data),verify = False)
            text = response.text

            it = re.finditer(r'"choices":\s\[{"delta":\s{"content":\s"(?P<content>.+?)",\s"function_call":',text) 
            # it = re.finditer(r'"choices":\s\[{"delta":\s{"content":\s(?P<content>.+?),\s"function_call":',text) 
            for m in it:
                content = m.group('content')
                while len(content) >= 6:
                    hexstr = content[0:6]
                    m = re.match(r'\\u(?P<hex>[0-9a-z]{4})', hexstr)
                    if m:
                        b = bytes.fromhex(m.group('hex'))
                        sql += b.decode('utf-16be')
                        content = content[6:]
                    else:
                        sql += content[0]
                        content = content[1:]
                sql += content
            break
        except Exception as e:
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for exception: {e}")
            time.sleep(5)
    #
    time.sleep(2)
    return sql

