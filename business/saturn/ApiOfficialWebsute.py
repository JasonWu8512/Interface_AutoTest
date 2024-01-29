# @Time    : 2021/3/17 4:58 下午
# @Author  : ygritte
# @File    : ApiOfficialWebsute

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiOfficialWebsite:
    """
    OfficialWebsiteController
    """
    root = "/api/saturn/website"

    def __init__(self):
        self.host = Domains.get_ggr_host()
        self.headers = {"version": "1", "Content-Type": "application/json;charset=utf-8"}

    def api_lead(self, mobile, province, city):
        """
        官网招商接口
        """
        api_url = f'{self.root}/lead'
        body = {
            "mobile": mobile,
            "province": province,
            "city": city
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json",
                                paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    ow = ApiOfficialWebsite()
    res = ow.api_lead(mobile="17778888345", province="陕西省",city="西安市")
    print(res)
