from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiSelectLevel:
    """
    级别选择页
    lessonbiz
    LessonController
    10.5以上用的是/api/lesson/details
    10.5以下用的是/api/lesson/buy
    """
    def __init__(self, token):
        self.host = Domains.config.get('url')
        self.root = '/api/lesson'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "version": "1",
            #"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 9; MI 8 SE MIUI/9.9.3); NiuWa : 110300; AndroidVersion : 11.3.0"
        }

    def api_select_details(self,bid):
        api_url = f"{self.host}{self.root}/details"
        body = {
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

    def api_select_old_version(self,bid,typ):
        api_url = f"{self.host}{self.root}/buy"
        body = {
            "bid":bid,
            "typ":typ
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("15900002229")
    token = user.basic_auth

    level_list=ApiSelectLevel(token)
    #resp=level_list.api_select_details("4427a1c703dd48c8ac332feaa9009828")
    resp = level_list.api_select_old_version("1b877919e16d4a8682bce4014bf70c6b","L1PH")
    print(resp)