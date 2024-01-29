''' 
===============
@Project  :  JLGL_autotest
@Author   :  Anna
@Data     :  2023/12/27
===============
'''
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPage(object):
    """数字版权信息"""

    def __init__(self):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        # 设置域名host
        self.host = Domains.config.get('url')
        print(self.host)

    def api_page(self):
        """
        选择年龄页面，展示数字版权
        """
        api_url = "/api/age/page/info"
        print(self.host)
        resp = send_api_request(url=self.host + api_url, paramType='params', method="get", headers=self.headers)
        print(resp)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    a = ApiPage()
    a.api_page()
