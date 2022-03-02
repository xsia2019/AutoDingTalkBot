# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import time
import urllib.request
import sys


class DingTalkWebHook(object):
    def __init__(self,  url=None, secret=None):
        """
        secret: 钉钉机器人加签信息
        url: 钉钉机器人没有加签的hook url
        """
        if secret is not None:
            secret = secret
        else:
            secret = 'secret'
        if url is not None:
            url = url
        else:
            url = 'https://oapi.dingtalk.com/robot/send?access_token=access_token'

        timestamp = round(time.time() * 1000)
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        self.webhook_url = url + '&timestamp={}&sign={}'.format(timestamp, sign)

    def send_message(self, data):
        headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }
        send_data = json.dumps(data)
        send_data = send_data.encode('utf-8')
        request = urllib.request.Request(url=self.webhook_url, headers=headers, data=send_data)

        opener = urllib.request.urlopen(request)
        print(opener.read())


if __name__ == '__main__':
    my_secret = 'SECf1d13f27bbceb66a187c37e1a4e422e87e52d7718727f3a548f9b9533b94c3c0'
    my_url = 'https://oapi.dingtalk.com/robot/send?access_token' \
             '=80da5c52f55d190c732e25b0d222249c2e509a29df36c78d3b389b14d211c724'
    webhook = sys.argv[0]
    secret = sys.argv[1]

    my_makedown = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'Hello, world!',
            'text': '#### 测试消息\n'
        },
        'at': {
            'atMobiles': [
                '17777909650'
            ],
            'isAtAll': False
        }
    }

    ding = DingTalkWebHook(secret=my_secret, url=my_url)
    ding.send_message(my_makedown)
    autoding = DingTalkWebHook(url=webhook, secret=secret)
    autoding.send_message(my_makedown)

