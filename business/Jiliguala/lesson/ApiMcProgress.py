from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiMcProgress:
    """
    上报McPh路线图课程进度
    lessonbiz
    LessonController
    """
    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/super/lesson/mode'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }
    def api_report_mcprogress(self,lid,skutastid,bid,detail):
        """
        上报MCPH路线图进度
        :param bid:宝贝id
        :param lid:当前课程id
        :param detail:课程中的得分信息
        :param subtaskid:当前子课程id
        :return:
        """
        api_url = f"{self.host}{self.root}/api/lesson/progress"
        body = {
            "lid": lid,
            "subtaskid": subtaskid,
            "bid": bid,
            "detail":detail
        }
        resp = send_api_request(url=api_url, method="post", headers=self.headers, paramType="json", paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19991011051")
    token = user.basic_auth
    version = config['version']['ver11.3']
    lesson_porgress = ApiMcProgress(token, version)
    resp = lesson_porgress.api_report_mcprogress("L1MC17","L1MC171","1b877919e16d4a8682bce4014bf70c6b",[])
    print(resp)