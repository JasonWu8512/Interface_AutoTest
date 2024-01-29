# coding=utf-8
# @Time    : 2020/11/20 4:56 下午
# @Author  : jerry
# @File    : Info.py

from dateutil import parser


class Info:
    # 9.9订单基础信息，用于预置九块九订单
    pingxxorder_basic = {
        "_id": "C90700",
        "amount": 990,
        "cts": parser.parse("2020-11-17T03:40:33.890Z"),
        "quantity": 1,
        "subject": "9.9限定装（钻石）Lv0",
        "guaid": "1488269",
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN",
        "welfare": "false",
        "ttl": "9.9限定装（钻石）Lv0",
        "promoter_openid": "oryICv86sXsULLnC15QUH8OfjD-c",
        "itemid": "H5_Sample_DiamondActivity_Lv0",
        "uid": "19debdd57bfa4b418b589a105b5607fa",
        "total": None,
        "shipping": "包邮",
        "sharer": "e7d170b9943440cfba38718ab0d8f0fa",
        "xshareInitiator": "e7d170b9943440cfba38718ab0d8f0fa",
        "gateWay": "h5",
        "thmb": "https://qiniucdn.jiliguala.com/icon/small_bird_icon.jpg",
        "status": "needaddress",
        "xshareId": "H5_Sample_DiamondActivity_Lv0",
        "channel": "wx_pub",
        "chargeid": "ch_101201117430423930880006",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN",
        "pts": parser.parse("2020-11-17T03:40:40.223Z"),
        "xsharePromoter": "e7d170b9943440cfba38718ab0d8f0fa"
    }

    def update_pingxxorder_basic(self, proUId, uid):
        """修改9.9订单信息"""
        self.pingxxorder_basic['_id'] = 'C91803'
        self.pingxxorder_basic['sharer'] = proUId
        self.pingxxorder_basic['xshareInitiator'] = proUId
        self.pingxxorder_basic['xsharePromoter'] = proUId
        self.pingxxorder_basic['uid'] = uid
        return self.pingxxorder_basic