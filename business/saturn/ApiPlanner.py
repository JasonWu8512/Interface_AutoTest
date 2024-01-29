# @Time    : 2021/3/16 1:39 下午
# @Author  : ygritte
# @File    : ApiPlanner

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiPlanner:
    """
    PlannerController
    """
    root = "/inner/saturn-crm"

    def __init__(self):
        self.host = Domains.config.get('saturn_gateway')
        self.headers = {"version": "1", "Content-Type": "application/json;charset=utf-8"}

    def api_planner_new(self, name, group, subject, email, wxQrcodeUrl, wxNickName, wxAccount):
        """
        新增规划师接口
        """
        api_url = f'{self.root}/planner/new'
        body = {
           "name": name,
            "group": group,
            "subject": subject,
            "email": email,
            "wxQrcodeUrl": wxQrcodeUrl,
            "wxNickName": wxNickName,
            "wxAccount": wxAccount
        }
        resp = send_api_request(url=self.host + api_url, method="post", paramType="json", paramData=body,
                                headers=self.headers)
        return resp

    def api_planner_get(self, uid, subject):
        """
        分配规划师接口
        """
        api_url = f'{self.root}/planner/get'
        body = {
            "uid": uid,
            "subject": subject
        }
        resp = send_api_request(url=self.host + api_url, method="get", paramType="params", paramData=body,
                                headers=self.headers)
        return resp

    # https://dev-crm.jiliguala.com/api/planner/get_flow_distribution_ghs
    def api_crm_get_planner(self, uid, subject_type, source="eshop", details="T1GE"):
        """
        crm侧查询下沉锁粉用户购买正价课后分配的规划师  注意：这里是fat环境的ip和端口
        """
        api_url = "http://10.50.221.117:7193/api/planner/get_flow_distribution_ghs"
        body = {
            "uid": uid,
            "subject_type": subject_type,
            "source": source,
            "details": details
        }
        resp = send_api_request(url=api_url, method='post', paramType="json", paramData=body,
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path("fat")
    pl = ApiPlanner()
    res = pl.api_crm_get_planner(uid="1d37b5825a804c22a6b684f63e6167a4", subject_type="english",source="eshop",
                                 details="L1XX")
    res1 = pl.api_planner_get(uid='1d37b5825a804c22a6b684f63e6167a4', subject='english')
    print(res)
    print(res1)