# coding=utf-8
# @Time    : 2022/7/18 6:15 下午
# @Author  : Karen
# @File    : test_shopping.py


import pytest
from business.goldenTouch.pay.ApiShopping import ApiShopping
from config.env.domains import Domains
from business.common.UserProperty import UserProperty


@pytest.mark.goldenTouch
class TestShopping(object):
    dm = Domains()

    @classmethod
    def setup_class(cls):
        # 获取环境配置
        cls.config = cls.dm.set_env_path('fat')
        # 设置域名host
        cls.dm.set_domain(cls.config['url'])

        cls.notBuy_user = ApiShopping(token=UserProperty(cls.config['goldenTouch']['notBuy_user']).basic_auth) # 13888888885 未购买用户
        cls.st99_user = ApiShopping(token=UserProperty(cls.config['goldenTouch']['st99_user']).basic_auth) # 18600000000 已购实体9.9用户


    def test_STEnglish_TC_99_purchaseView(self):
        """01 请求实体9.9购买页"""
        resp = self.notBuy_user.api_goldentouch_shopping_newViewpage('STEnglish_SPU_detry')
        assert resp['code'] == 0
        assert resp['data'][0]['title'] == '呱呱英语启蒙体验版'
        assert resp['data'][0]['sguId'] == 'STEnglish_TC_99_SGU'


    def test_STEnglish_K1K4_purchaseView(self):
        """02 请求实体大课包（k1-k4）购买页"""
        resp = self.notBuy_user.api_goldentouch_shopping_newViewpage('STEnglish_SPU_K1-K4')
        assert resp['code'] == 0
        assert resp['data'][0]['title'] == '呱呱英语家庭启蒙-无忧版 '
        assert resp['data'][0]['sguId'] == 'STEnglish_SGU_K1-K4'


    def test_STEnglish_TC_99_shoppingDetail(self):
        """03 请求实体9.9购买详情页"""
        resp = self.notBuy_user.api_goldentouch_shopping_newLessonDetail('STEnglish_SPU_detry')
        assert resp['code'] == 0
        assert resp['data'][0]['title'] == '呱呱英语启蒙体验版'
        assert resp['data'][0]['skuDetailList'][0]['title'] == '9.9英语Lv1 教具'
        assert resp['data'][0]['skuDetailList'][1]['title'] == '实体英语9.9资源'


    def test_STEnglish_SPU_K1K4_shoppingDetail(self):
        """04 请求实体大课包（k1-k4)购买详情页"""
        resp = self.notBuy_user.api_goldentouch_shopping_newLessonDetail('STEnglish_SPU_K1-K4')
        assert resp['code'] == 0
        assert resp['data'][0]['title'] == '呱呱英语家庭启蒙-无忧版 '
        assert len(resp['data'][0]['skuDetailList']) == 10


    def test_st99_user_addAdvisor(self):
        """05 已购买用户：购买流程-添加班主任"""
        resp = self.st99_user.api_goldentouch_shopping_addAdvisor('entity_eng')
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['entity_eng']['classStartTime'] != None
        assert resp['data']['entity_eng']['name'] != None
        assert resp['data']['entity_eng']['qrCode'] != None


    def test_notBuy_user_addAdvisor(self):
        """06 未购买用户：添加班主任"""
        resp = self.notBuy_user.api_goldentouch_shopping_addAdvisor('entity_eng')
        assert resp['code'] == 0
        assert resp['data'] == {}


    def test_st99_user_updateAddress(self):
        """07 已购买用户填写收货地址"""
        resp = self.st99_user.api_goldentouch_shopping_updateAddress(
            orderNo='O221786915923709952',
            addressCity="上海市",
	        addressDistrict="长宁区",
	        addressProvince="上海市",
	        addressStreet="测试订单不要发货",
	        mobile="13816435634",
	        recipient="Karen")
        assert resp['code'] == 0


    def test_shopping_purchase(self):
        """08 未购买用户创建订单"""
        resp = self.notBuy_user.api_goldentouch_shopping_purchase('PROGRAM','NA', 'wx_lite', 'STEnglish_TC_99_SGU', 'oGoLP5cCodb8Q3lFSkElelsAhYUE', physical=False)
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['subject'] == '呱呱英语启蒙体验版'
        assert resp['data']['order_no'] != None


    def test_shopping_purchase_alreadybuy(self):
        """09 已购买用户不可创建订单"""
        resp = self.st99_user.api_goldentouch_shopping_purchase('PROGRAM','NA', 'wx_lite', 'STEnglish_TC_99_SGU', 'oGoLP5cCodb8Q3lFSkElelsAhYUE', physical=False)
        print(resp)
        assert resp['code'] == 175
        assert resp['msg'] == '您已购买过本商品,请勿重复购买'
