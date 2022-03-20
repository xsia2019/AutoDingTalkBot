class getJobinfo(object):

    def __init__(self, start_page, end_page):
        self.start_url = ''

        self.start_page = start_page
        self.end_page_ = end_page

    # 生成爬取信息的url
    def generate_url(self):
        for i in range(self.page_num, self.end_page + 1):
            url = self.start_url + str(i)
            yield url

    # 获取网页信息
    def get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    # 解析网页信息
    def parse_page(self, html):
        pass

    # 筛选网页信息
    def filter_page(self, html):
        pass

    # 模式化网页信息
    def format_page(self, html):
        pass

    # 运行爬虫
    def get_job_info_now(self):
        # 生成网页信息
        for url in self.generate_url():
            html = self.get_page(url)
            self.parse_page(html)

            # 取得网页html内容

            # 解析网页信息

            # 筛选网页信息

            # 生成md信息
