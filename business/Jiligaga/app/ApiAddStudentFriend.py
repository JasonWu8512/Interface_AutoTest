"""
=========
Author:WenLing.xu
time:2023/11/29
=========
"""
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiAddStudentFriend(object):
    def __init__(self, cookies=None):
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',

            "platform": "ios",
            "dev_uni_id": "C264F398 - 4132 - 4162 - BC09 - 8DD21CA8CACC"
        }
        self.cookies = cookies
        self.dm = Domains()
        # 设置域名host
        self.host = self.dm.set_env_path("fat")["gaga_url"]
        self.crm_host = self.dm.set_env_path("fat")["crm_number_url"]

    def add_student_friend(self, termId, userId, tid):
        """
        添加班主任好友
        """
        api_url = "/api/inter/salesman/addStudentFriend"
        body = {
            "termId": termId,
            "userId": userId,
            "tid": tid
        }

        resp = send_api_request(url=self.crm_host + api_url, paramType="json", paramData=body, method="post",
                                headers=self.headers, cookies=self.cookies)
        print(self.cookies)
        print(resp)
        return resp

    # def add_student_friend(self, studentKeyWord, null=None):
    #     """
    #     学员信息列表查询-添加班主任好友状态
    #     """
    #     api_url = "/api/inter/salesman/pageQueryStudentList"
    #     body = {"deptUuid": "", "accountUuid": "", "email": "", "studentKeyWord": studentKeyWord, "termId": "",
    #             "channelType": null, "leadsOrderId": "", "isAddFriend": null, "conversionStatus": null,
    #             "previewLessonFinishCntList": null, "experienceLessonFinishCntList": null, "friendFollowStatus": null,
    #             "leadsOrderStartDate": "", "leadsOrderEndDate": "", "phoneSourceType": null, "babyContactNickName": "",
    #             "page": 1, "pageSize": 25, "testAccount": 0}
    #
    #     resp = send_api_request(url=self.crm_host + api_url, paramType="json", paramData=body, method="post",
    #                             headers=self.headers, cookies=self.cookies)
    #     print(resp)
    #     return resp
