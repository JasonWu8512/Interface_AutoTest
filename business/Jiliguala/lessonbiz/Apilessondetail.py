''' 
===============================
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/9
===============================
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser


class ApiLessonDetail(object):
    """
    1.5课程详情页
    """
    root = '/api/super/v2/lessondetail'

    def __init__(self, token, agent):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            # "Basic YmFlZGY0ZWJjYjYwNDk3YTg5ZjlkZGI3OTA4N2U2ZDY6OGVhNmYxM2Q3Y2VjNGM1M2E3MWFiMTExZGUxMmFiMzc=",
            "User-Agent": agent  # 需要获取App版本，不同版本，
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_lessondetail(self, bid):
        """
        发送请求
        """
        api_url = "/api/super/v2/lessondetail"
        print(self.host + self.root)

        # fat环境数据
        body = {'lid': 'L3XX088',
                'bid': bid,
                'popup': 'true',
                'lesson_click': 1,
                'nonce': 'd2d9200a-d8eb-4959-838f-e8ab0e22e0d2'}
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)

        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('prod')
    dm.set_domain(config['url'])
    user = ApiUser()
    agent = config['agent']['ios_11.12.3']
    CS_user = config["CS_user"]
    lessondetail = config["LessonDetail"]
    token = user.get_token(typ="mobile", u=CS_user["user"], p=CS_user["pwd"])
    apilessondetail = ApiLessonDetail(token=token, agent=agent)
    resp = apilessondetail.api_lessondetail(lessondetail['bid'])
    print(resp)
