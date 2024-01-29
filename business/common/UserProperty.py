# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 4:19 下午
# @Author  : zoey
# @File    : UserProperty.py
# @Software: PyCharm
import pymysql
import lazy_property

from config.env.domains import Domains
from utils.middleware.mongoLib import MongoClient
from lazy_property import LazyProperty
import base64
from utils.format.format import encrypt, dateToTimeStamp
from utils.decorators import switch_db


class UserProperty:
    mobile = None
    email = None
    dm = Domains()
    serverType = "userinfo"

    def __init__(self, mobile: object, unionid: object = None,email: object=None) -> object:
    # def __init__(self, mobile: object, unionid: object = None) -> object:
        self.mobile = mobile
        self.user = self.get_jlgl_user()
        self.unionid = unionid
        self.email = email
        self.config = self.dm.set_env_path(env="fat")
        self.eshop_appid = Domains.config.get('eshop_app')  # 商城购买页公众号的appid
        self.pingpp_appid = Domains.config.get('pingpp_app')
        self.promoter_appid = Domains.config.get('promoter_app')  # 新推广人公众号的appid

    @switch_db('jlgl')
    def get_jlgl_user(self):
        with MongoClient("JLGL", "users") as client:
            return client.find_one({"mobile": self.mobile})

    @switch_db('jlgg')
    def get_jlgg_user(self):
        with pymysql("JLGG","inter_user") as client:
            return client.find_one({"email":self.email})

    @switch_db ( 'jlgg' )
    def get_jlgg_user(self):
        with pymysql ( "JLGG", "inter_user" ) as client:
            return client.find_one ( {"phone": self.phone} )

    @switch_db('jlgl')
    def get_jlgl_openuser(self):
        with MongoClient("JLGL", "openuser") as client:
            return client.find_one({"mobile": self.mobile})
    @switch_db('jlgl')
    def get_jlgl_wc_users(self):
        with MongoClient("JLGL", "wc_users") as client:
            return client.find_one({"uid": self.user_id})

    @switch_db('jlgl')
    def get_jlgl_wc_openusers(self):
        with MongoClient("JLGL", "wc_openusers") as client:
            return client.find_one({"appId": self.eshop_appid, "unionId": self.wc_users_unionId})

    @switch_db('jlgl')
    def get_jlgl_babies(self):
        """通过父母的uid获取babyid"""
        with MongoClient("JLGL", "babies") as client:
            return list(client.find({"prt": self.user_id}, {'field1': 1}).sort([('cts', -1)]).limit(1))

    @switch_db('jlgl')
    def get_jlgl_wc_openusers_byPingppAppid(self):
        with MongoClient("JLGL", "wc_openusers") as client:
            return client.find_one({"appId": self.pingpp_appid, "unionId": self.wc_users_unionId})

    def get_jlgl_bindwechat_byUnionId(self):
        with MongoClient("JLGL", "bindwechat") as client:
            return client.find_one({"unionid": self.unionid})

    @switch_db('jlgl')
    def get_jlgl_wc_openusers_byPromoterAppid(self):
        with MongoClient("JLGL", "wc_openusers") as client:
            return client.find_one({"appId": self.promoter_appid, "unionId": self.wc_users_unionId})

    # @LazyProperty
    # def user(self):
    #     return self.get_jlgl_user()

    @LazyProperty
    def openuser(self):
        return self.get_jlgl_openuser()

    @LazyProperty
    def wc_users(self):
        return self.get_jlgl_wc_users()

    @LazyProperty
    def babies(self):
        return self.get_jlgl_babies()[0]

    @LazyProperty
    def wc_openusers(self):
        return self.get_jlgl_wc_openusers()

    @LazyProperty
    def wc_openusers2(self):
        return self.get_jlgl_wc_openusers_byPingppAppid()

    @LazyProperty
    def bindwechat(self):
        return self.get_jlgl_bindwechat_byUnionId()

    @LazyProperty
    def wc_openusers_by_promoter(self):
        return self.get_jlgl_wc_openusers_byPromoterAppid()

    @LazyProperty
    def openuser_sp99(self):
        return self.openuser.get("sp99")

    @LazyProperty
    def user_id(self):
        return self.user.get("_id")

    @LazyProperty
    def inter_user_email(self):
        return self.inter_user.get("email")


    @LazyProperty
    def user_mobile(self):
        return self.user.get("mobile")

    @LazyProperty
    def user_guaid(self):
        return self.user.get("guaid")

    @LazyProperty
    def user_tok(self):
        return self.user.get("tok")

    @LazyProperty
    def user_u(self):
        return self.user.get("u")

    @LazyProperty
    def user_p(self):
        return self.user.get("p")

    @LazyProperty
    def openuser_id(self):
        return self.openuser.get("_id")

    @LazyProperty
    def openuser_uid(self):
        return self.openuser.get("uid")

    @LazyProperty
    def sp99_openid(self):
        return self.openuser_sp99.get("openid")

    @LazyProperty
    def sp99_token(self):
        return "Token"+" "+self.openuser_sp99.get("token")

    @LazyProperty
    def sp99_appid(self):
        return self.openuser_sp99.get("watermark")["appid"]

    @LazyProperty
    def wc_users_nick(self):
        return self.wc_users.get("nick")

    @LazyProperty
    def wc_users_ava(self):
        return self.wc_users.get("ava")

    @LazyProperty
    def wc_users_unionId(self):
        return self.wc_users.get("unionId")

    @LazyProperty
    def wc_openusers_openId(self):
        return self.wc_openusers.get("openId")

    @LazyProperty
    def wc_openusers2_openId(self):
        return self.wc_openusers2.get("openId")

    @LazyProperty
    def wc_openusers_by_promoter_openId(self):
        return self.wc_openusers_by_promoter.get("openId")

    @LazyProperty
    def babies_id(self):
        return self.babies.get("_id")

    @LazyProperty
    def basic_auth(self):
        code = base64.b64encode(f'{self.user_id}:{self.user_tok}'.encode('utf-8'))
        print(self.user_id)
        return 'Basic ' + str(code, encoding="utf-8")

    @LazyProperty
    def bindwechat_nick(self):
        return self.bindwechat.get("nick")

    @LazyProperty
    def bindwechat_ava(self):
        return self.bindwechat.get("ava")

    @LazyProperty
    def bindwechat_openid(self):
        return self.bindwechat.get("openid")

    @LazyProperty
    def bindwechat_unionid(self):
        return self.bindwechat.get("unionid")

    @LazyProperty
    def encryptWechatToken(self):
        """获取微信鉴权需要的wechattoken"""
        dt = dateToTimeStamp(hour=2)
        info = []
        info.append(self.wc_openusers_openId)
        info.append(self.eshop_appid)
        info.append(self.serverType)
        info.append(str(int(dt)))
        info.append(self.wc_users_unionId)
        info.append(self.wc_users_nick)
        info.append(self.wc_users_ava)
        rawToken = "|".join(info)
        wechattoken = encrypt(rawToken)
        return str(wechattoken, encoding='utf-8')

    @LazyProperty
    def encryptWechatToken_pingpp(self):
        """获取微信鉴权需要的wechattoken,appid不同"""
        dt = dateToTimeStamp(hour=2)
        info = []
        info.append(self.wc_openusers2_openId)
        info.append(self.pingpp_appid)
        info.append(self.serverType)
        info.append(str(int(dt)))
        info.append(self.wc_users_unionId)
        info.append(self.wc_users_nick)
        info.append(self.wc_users_ava)
        rawToken = "|".join(info)
        wechattoken = encrypt(rawToken)
        return str(wechattoken, encoding='utf-8')

    @LazyProperty
    def encryptWechatToken_bindwechat(self):
        """获取微信鉴权需要的wechattoken,appid不同"""
        dt = dateToTimeStamp(hour=2)
        info = []
        info.append(self.bindwechat_openid)
        info.append(self.pingpp_appid)
        info.append(self.serverType)
        info.append(str(int(dt)))
        info.append(self.bindwechat_unionid)
        info.append(self.bindwechat_nick)
        info.append(self.bindwechat_ava)
        rawToken = "|".join(info)
        wechattoken = encrypt(rawToken)
        return str(wechattoken, encoding='utf-8')

    @LazyProperty
    def encryptWechatToken_promoter(self):
        """获取微信鉴权需要的wechattoken"""
        dt = dateToTimeStamp(hour=2)
        info = []
        info.append(self.wc_openusers_by_promoter_openId)
        info.append(self.promoter_appid)
        info.append("unsilent")
        info.append(str(int(dt)))
        info.append(self.wc_users_unionId)
        info.append(self.wc_users_nick)
        info.append(self.wc_users_ava)
        rawToken = "|".join(info)
        wechattoken = encrypt(rawToken)
        return str(wechattoken, encoding='utf-8')

if __name__ == '__main__':
    dm = Domains()
    dm.set_env_path('dev')
    dm.set_domain("https://dev.jiliguala.com")
    user = UserProperty("18900000314", "o0QSN1SyE6JzjNG735dhzIDNqqGw")