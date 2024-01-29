# coding=utf-8
# @Time    : 2021/05/17 2:33 下午
# @Author  : tina_hu
# @File    : test_groupBuyFlow
import pytest_check

from business.businessQuery import usersQuery
from business.common.UserProperty import UserProperty
from business.Jiliguala.user.ApiUserInfo import ApiUserInfo
from business.xshare import ApiDiamondMall
from config.env.domains import Domains


class TestDiamondOrder(object):
    dm = Domains()
    dm.set_env_path("fat")
    config = dm.config
    dm.set_domain(config["url"])
    mobile = config["diamondMall"]["mobile"]
    mobile_no_addr = config["diamondMall"]["mobile_no_addr"]
    unionid = config["diamondMall"]["unionid"]

    @classmethod
    def setup_class(cls):
        """手机号发送验证码，保证user表有新用户数据"""
        apiUserInfo = ApiUserInfo()
        cls.usersQuery1 = usersQuery()
        apiUserInfo.api_get_websms(cls.mobile)
        res = cls.get_userInfo(mobile=cls.mobile, unionid=cls.unionid)
        cls.baseToken = res[0]
        cls.diaUserId = res[1]
        res1 = cls.get_userInfo(mobile=cls.mobile_no_addr, unionid=cls.unionid)
        cls.baseToken1 = res1[0]
        cls.diaUserId1 = res1[1]
        cls.diamondOrder = ApiDiamondMall(cls.baseToken)
        cls.diamondOrder1 = ApiDiamondMall(cls.baseToken1)

    def get_userInfo(mobile, unionid):
        """获取token"""
        user = UserProperty(mobile=mobile, unionid=unionid)
        baseToken = user.basic_auth
        userId = user.user_id
        wxToken = user.encryptWechatToken_bindwechat
        return baseToken, userId, wxToken

    def get_purchase_iid(self, iid, type):
        """查询测试数据是否在查询itemlist里，如没有就随机查询一个用来购买"""
        itemlist = self.diamondOrder.query_items()
        if iid not in itemlist:
            iid = self.diamondOrder.query_itepmByType(type=type)
        return iid

    def add_pointNum(self, pointnum=1):
        """查询当前钻石数，如果为0则充值，返回充值后的钻石数"""
        result = self.diamondOrder.api_get_diamondUser()
        num = result["data"]["point"]
        if num == 0:
            self.usersQuery1.update_point_user_point(uid=self.diaUserId, pointNum=pointnum)
            current = num + pointnum
            return current
        else:
            return num

    def delete_buyNum(self, uid):
        """清空用户购买记录"""
        self.usersQuery1.update_point_user_num(uid)

    def update_cdks(self, itemid):
        """更新cdks为true"""
        self.usersQuery1.update_cdks(itemid=itemid)

    def query_user_limit(self, uid):
        """查询用户limit数"""
        result = self.usersQuery1.get_point_user(_id=uid)["limit"]["t2"]
        return result

    def make_order(self, iid, type, buynum=None):
        # 查询测试数据是否在查询itemlist里，如没有就随机查询一个用来购买
        iid = self.get_purchase_iid(iid=iid, type=type)
        # 查询当前购买次数，商品价格，库存
        res = self.diamondOrder.query_itemBuyNum(iid=iid)
        if buynum == None:
            buynum = res[0]
        buypoint = res[1]
        # 查询当前钻石数，为0的话充值
        beforePointNum = self.add_pointNum(buypoint)
        result = self.diamondOrder.api_put_UserOrder(iid=iid, num=buynum, comment="")
        print(result)
        return result, beforePointNum

    # def delete_address(self,uid):
    #     """删除地址"""
    #     usersQuery2=usersQuery()
    #     usersQuery2.update_user_addr(uid)

    def test_01_putOrder_physical(self):
        """type=0实物奖品兑换JLGL_reward099"""

        result, initPointNum = self.make_order(iid="JLGL_reward099", type=0)
        if result["code"] == 0:
            pytest_check.not_equal(result["data"]["oid"], "", "检查oid返回不为空，下单成功")

        else:
            print("错误code：%d" % result["code"], "错误msg：%s" % result["msg"])
            assert result["code"] == 0
        # 再次查询购买钻石数
        currentPointNum = self.diamondOrder.query_pointNum()
        pytest_check.equal(currentPointNum, initPointNum - 1, "检查消耗钻石是否正确")

    def test_02_getOrderList(self):
        """下单后去订单列表查询已下单的订单"""
        result1 = self.make_order(iid="JLGL_reward099", type=0)[0]
        orderid = result1["data"]["oid"]
        result = self.diamondOrder.api_get_orders(pageSize=100)
        a = []
        for i in result["data"]["list"]:
            a.append(i["order"])
        pytest_check.is_in(orderid, a, "检查下单列表里是否返回已下单的订单")

    def test_03_putOrder_physical_fail1(self):
        """实体物品下单失败场景，没有地址"""

        # 查询测试数据是否在查询itemlist里，如没有就随机查询一个用来购买
        iid = self.get_purchase_iid(iid="JLGL_reward099", type=0)
        # self.delete_address(self.diaUserId)
        # 查询当前购买次数
        buynum = self.diamondOrder1.query_itemBuyNum(iid=iid)[0]
        result = self.diamondOrder1.api_put_UserOrder(iid=iid, num=buynum, comment="")
        print(result)
        pytest_check.equal(result["data"]["oid"], "NeedAddress", "检查没有地址下单失败场景")

    def test_04_putOrder_physical_fail2(self):
        """钻石数不够，下单失败"""

        # 查询当前钻石数，为0的话充值
        initPointNum = self.add_pointNum()
        # 查询一个当前钻石数买不了的iid
        result = self.diamondOrder.api_get_items(pageSize=100, promoterZoneFlag=0)
        for i in result["data"]["list"]:
            if i["point"] > initPointNum:
                iid = i["iid"]
                break
        # 查询当前购买次数
        buynum = self.diamondOrder.query_itemBuyNum(iid=iid)[0]
        result = self.diamondOrder.api_put_UserOrder(iid=iid, num=buynum, comment="")
        print(result)
        pytest_check.equal(result["data"]["oid"], "", "检查钻石数量不够下单失败场景")

    def test_05_putOrder_guaguaVirtual(self):
        """type=1呱呱虚拟奖品兑换JLGL_reward098"""

        result, initPointNum = self.make_order(iid="JLGL_reward098", type=1)
        if result["code"] == 0:
            pytest_check.not_equal(result["data"]["oid"], "", "检查oid返回不为空，下单成功")

        else:
            print("错误code：%d" % result["code"], "错误msg：%s" % result["msg"])
            assert result["code"] == 0
        # 再次查询购买钻石数
        currentPointNum = self.diamondOrder.query_pointNum()
        pytest_check.equal(currentPointNum, initPointNum - 1, "检查消耗钻石是否正确")

    def test_06_putOrder_guaguaVirtual_fail1(self):
        """库存不够，下单失败"""
        # 查询一个库存为0的iid
        result = self.diamondOrder.api_get_items(pageSize=100, promoterZoneFlag=0)
        for i in result["data"]["list"]:
            if i["store"] == 0:
                iid = i["iid"]
                break
        result = self.make_order(iid=iid, type=1)[0]
        pytest_check.equal(result["data"]["oid"], "NoStore", "检查库存不够下单失败场景")

    def test_07_putOrder_Cash(self):
        """type=3现金5元奖品兑换JLGL_reward097"""

        # 清空用户购买记录
        self.delete_buyNum(self.diaUserId)
        result, initPointNum = self.make_order(iid="JLGL_reward097", type=3)
        if result["code"] == 0:
            pytest_check.not_equal(result["data"]["oid"], "", "检查oid返回不为空，下单成功")

        else:
            print("错误code：%d" % result["code"], "错误msg：%s" % result["msg"])
            assert result["code"] == 0
        # 再次查询购买钻石数
        currentPointNum = self.diamondOrder.query_pointNum()
        pytest_check.equal(currentPointNum, initPointNum - 1, "检查消耗钻石是否正确")

    def test_08_putOrder_Cash_fail(self):
        """type=3现金5元奖品兑换只能兑换一次，超过一次失败JLGL_reward097"""
        # 查询测试数据是否在查询itemlist里，如没有就随机查询一个用来购买
        result = self.make_order(iid="JLGL_reward097", type=3, buynum=1)[0]
        pytest_check.equal(result["data"]["oid"], "", "检查oid返回为空，下单失败")

    def test_09_putOrder_otherVirtual(self):
        """type=2第三方虚拟奖品兑换JLGL_reward096"""
        # 更新对应的cdks为true
        self.update_cdks(itemid="JLGL_reward096")
        result, initPointNum = self.make_order(iid="JLGL_reward096", type=2)
        if result["code"] == 0:
            pytest_check.not_equal(result["data"]["oid"], "", "检查oid返回不为空，下单成功")

        else:
            print("错误code：%d" % result["code"], "错误msg：%s" % result["msg"])
            assert result["code"] == 0
        # 再次查询购买钻石数
        currentPointNum = self.diamondOrder.query_pointNum()
        pytest_check.equal(currentPointNum, initPointNum - 1, "检查消耗钻石是否正确")

    def test_10_putOrder_otherVirtual_fail(self):
        """type=2第三方虚拟奖品兑换,当用户的limit<item的钻石价格，达到购买上限下单失败"""
        # 查询用户的limit数
        userlimit = self.query_user_limit(uid=self.diaUserId)
        print(userlimit)
        # 查询一个当前钻石价格>limit的iid
        result = self.diamondOrder.api_get_items(pageSize=100, promoterZoneFlag=0)
        for i in result["data"]["list"]:
            if i["point"] > userlimit and i["type"] == 2:
                iid = i["iid"]
                break
        result = self.make_order(iid=iid, type=2)[0]
        pytest_check.equal(result["data"]["oid"], "Limited", "检查用户才到limit不能下单")
