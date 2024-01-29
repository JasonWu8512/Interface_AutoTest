# coding=utf-8
# @Time    : 2020/12/4 10:54 上午
# @Author  : jerry
# @File    : PromoterProperty.py
from config.env.domains import Domains
from utils.middleware.mongoLib import MongoClient
from lazy_property import LazyProperty
from utils.format.format import encrypt, dateToTimeStamp
from utils.decorators import switch_db
import base64

class PromoterProperty:
    mobile = None

    def __init__(self, mobile):
        self.mobile = mobile

    @switch_db('jlgl')
    def get_xhare_promoter_accounts(self):
        with MongoClient("XSHARE", "promoter_accounts") as client:
            return client.find_one({"mobile": self.mobile})

    @LazyProperty
    def promoter_accounts(self):
        return self.get_xhare_promoter_accounts()

    @LazyProperty
    def promoter_accounts_id(self):
        return self.promoter_accounts.get("_id")

    @LazyProperty
    def promoter_accounts_unionId(self):
        return self.promoter_accounts.get("unionId")

    @LazyProperty
    def promoter_accounts_openid(self):
        return self.promoter_accounts.get("openid")

    @LazyProperty
    def promoter_accounts_ava(self):
        return self.promoter_accounts.get("ava")

    @LazyProperty
    def promoter_accounts_nick(self):
        return self.promoter_accounts.get("nick")

    @LazyProperty
    def promoter_accounts_uid(self):
        return self.promoter_accounts.get("uid")

    @LazyProperty
    def promoter_accounts_mobile(self):
        return self.promoter_accounts.get("mobile")

    @LazyProperty
    def promoter_accounts_tok(self):
        return self.promoter_accounts.get("tok")

    @LazyProperty
    def basic_auth(self):
        code = base64.b64encode(f'{self.promoter_accounts_id}:{self.promoter_accounts_tok}'.encode('utf-8'))
        return 'Basic ' + str(code, encoding="utf-8")

    # @LazyProperty
    # def encryptWechatToken(self):
    #     """获取微信鉴权需要的wechattoken"""
    #     dt = dateToTimeStamp(hour=2)
    #     info = []
    #     info.append(self.promoter_accounts_openid)
    #     info.append(self.appid)
    #     info.append(self.serverType)
    #     info.append(str(int(dt)))
    #     info.append(self.promoter_accounts_unionId)
    #     info.append(self.promoter_accounts_nick)
    #     info.append(self.promoter_accounts_ava)
    #     rawToken = "|".join(info)
    #     wechattoken = encrypt(rawToken)
    #     return str(wechattoken, encoding='utf-8')

if __name__ == '__main__':
    dm = Domains()
    dm.set_domain("https://dev.jiliguala.com")
    promoter = PromoterProperty('13951782841')
    r = promoter.promoter_accounts
    print(r)