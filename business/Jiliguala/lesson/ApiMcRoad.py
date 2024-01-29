
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request

class ApiMcRoad():
    '''
    LessonController
    路线图-MC/PH课程路线图
    '''
    def __init__(self,token,version):
        self.host = Domains.config.get('url')
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }
    def api_get_mc_roadmap(self,bid,id,typ):
        '''
        MC/PH 课程路线图
        :param bid:宝贝id
        :param id:路线图IDL1MC、L2MC、L1PH-L4PH
        :param typ:
        :return:
        '''
        api_url = f"{self.host}/api/lesson/roadmap"
        body = {
            "typ": typ,
            "id": id,
            "bid": bid
        }
        resp = send_api_request(url=api_url, method="get", headers=self.headers, paramType="params", paramData=body)
        return resp

if __name__ == '__main__':
    dm=Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19595959540")
    token = user.basic_auth
    version=config['version']['ver11.0']

    roadmap = ApiMcRoad(token, version)
    resp = roadmap.api_get_mc_roadmap("4427a1c703dd48c8ac332feaa9009828", "L1MC", "MC")
    print(resp)
