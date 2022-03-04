# -*- coding: utf-8 -*-
# get daily sentence from http://dict.eudic.net/home/dailysentence/
#

import requests
import re


class EduicContent(object):

    def __init__(self):
        self.url = 'http://dict.eudic.net/home/dailysentence/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.110 Safari/537.36 '
        }
        self.session = requests.session()
        self.session.headers = self.headers
        self.response = self.session.get(self.url, headers=self.headers, timeout=10)

    def get_daily_content(self):
        if self.response.status_code == 200:
            html = self.response.text
            sentence = re.search(r'<p class="sect-trans">.*</p>', html).group()[22:-4]
            img_url = re.search(r'<img src="http:.*jpg', html).group()[10:]
            return sentence, img_url
        else:
            return None
