# coding=utf-8
# @Time    : 2022/9/27 5:03 下午
# @Author  : Karen
# @File    : test_words.py


import pytest
from business.Reading.user.ApiUser import ApiUser as g
from business.Reading.user.ApiUser import ApiBaby
from business.MVP.words.ApiWords import ApiWords
from config.env.domains import Domains


@pytest.mark.MVP
class TestWords(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])

        # 游客
        cls.guest_token = g().get_guest_token()  # 创建游客并获取token
        ApiBaby(token=cls.guest_token).api_put_baby()  # 创建宝贝
        cls.guest = ApiWords(token=cls.guest_token)  # 创建游客实例

    def test_books_mine_read(self):
        """01）非VIP用户纠音上报"""
        records = [{
            "audio": "https:\/\/qiniucdn.jiliguala.com\/fatggr\/user_audio\/V000043\/bdb7a8045dad4ba8bad1087f55c8c384\/1664335540.mp3",
            "score": 100,
            "wordId": "V000043"
        }]
        resp = self.guest.api_words_progress('AfterLessonCorrect', records)
        assert resp['code'] == 0
        assert resp['data']['wordsStudyInfo'][0]['wordId'] == 'V000043'
        assert resp['data']['wordsStudyInfo'][0]['isCollected'] == True
        assert resp['data']['wordsStudyInfo'][0]['notMastered'] == False
