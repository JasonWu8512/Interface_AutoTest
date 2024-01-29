# coding=utf-8
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiLexile(object):
    """
    赠送vip
    """
    def __init__(self, token):
        self.headers = {"authorization": token, "version": "1", 'Content-Type': 'application/json;charset=UTF-8'}
        self.host = Domains.domain

    def api_get_lexile_home(self):
        """
        蓝思首页
        """
        api_url = "/api/lexile/home"
        body = {}
        resp = send_api_request(url=self.host + api_url, paramType="params", paramData=body, method="get",
                                headers=self.headers)
        return resp

    def api_lexile_submit(self, chanceId):
        """
        蓝思提交
        """
        api_url = "/api/lexile/submit"
        body = {
            "locatorAnswers":[
                {"id": "L44901",
                 "choice": "A",
                 "correct": True
                 },
                {"id": "L42042",
                 "choice": "D",
                 "correct": True
                },
                {"id": "L40307",
                 "choice": "C",
                 "correct": True
                },
                {"id": "L36997",
                 "choice": "C",
                 "correct": False
                }],
            "placementAnswers": [
                {"id": "L43432",
                 "choice": "A",
                 "correct": False
                },
                {"id": "L36888",
                 "choice": "A",
                 "correct": False
                },
                {"id": "L37207",
                 "choice": "A",
                 "correct": False
                },
                {"id": "L41027",
                 "choice": "A",
                 "correct": True
                },
                {"id": "L36903",
                 "choice": "A",
                 "correct": False
                }],
            "chanceId": chanceId
        }
        resp = send_api_request(url=self.host + api_url, paramType='json', paramData=body, method="put",
                                headers=self.headers)
        return resp


if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path('dev')
    dm.set_domain("https://devggr.jiliguala.com")
    mobile = '13162592038'
    user = UserProperty(mobile)
    token = user.basic_auth
    lexile = ApiLexile(token=token)
    res= lexile.api_get_lexile_home()
    # res = lexile.api_lexile_submit()
    print(res)