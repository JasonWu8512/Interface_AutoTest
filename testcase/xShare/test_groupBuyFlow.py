# coding=utf-8
# @Time    : 2021/05/18 2:33 下午
# @Author  : tina_hu
# @File    : test_group_buy
import pytest_check

from business.businessQuery import usersQuery, xshareQuery
from business.common.UserProperty import UserProperty
from business.mars.ApiOrder import ApiOrder
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
from business.xshare.ApiGroupPurchase import ApiGroupPurchase
from business.xshare.ApiInitUser import ApiInitUser
from business.xshare.ApiWechat import ApiWechat
from config.env.domains import Domains


class TestGroupBuyFlow:
    gpid = "jlglpintuan202104_HDTT"
    tuanzhang_mobile = "19900000089"
    tuanyuan_mobile = "19900000099"

    @classmethod
    def setup_class(cls):
        """设置环境"""
        dm = Domains()
        config = dm.set_env_path("fat")
        dm.set_domain(config["url"])

    @classmethod
    def tuanzhang_data_init(cls, mobile):
        """手机号发送验证码，保证user表有新用户数据"""
        apiUserInfo = ApiUserInfo()
        apiUserInfo.api_get_websms(mobile)
        """通过手机号获取token"""
        purchaseUser = UserProperty(mobile, unionid="o0QSN1UG1Jru786lvAqCUd4wxB7I")
        purchaseUserToken = purchaseUser.basic_auth
        """获取wxtoken,uid绑定微信"""
        cls.userId = purchaseUser.user_id
        cls.purchaseUserWXToken = purchaseUser.encryptWechatToken_bindwechat
        apiWechat = ApiWechat(cls.purchaseUserWXToken)
        apiWechat.api_bind(cls.userId)
        cls.apiGroupPurchase = ApiGroupPurchase(purchaseUserToken)
        """删除uid下未完成的团单"""
        dbquery = xshareQuery()
        dbquery.delete_xshare_group_purchase_many(inviterId=cls.userId, status="notcompleted")

    @classmethod
    def tuanyuan_data_init(cls, mobile):
        """手机号发送验证码，保证user表有新用户数据"""
        apiUserInfo = ApiUserInfo()
        apiUserInfo.api_get_websms(mobile)
        """通过手机号获取token"""
        purchaseUser = UserProperty(mobile, unionid="o0QSN1UG1Jru786lvAqCUd4wxB7I")
        purchaseUserToken = purchaseUser.basic_auth
        print(purchaseUserToken)
        """获取wxtoken,uid绑定微信"""
        cls.userId = purchaseUser.user_id
        cls.purchaseUserWXToken = purchaseUser.encryptWechatToken_bindwechat
        apiWechat = ApiWechat(cls.purchaseUserWXToken)
        apiWechat.api_bind(cls.userId)
        cls.apiOrder = ApiOrder(cls.purchaseUserWXToken, purchaseUserToken)

    def init_user(self, mobile):
        purchaseUser_new = UserProperty(mobile)
        purchaseUserToken_new = purchaseUser_new.basic_auth
        apiInitUser = ApiInitUser(auth_token=purchaseUserToken_new)
        apiInitUser.api_sms_logout()
        xshareQueryInstance = usersQuery()
        code = xshareQueryInstance.get_users(mobile=mobile)["sms"]["code"]
        apiInitUser.api_users_security_info(mobile=mobile, smsCode=code)

    def test_createGroup(self):
        """团长开团"""
        global gpOid
        self.tuanzhang_data_init(self.tuanzhang_mobile)
        result = self.apiGroupPurchase.api_invite_order(self.gpid)
        print(result)
        if result["code"] == 0:
            pytest_check.not_equal(result["data"]["gpOid"], "NA", "检查创建团单成功")
            gpOid = result["data"]["gpOid"]

        else:
            errorCode = result["code"]
            errorMsg = result["msg"]
            pytest_check.equal(result["code"], 0, "创建团单失败，错误码：%s，错误信息：%s" % (errorCode, errorMsg))

    def test_joinGroup(self):
        """团员参团"""
        self.init_user(mobile=self.tuanyuan_mobile)
        self.tuanyuan_data_init(self.tuanyuan_mobile)
        result = self.apiOrder.api_create_v2(
            item_id="H5_Sample_Pintuan",
            nonce=None,
            source="NA",
            xshare_initiator=self.userId,
            sharer=self.userId,
            sp2xuIds=[2143],
            gpid=self.gpid,
            gpoid=gpOid,
        )
        print(result)
        assert result["code"] == 0
        oid = result["data"]["orderNo"]
        purchase = self.apiOrder.api_charge_v2(
            channel="wx_pub", oid=oid, pay_wechat_token_typ="silent", pay_wechat_token=self.purchaseUserWXToken
        )
        print(purchase)
