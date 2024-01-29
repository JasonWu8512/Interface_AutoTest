# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2021/8/04 1:16 下午
@Author   : Anna
@File     : ApiOrder.py
"""
from business.common.UserProperty import UserProperty
from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiOrder():
    """
    魔石商城--兑换商品
    """

    def __init__(self, token, version):
        self.host = Domains.config.get('url')
        self.root = '/api/magika'
        self.headers = {
            "authorization": token, "Content-Type": "application/json",
            "X-APP-Version": version
        }

    def api_put_order(self, source, goodsID, addressCity, addressDistrict, addressProvince, addressStreet, items,
                      magikaNum,
                      magikaPrice, mobile, recipient, shipping):
        """
        兑换魔石商品
        :param source:城市
        :param goodsID：街道
        :param addressCity:城市
        :param addressDistrict：街道
        :param addressProvince：省份
        :param addressStreet：详细地址
        :param magikaNum:魔石数量
        :param items:商品数量+id
        :param magikaPrice:魔石抵扣金额
        :param mobile:收件人手机号
        :param recipient:收件人
        :param shipping:在售
        :return：
        """
        api_url = f"{self.host}{self.root}/order"
        body = {
            "source": source,
            "goodsID": goodsID,
            "addressCity": addressCity,
            "addressDistrict": addressDistrict,
            "addressProvince": addressProvince,
            "addressStreet": addressStreet,
            "items": items,
            "magikaNum": magikaNum,
            "magikaPrice": magikaPrice,
            "mobile": mobile,
            "recipient": recipient,
            "shipping": shipping
        }
        resp = send_api_request(url=api_url, method="put", headers=self.headers, paramType="json", paramData=body)
        return resp


if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path("fat")
    user = UserProperty("19393123455")
    token = user.basic_auth
    version = config['version']['ver11.6']
    order = ApiOrder(token, version)

    # 兑换商品
    resp = order.api_put_order("ParentCenterEntry", "MG_goods_012_SPU", "北京市", "东城区", "北京市", "测试订单地址", [{
        "amount": 1,
        "id": 2561
    }], "3000", "3000", "19696969696", "tester", "true")
    print(resp)
