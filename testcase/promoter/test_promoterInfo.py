# coding=utf-8
# @Time    : 2021/3/30 5:20 下午
# @Author  : jerry
# @File    : test_promoterInfo.py

import pytest

from config.env.domains import Domains
from business.common.UserProperty import UserProperty
from business.common.PromoterProperty import PromoterProperty
from business.promoter.ApiPromoter import ApiPromoter
from business.promoter.ApiHome import ApiHome
from utils.enums.businessEnums import PromoterOperationEnum
from business.promoter.ApiCommodity import ApiCommodity
from business.promoter.ApiPromoterLogin import ApiPromoterLogin
from business.promoter.ApiLogOut import ApiLogOut
from business.zero.dataTool.ApiPromoterData import ApiPromoterData
from business.businessQuery import promoterQuery, pingxxorderQuery, usersQuery, wcuserQuery
from business.xshare.ApiWechat import ApiWechat
from business.promoter.ApiGroupPurchase import ApiGroupPurchase
from business.promoter.ApiPromoterOperation import ApiPromoterOperation


@pytest.mark.promoter
@pytest.mark.promoterInfo
class TestPromoterInfo:
    """推广人展示信息相关用例"""
    promoterQuery = promoterQuery()
    pingxxorderQuery = pingxxorderQuery()
    usersQuery = usersQuery()
    wcuserQuery = wcuserQuery()

    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('fat')
        Domains.set_domain(cls.config['url'])
        cls.promoterUser = UserProperty(cls.config['promoter']['promoter4'])  # 构建正常推广人的user实例
        cls.promoterOldUser = PromoterProperty(cls.config['promoter']['promoter4'])  # 构建正常推广人的user实例
        url = cls.config['promoter']['crm_promoter_url']
        # 设置wc_users 为当前当前用户uid
        cls.wcuserQuery.update_wc_users("o0QSN1SP68mKOo_SPD2gV_Omj4d4", uid=cls.promoterUser.user_id)
        cls.promoterGroupPurchase = ApiGroupPurchase(cls.promoterUser.encryptWechatToken_promoter,
                                                     cls.promoterUser.basic_auth)
        cls.promoter = ApiPromoter(cls.promoterUser.encryptWechatToken_promoter, cls.promoterUser.basic_auth)
        cls.promoterOld = ApiPromoter(cls.promoterUser.encryptWechatToken_promoter, cls.promoterOldUser.basic_auth)
        cls.promoter_home = ApiHome(cls.promoterUser.encryptWechatToken_promoter, cls.promoterUser.basic_auth)
        cls.commodity = ApiCommodity(cls.promoterUser.encryptWechatToken_promoter, cls.promoterUser.basic_auth)
        cls.promoterLogin = ApiPromoterLogin(cls.promoterUser.encryptWechatToken_promoter, cls.promoterUser.basic_auth)
        cls.promoter_bind = ApiPromoterLogin(cls.promoterUser.encryptWechatToken_promoter)
        cls.promoter_dataTool = ApiPromoterData()
        cls.promoterLoginOut = ApiLogOut(cls.promoterUser.encryptWechatToken_promoter, cls.promoterUser.basic_auth)
        cls.wechat = ApiWechat(wechat_token=cls.promoterUser.encryptWechatToken_promoter,
                               auth_token=cls.promoterUser.basic_auth)
        cls.add_delete_tags = ApiPromoterOperation(url=url)

    @classmethod
    def teardown_class(cls):
        pass

    def cmpList(self, list1, list2):
        flag = False
        for x in list1:
            if x in list2:
                flag = True
            else:
                flag = False
                break
        return flag

    @pytest.mark.parametrize("operation,mobile", [("update_promoter_state_inactive", "13701941089")])
    def test_first_login(self, operation, mobile):
        """
        推广人首次登陆，会出现加组长页面
        """
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                     operation=operation,
                                                     mobile=mobile
                                                     )  # 修改推广人状态为未激活状态

        #  首次登陆会额外调取login和config接口
        login_res = self.promoterLogin.api_promoter_login(mobile)
        config_res = self.promoter.api_promoter_config()
        promoter_info = self.promoterQuery.get_promoter_accounts(mobile=mobile)
        assert login_res['code'] == 0
        assert config_res['code'] == 0
        assert login_res['data']['nick'] == promoter_info['nick']
        assert login_res['data']['tok'] == promoter_info['tok']
        assert login_res['data']['uid'] == promoter_info['uid']
        assert config_res['data']['externalQrCodeUrl'] != ""
        assert config_res['data']['internalQrCodeUrl'] != ""
        assert promoter_info['state'] == 'active'

    def test_promoter_login(self):
        """
        正常登录
        """
        bind_resp = self.promoter_bind.api_check_bind()
        promoter = self.promoterQuery.get_promoter_accounts(mobile=self.promoterUser.mobile)
        assert bind_resp["data"]["isBind"] is True
        assert bind_resp['data']['userInfo']['state'] == "active"
        assert bind_resp["code"] == 0
        assert bind_resp["data"]["userInfo"]["nick"] == promoter["nick"]
        assert bind_resp["data"]["userInfo"]["totalAmount"] == promoter["totalAmount"]
        assert bind_resp["data"]["userInfo"]["promoterLevel"] == promoter["level"]
        assert bind_resp["data"]["userInfo"]["totalRevenue"] == promoter["totalRevenue"]
        assert bind_resp["data"]["userInfo"]["guaid"] == promoter["guaid"]

    @pytest.mark.parametrize("state", ["invalid"])
    def test_promoter_invalid(self, state):
        """
        推广人名下粉丝全部退款呱美课，推广人账号变为无效，且不在白名单，可正常登陆，但无法提现
        """
        content = {'state': state}
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                     operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
                                                     mobile=self.promoterUser.mobile,
                                                     content=content)  # 修改推广人状态为已失效状态
        res = self.promoter_bind.api_check_bind()
        self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
                                                     operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
                                                     mobile=self.promoterUser.mobile,
                                                     content={'state': 'active'})  # 还原正常状态
        assert res["data"]['userInfo']['promoterStatus'] == 1
        assert res["data"]['userInfo']['state'] == "invalid"

    def test_promoter_income(self):
        """
        测试推广人收入
        """
        pro_resp = self.promoterLogin.api_check_bind()
        over_res = self.promoter_home.api_income_overview()
        assert over_res['code'] == 0
        assert pro_resp["data"]['userInfo']["totalRevenue"] == over_res["data"]["totalRevenue"]

    def test_get_top_commodities(self):
        """
        主推商品展示是否正常
        """
        top_res = self.commodity.api_top_recommend_commodities()
        assert len(top_res["data"]) > 0
        assert top_res['code'] == 0

    def test_get_recommend_consumed(self):
        """
        推广记录中已消费数据是否准确
        """
        c_res = self.promoter.api_recommend_consumed()
        assert c_res['code'] == 0
        assert isinstance(c_res['data'], list)

    def test_get_promoter_fans(self):
        """
        推广人粉丝是否正确
        """
        check_res = self.promoter_bind.api_check_bind()
        db_promoter_account = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        # 计算粉丝的数量
        db_promoter_fans = self.promoter.api_promoter_invitees_fans(1)
        englishFansCount = 0
        mindFansCount = 0
        if db_promoter_fans['data']['englishFansCount'] != None:
            englishFansCount = int(db_promoter_fans['data']['englishFansCount'])
        if db_promoter_fans['data']['mindFansCount'] != None:
            mindFansCount = int(db_promoter_fans['data']['mindFansCount'])

        assert check_res['data']['userInfo']['id'] == db_promoter_account['_id']
        assert check_res['data']['userInfo']['nick'] == db_promoter_account['nick']
        assert check_res['data']['userInfo']['ava'] == db_promoter_account['ava']
        assert check_res['data']['userInfo']['promoterLevel'] == db_promoter_account['level']
        assert check_res['data']['userInfo']['state'] == db_promoter_account['state']
        assert check_res['data']['userInfo']['fansNum'] == englishFansCount + mindFansCount

    @pytest.mark.parametrize("subject,orderSubject", [(1, 1), (2, 3)])
    def test_get_english_mind_fans(self, subject, orderSubject):
        """
        推广人英语\思维科目粉丝
        """
        db_promoter_account = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        # 计算粉丝的数量
        interface_promoter_fans = self.promoter.api_promoter_invitees_fans(orderSubject)
        db_promoter_fans = self.promoterQuery.get_promoter_fans(uid=self.promoterUser.user_id, subjectType=subject)
        english_fans_number = 0
        interface_fanslist = []
        db_fanslist = []
        for res in interface_promoter_fans['data']['fansList']:
            interface_fanslist.append(res['guaid'] + str(res['validInvitation']))
        for res_fan in db_promoter_fans:
            english_fans_number = english_fans_number + 1
            userInfo = self.usersQuery.get_users(_id=res_fan['childUid'])
            if res_fan['relationType'] == -1:
                db_fanslist.append(userInfo['guaid'] + 'False')
            if res_fan['relationType'] == 0:
                db_fanslist.append(userInfo['guaid'] + 'True')
        if subject == 1:
            assert interface_promoter_fans['data']['englishFansCount'] == english_fans_number
        else:
            assert interface_promoter_fans['data']['mindFansCount'] == english_fans_number
        assert interface_fanslist.sort() == db_fanslist.sort()

    def test_get_check_band(self):
        """
        推广人信息是否正确
        """
        check_res = self.promoter_bind.api_check_bind()
        db_promoter_account = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        # 计算粉丝的数量
        db_promoter_fans = self.promoter.api_promoter_invitees_fans(1)
        englishFandCount = 0
        mindFandCount = 0
        if db_promoter_fans['data']['englishFansCount'] != None:
            englistFandCount = englishFandCount + int(db_promoter_fans['data']['englishFansCount'])
        if db_promoter_fans['data']['mindFansCount'] != None:
            mindFandCount = mindFandCount + int(db_promoter_fans['data']['mindFansCount'])

        assert check_res['data']['userInfo']['id'] == db_promoter_account['_id']
        assert check_res['data']['userInfo']['nick'] == db_promoter_account['nick']
        assert check_res['data']['userInfo']['ava'] == db_promoter_account['ava']
        assert check_res['data']['userInfo']['promoterLevel'] == db_promoter_account['level']
        assert check_res['data']['userInfo']['state'] == db_promoter_account['state']
        assert check_res['data']['userInfo']['fansNum'] == englistFandCount + mindFandCount

    def test_get_banner_resource(self):
        """
        推广人资源位信息
        """
        banner_res = self.promoter_home.api_promoter_home()
        db_promoter_banner = self.promoterQuery.get_promoter_banner(_id="lianbaotuan")
        assert banner_res['data']['banners'][0]['bannerImageUrl'] == db_promoter_banner['bannerImageUrl']
        assert banner_res['data']['banners'][0]['forwardUrl'] == db_promoter_banner['forwardUrl']
        assert banner_res['data']['banners'][0]['posterId'] == str(db_promoter_banner['posterId'])
        assert banner_res['data']['banners'][0]['sort'] == db_promoter_banner['sort']

    def test_get_promoter_consumed(self):
        """
        推广记录中已消费数据是否准确
        """
        c_res = self.promoter.api_recommend_consumed()
        proid = self.promoter_bind.api_check_bind()["data"]["userInfo"]["id"]
        pro_order = self.promoterQuery.get_promoter_order(promoterId=proid)
        res_list = []
        ord_list = []
        for res in c_res["data"]:
            res_list.append(res["guaid"])
        for order in pro_order:
            uid = self.pingxxorderQuery.get_pingxxorder(_id=order['_id'])['uid']
            ord_list.append(self.usersQuery.get_users(_id=uid)["guaid"])
        res_list.sort()
        ord_list.sort()
        assert res_list == ord_list

    def test_promoter_income(self):
        """
        测试推广人收入
        """
        over_res = self.promoter_home.api_income_overview()
        db_promoterAccount = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        # 退款金额为空，默认为0
        refundingRevenue = 0
        if 'refundingRevenue' in db_promoterAccount:
            refundingRevenue = db_promoterAccount['refundingRevenue']
        # 完成金额为空，默认为0
        doneRevenue = 0
        if 'doneRevenue' in db_promoterAccount:
            doneRevenue = db_promoterAccount['doneRevenue']

        availableRevenue = over_res['data']['totalRevenue'] - over_res['data'][
            'frozenRevenue'] - refundingRevenue - doneRevenue
        assert over_res['data']['frozenRevenue'] == db_promoterAccount['frozenRevenue']
        assert over_res['data']['totalRevenue'] == db_promoterAccount['totalRevenue']
        assert over_res['data']['availableRevenue'] == availableRevenue

    def test_get_income_detail(self):
        """
        推广记录中已消费数据是否准确
        """
        c_res = self.promoter_home.api_income_detail()
        proid = self.promoter_bind.api_check_bind()["data"]["userInfo"]["id"]
        pro_order = self.promoterQuery.get_promoter_order(promoterId=proid)
        res_list = []
        ord_list = []
        for res in c_res["data"]:
            res_list.append(res["itemid"] + str(res["amount"]) + str(res["revenue"]))

        for order in pro_order:
            ord_list.append(order["itemid"] + str(order["amount"]) + str(order["revenue"]))

        assert self.cmpList(ord_list, res_list) == True

    def test_promoter_histroy_fans(self):
        """
        历史粉丝查看记录
        """
        histroy_fans = self.promoterOld.api_prometer_fans_list()
        promoterInfo = self.promoterQuery.get_promoter_history_fans(uid=self.promoterUser.user_id)
        promoterwechat = self.promoterQuery.get_promoter_wechat(promoterId=self.promoterUser.user_id)
        assert histroy_fans['data']['fans'][0]['_id'] == promoterInfo['_id']
        assert histroy_fans['data']['fans'][0]['nick'] == promoterInfo['nick']
        assert histroy_fans['data']['fans'][0]['ava'] == promoterInfo['ava']
        if histroy_fans['data']['fans'][0]['status'] == '已领取':
            status = 'registered'
        assert status == promoterInfo['status']

    def test_write_promopter_recruit_form(self):
        """
        填写招募信息
        """
        update_promoter = self.promoterQuery.update_promoter_accounts("JLGL_TEST_WYW1", valid=False)
        c_res = self.promoter.api_promoter_recruit_form_update(wechatAccount="yyy", province="北京市", city="北京市",
                                                               promoterGoals=["赚回学费"])
        db_promoter = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        assert db_promoter['city'] == '北京市'
        assert db_promoter['province'] == '北京市'
        assert db_promoter['valid'] == True
        assert db_promoter['promoterGoals'][0] == '赚回学费'

    @pytest.mark.parametrize("promoterId,tags,type",
                             [("JLGL_TEST_WYW1", "地推", "add"), ("JLGL_TEST_WYW1", "", "delete")])
    def test_add_delete_promoter_tags(self, promoterId, tags, type):
        """
        添加和删除、查询推广人的低质流量标签
        """
        self.add_delete_tags.api_update_tags(promoterId, tags)
        res = self.add_delete_tags.api_find_tags(promoterId)
        if type == 'add':
            assert res['data'][0] == '地推'
        if type == 'delete':
            assert res['data'][0] == ''

    @pytest.mark.parametrize("flag", ["success", "fail"])
    def test_purchase_success(self, flag):
        """
        产看拼团成功,失败信息
        """
        if flag == 'success':
            purchase_success_res = self.promoterGroupPurchase.api_group_purchase_list(1)
        if flag == 'fail':
            purchase_success_res = self.promoterGroupPurchase.api_group_purchase_list(0)
        id = ""
        members = ""
        for res in purchase_success_res['data']['orders']:
            id = id + res['id']
            for member in res['members']:
                members = members + member['guaid'] + member['subject']
        expect_success_ids = '60a754ce03434242e12b8e3c609cf698b82a81088d417de1'
        expect_sucesss_members = '1503702英语1503703英语1499617思维1503054思维'
        expect_fail_ids = '60a4c5e2b82a81088d418695'
        expect_fail_members = '1503537英语'
        if flag == "success":
            assert expect_success_ids == id
            assert members == expect_sucesss_members
        if flag == "fail":
            assert expect_fail_ids == id
            assert members == expect_fail_members

    def test_promoter_logout(self):
        """
        正常登出,推广人表unionid 和openid 设置为空。删除 promoterWechat的记录
        """
        self.promoterLogin.api_check_bind()
        self.wechat.api_sbind(self.promoterUser.user_id)
        logout_res = self.promoterLoginOut.api_log_out()
        promoterInfo = self.promoterQuery.get_promoter_accounts(uid=self.promoterUser.user_id)
        promoterwechat = self.promoterQuery.get_promoter_wechat(promoterId=self.promoterUser.user_id)
        assert logout_res['code'] == 0
        assert logout_res['status_code'] == 200
        assert promoterInfo['unionId'] == ''
        assert promoterInfo['openid'] == ''
        assert promoterwechat == None

    # def test_promoter_fans(self):
    #     """
    #     测试粉丝数量是否正确
    #     """
    #     res = self.promoterLogin.api_promoter_login(self.promoterUser.mobile)
    #     pro_resp = self.promoterLogin.api_check_bind()
    #     fana_res = self.promoter.api_promoter_invitees_fans(orderSubject=1)
    #     assert fana_res["code"] == 0
    #     assert fana_res["data"]["englishFansCount"] + fana_res["data"]["mindFansCount"] == pro_resp["data"]["userInfo"][
    #         'fansNum']

    # @pytest.mark.parametrize("state", ["forbidden"])
    # def test_promoter_forbidden(self, state):
    #     """
    #     推广人资格被封号，登陆失败
    #     """
    #     content = {'state': state}
    #     self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
    #                                                  operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
    #                                                  mobile=self.promoterUser.mobile,
    #                                                  content=content)  # 修改推广人状态为取消状态
    #     res = self.promoter_bind.api_check_bind()
    #     self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
    #                                                  operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
    #                                                  mobile=self.promoterUser.mobile,
    #                                                  content={'state': 'active'})  # 还原正常状态
    #     assert res["code"] == 43334
    #     assert res["msg"] == "您的账号存在风险，请联系客服"

    # @pytest.mark.parametrize("state", ["frozen"])
    # def test_promoter_frozen(self, state):
    #     """
    #     推广人退款呱美课，账号变成已冻结，且不在白名单，登陆失败
    #     """
    #     content = {'state': state}
    #     self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
    #                                                  operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
    #                                                  mobile=self.promoterUser.mobile,
    #                                                  content=content)  # 修改推广人状态为冻结状态
    #     res = self.promoter_bind.api_check_bind()
    #     self.promoter_dataTool.api_set_promoter_data(env=self.config['env'],
    #                                                  operation=PromoterOperationEnum.get_chinese("修改推广人信息"),
    #                                                  mobile=self.promoterUser.mobile,
    #                                                  content={'state': 'active'})  # 还原正常状态
    #     assert res["code"] == 43333
    #     assert res["msg"] == "您已退款呱美课"
