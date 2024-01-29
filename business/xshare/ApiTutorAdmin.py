# coding=utf-8
# @Time    : 2021/03/18
# @Author  : qilijun
# @File    : ApiTutorAdmin.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiTutorAdmin:
    """"
    班主任相关接口，供CRM调用
    """
    def __init__(self):
        self.host = Domains.domain
        self.root = "/api/xshare/tutor"

    def api_new(self):
        """"
        同步新增班主任ID
        """
        api_url = "{}/new".format(self.root)
        body = {
            "id": "T999",
            "mid": "0h5q6q1WtclZfnrxuY5nzBouxebS99s1xtIWHDk7sEQ",
            "qrcode": "https://qiniucdn.jiliguala.com/dev/upload/2e8882e51566453aaaf5b0509d0f25e6_20210207103913.jpeg",
            "group": "上海思维1区B组",
            "email": "test_qilijun@jiliguala.com",
            "wechat_type": "A",
            "name": "思维班主任测试",
            "wechat_id": "",
            "status": "active",
            "customers_limit": 51,
            "gender": "",
            "subject_type": "math"
        }
        resp = send_api_request(url=self.host+api_url, method="post", paramData=body, paramType="json")
        return resp

    def api_edit(self):
        """"
        同步修改班主任ID
        """
        api_url = "{}/edit".format(self.root)
        body = {
            "id": "T999",
            "mid": "0h5q6q1WtclZfnrxuY5nzHCS4F0bMTki4gp3eTZOxr8",
            "qrcode": "https://qiniucdn.jiliguala.com/dev/upload/2e8882e51566453aaaf5b0509d0f25e6_20210207103913.jpeg",
            "group": "上海思维1区B组",
            "email": "test_qilijun@jiliguala.com",
            "wechat_type": "A",
            "name": "思维班主任测试",
            "wechat_id": "",
            "status": "active",
            "customers_limit": 81,
            "gender": "male",
            "subject_type": "math"
        }
        resp = send_api_request(url=self.host+api_url, method="post", paramData=body, paramType="json")
        return resp

    def api_batchupdateset(self):
        """"
        批量添加学员
        """
        api_url = "{}/batchupdateset".format(self.root)
        body = {
            "uidList": [
                {"id": "3629ee8f556447b2ac571a7df1dbf3f3", "subject_type": "math"}
            ]
        }
        resp = send_api_request(url=self.host+api_url, method="put", paramData=body, paramType="json")
        return resp

    def api_batchupdatelimit(self):
        """"
        修改班主任学员上限接口
        """
        api_url = "{}/batchupdatelimit".format(self.root)
        body = {
            "tutor_list": [
                {"id": "T999", "subject_type": "math"}
            ],
            "customers_limit": 99
        }
        resp = send_api_request(url=self.host+api_url, method="put", paramData=body, paramType="json")
        return resp

    def api_schedule(self):
        """"
        修改排班接口
        """
        api_url = "{}/schedule".format(self.root)
        body = {
            "date": "2021-03-19",
            "tutorList": [{"id": "T999", "weight": "10"}],
            "subject_type": "math"
        }
        resp = send_api_request(url=self.host+api_url, method="post", paramData=body, paramType="json")
        return resp


if __name__ =="__main__":
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    tutor = ApiTutorAdmin()
    # result = tutor.api_new()
    # result = tutor.api_edit()
    # result = tutor.api_batchupdateset()
    # result = tutor.api_batchupdatelimit()
    result = tutor.api_schedule()

    print(result)

