''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2022/7/18
===============
'''

import pytest
import pytest_check as check
from config.env.domains import Domains
from business.Jiliguala.userbiz.ApiDeleteDevices import DeleteDevices


@pytest.mark.menu
class Test_deletedevice:
    dm = Domains

    @classmethod
    def setup_class(cls):
        cls.dm = Domains()
        cls.delete_user_devices = DeleteDevices()

    def test01_userlogin(self):
        """
        游客登陆
        """
        resp = self.delete_user_devices.login()
        check.equal(resp["code"], 0)

    def test02_delete__device(self):
        """验证设备是否移除"""
        resp = self.delete_user_devices.delete_devices()
        check.equal(resp["msg"], "该设备已移除")



