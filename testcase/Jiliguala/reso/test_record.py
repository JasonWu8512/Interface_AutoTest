# coding=utf-8
# @Time    : 2020/8/6 1:07 下午
# @Author  : keith
# @File    : testRecord

import pytest
import pytest_check as check

from business.Jiliguala.reso.Record.ApiRecord import ApiRecord
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.reso
class TestRecord(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['url'])
        user = ApiUser()
        cls.token = user.get_token(typ="mobile", u="13818207214", p="123456")
        cls.record = ApiRecord(token=cls.token)

    def setup(cls):
        print("setup")

    @pytest.mark.record
    def test_stop_record_config(self):
        resp = self.record.api_get_record_config()
        check.is_not_none(resp['data']['phoneme'])

    def test_stop_record(self):
        resp = self.record.api_get_record_config()
        check.is_not_none(resp['data']['phoneme'])


if __name__ == '__main__':
    a = TestRecord()
    a.setup_class()
    a.test_stop_record_config()
