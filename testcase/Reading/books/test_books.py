# coding=utf-8
import pytest
import pytest_check as check

from business.Reading.user.ApiUser import ApiUser
from config.env.domains import Domains
from business.Reading.books.ApiBooks import ApiBooks


@pytest.mark.reg
class TestBooks(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path()
        # 设置域名host
        cls.dm.set_domain(cls.config['reading_url'])
        cls.account = cls.config["reading_account"]
        cls.user = ApiUser()
        cls.token = cls.user.get_token(typ="mobile", u=cls.account["user"], p=cls.account["pwd"])
        cls.books = ApiBooks(token=cls.token)

    def test_get_books_word_success(self):
        resp = self.books.api_get_books_word(book_id="B9780007186488")
        check.equal(resp["code"], 0)
        words = resp['data']['words']
        check.greater(len(words), 0)