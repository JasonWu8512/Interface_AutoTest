# coding=utf-8
# @Time    : 2020/8/6 1:07 下午
# @Author  : keith
# @File    : testLogin

import pytest
import pytest_check as check

from business.Jiliguala.reso.Audio.ApiAudio import ApiAudio
from business.Jiliguala.user.ApiUser import ApiUser
from config.env.domains import Domains


@pytest.mark.reso
class TestAudio(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['url'])
        user = ApiUser()
        # keith token
        cls.token = user.get_token(typ="mobile", u="13818207214", p="123456")
        cls.audio = ApiAudio(token=cls.token)

    def test_audios_channel(self):
        resp = self.audio.api_get_audios_channel()
        check.equal(resp["status_code"], 200)
        channels = resp["data"]
        for channel in channels:
            check.is_not_none(channel["ttl"])
            check.is_not_none(channel["thmb"])
            check.is_not_none(channel["channel"])
        return resp



if __name__ == '__main__':
    a = TestAudio()
    a.setUpClass()
    a.test_audios_channel()
