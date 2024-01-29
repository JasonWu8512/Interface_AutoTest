# coding=utf-8
# @Time    : 2020/9/8 6:38 下午
# @Author  : keith
# @File    : ApiGroupPurchase

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
# from business.businessQuery import xshareQuery


# done
class ApiGroupPurchase(object):
    """
    转介绍 拼团
    """

    def __init__(self, token=None):
        self.root = "/api/xshare/grouppurchase"
        self.headers = {"Authorization": token, "version": "1"}
        self.wx_headers = {"Authorization": token, "version": "1", "openapp": "sp99",
                           "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_invite_order(self, gpid):
        """
        创建团单
        :param gpid:
        :return:
        """
        api_url = "{}/inviter/order".format(self.root)
        body = {
            "gpid": gpid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_get_invitee_order(self, gpid,gpoid):
        """
        团员获得团单信息
        :param
        :return:
        """
        api_url = "{}/invitee/order".format(self.root)
        body = {
            "gpid": gpid,
            'gpoid':gpoid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_inviter_order(self, gpid,gpoid):
        """
        团长获得团单信息
        :param
        :return:
        """
        api_url = "{}/inviter/order".format(self.root)
        body = {
            "gpid": gpid,
            'gpoid':gpoid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_judge_inviter(self, ):
        """
        查询是否为团长
        :param uid:
        :return:
        """
        api_url = "{}/inviter/judge".format(self.root)

        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=None, method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_gua_ticket(self):
        """
        获取呱呱爱分享ticket
        :return:
        """
        api_url = "{}/ticket".format(self.root)
        resp = send_api_request(url=self.host + api_url, paramType='params', method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_sts(self):
        """
        查询开课时间
        :param oid:
        :param receiver:
        :return:
        """
        api_url = "{}/sts".format(self.root)
        body = {
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_get_invitee_info(self, itemid):
        """
        查询用户信息
        :param itemid:
        :return:
        """
        api_url = "{}/invitee/classinfo".format(self.root)
        body = {
            "itemid": itemid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_config(self, gpid):
        """
        拼团-获取活动规则
        :param gpid:
        :return:
        """
        api_url = "{}/config".format(self.root)
        body = {
            "gpid": gpid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_get_push_reddot(self):
        """
        获取小红点状态
        """
        api_url = "{}/pushMessageRedDot".format(self.root)
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=None, method="get",
                                headers=self.wx_headers)
        return resp

    def api_click_red_dot(self):
        """
        点击小红点
        """
        api_url = "{}/pushMessage".format(self.root)
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=None, method="post",
                                headers=self.wx_headers)
        return resp

    def api_get_detail(self):
        """
        拼团-获取拼团详情
        """
        api_url = "{}/detail".format(self.root)
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=None, method="get",
                                headers=self.headers)
        return resp

    def api_inviter_noti(self,inviterId,gpid):
        """
        二次开团提醒
        """
        api_url = "{}/inviter/noti".format(self.root)
        body={
            "inviterId":inviterId,
            "gpid":gpid,
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp

    def api_rewardAddress(self,gpid,gpOid,comment,name,tel,region,addr):
        """
        根据团单号查询关联地址

        """
        api_url = "{}/rewardAddress".format(self.root)
        body={
            "gpid":gpid,
            "gpOid":gpOid,
            "comment":comment,
            "receiver":{
                "name":name,
                "tel":tel,
                "region":region,
                "addr":addr
            }
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        print(self.host + api_url)
        return resp

    def api_page_config(self,gpid):
        """
        页面配置
        """
        api_url = "{}/config/v2".format(self.root)
        body={
            'gpid':gpid
        }
        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.wx_headers)
        return resp

    def api_invitee_qualification(self,gpid,gpoid):
        """
        参团资格判断
        """
        api_url = "{}/invitee/qualification".format(self.root)
        body={
            'gpid':gpid,
            'gpoid':gpoid
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="post",
                                headers=self.wx_headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://fat.jiliguala.com")
    token = 'Basic MjhkMTQ4ZDQ1Nzc0NGYyNjg5NDE4YzkxNzczNzZiNDU6ZTNlMWFkMTJlZjUxNDU1MGFmMDFjMzc4N2E4MjE2ZDA='
    print(ApiGroupPurchase(token).api_invitee_qualification('jlglpintuan202104_Omo1','60767d6354b98c30215fe634'))
