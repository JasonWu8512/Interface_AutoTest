''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/8/9
===============
'''


import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.tradeorderserver.Apicommit import ApiCommit
from business.Jiliguala.user.ApiUser import ApiUser


@pytest.mark.menu
class Testcommit:
    """
    修改订单地址，提交地址
    """
    dm = Domains
    @classmethod
    def setup_class(cls):

        cls.dm = Domains()
        cls.config = cls.dm.set_env_path('prod')
        cls.dm.set_domain(cls.config['url'])
        cls.user = ApiUser()
        cls.CS_user = cls.config["CS_user"]
        cls.orderNo = cls.config["orderNo"]
        cls.token = cls.user.get_token(typ="mobile", u=cls.CS_user["user"], p=cls.CS_user["pwd"])
        print(type(cls.token))
        print(cls.token)
        cls.apicommit = ApiCommit(token=cls.token)

    def test01_apicommit(self):
        """
        发送请求
        recipient : 接收人
        mobile : 电话
        addressStreet : 详情地址
        addressProvince : 地区
        """
        resp = self.apicommit.api_commit(self.orderNo["orderNo"])
        check.equal(resp["code"], 0) # 断言返回状态码
        assert resp['data']['recipientAddress']['recipient'] == '测试'
        assert resp['data']['recipientAddress']['mobile'] == '12345670018'
        assert resp['data']['recipientAddress']['addressCity'] == '北京市'
        assert resp['data']['recipientAddress']['addressDistrict'] == '东城区'
        assert resp['data']['recipientAddress']['addressStreet'] == '测试测试'

