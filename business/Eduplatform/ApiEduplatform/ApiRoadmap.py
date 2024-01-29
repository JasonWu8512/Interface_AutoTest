'''
@Author : degg_wang
@Date : 2022/9/6
@File : ApiRoadmap
'''


from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains

class ApiRoadmap(object):
    """
        灵活路线图
    """

    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def leaf_node_complete(self, bid, finishTime, nodeId):
        """
            灵活路线图叶节点完课
            :param bid:   孩子ID
            :param finishTime:   完课时间
            :param nodeId: nodeId
            :return:
        """
        api_url = "/api/v1/roadmap/leafNodeComplete"
        body = {
            "bid": bid,
            "finishTime": finishTime,
            "nodeId": nodeId
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                                headers=self.headers)
        return resp

    def get_leaf_node_records(self, bid, subjectId):
        """
            获取叶子节点完课情况
            :param bid:   孩子ID
            :param subjectId:   学科id（STYY）
            :return:
        """
        api_url = "/api/v1/roadmap/getLeafNodeRecords"
        body = {
            "bid": bid,
            "subjectId": subjectId
        }
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="post",
                                headers=self.headers)
        return resp
