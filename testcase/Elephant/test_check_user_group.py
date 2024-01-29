
import pytest

from config.env.domains import Domains
from business.Elephant.ApiBasic.GetUserProper import GetUserProper



@pytest.mark.Elephant
class TestReport(object):
    @classmethod
    def setup_class(cls):
        cls.config = Domains.set_env_path('dev')
        cls.user = GetUserProper(user=cls.config['elephant']['user'], pwd=cls.config['elephant']['pwd'])

