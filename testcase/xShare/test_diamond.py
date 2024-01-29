# -*- coding: utf-8 -*-
# @Time: 2021/3/31 2:11 下午
# @Author: sunny.jia
# @File: testDiamond
# @Software: PyCharm

from business.common.UserProperty import UserProperty
from business.xshare.ApiDiamond import ApiDiamond
from config.env.domains import Domains
from business.businessQuery import xshareQuery,usersQuery


class TestDiamond(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('fat')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])

        #初始化数据库操作对象
        cls.db_user = usersQuery()
        cls.dbchaxun = xshareQuery()

        # 初始化不同身份用户
        cls.english_user = UserProperty(cls.config["xshare"]["point_user"])
        cls.english_user_id = cls.english_user.user_id
        # cls.user1 = UserProperty(cls.mobile1)  # 构建英语正价课用户user实例
        cls.auth_token = cls.english_user.basic_auth

        #初始化钻石商城用户实例
        cls.diamond_right = ApiDiamond(cls.auth_token)

        #查询用户数据
        cls.data = cls.dbchaxun.get_point_user(cls.english_user_id)

    def test_right_Diamond(self):
        """"
        用户的钻石展示正确
        """
        res = self.diamond_right.api_get_Diamond_user()

        assert res['data']['total'] == self.data['total']
        assert res['data']['point'] == self.data['point']

    def test_diamond_user_invitees(self):
        """"
        用户已邀请好友数展示正确
        """
        res = self.diamond_right.api_diamond_user_invitees()
        api_friends_num =len(res['data']['list'])
        assert api_friends_num == len(self.data['invitees'])

    def test_diamond_user_orders(self):
        """"
        用户兑换历史展示正确
        """
        res = self.diamond_right.api_diamond_user_orders()  # 接口请求结果
        data = self.dbchaxun.get_point_order(uid=self.english_user_id)  # 数据查询结果

        assert res['code'] == 0   # 接口是否跑通
        assert res['data']['list'][0]['order'] == data['_id']
