# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 5:35 下午
# @Author  : zoey
# @File    : businessEnums.py
# @Software: PyCharm

from utils.enums.jlgl_enum import ChineseEnum, ChineseTuple


class EshopAdminEnum(ChineseEnum):
    PROCESSING = ChineseTuple(('processing', "进行中"))
    PENDING = ChineseTuple(('pending', "未开始"))
    FINISHED = ChineseTuple(('finished', '已结束'))
    ALL = ChineseTuple(('all', "进行中,未开始,已结束"))


class ChannelEnum(ChineseEnum):
    WECHAT_MINI_GROUP = ChineseTuple(('wechat_mini_group', '微信小程序假拼团'))
    WECHAT_MINI = ChineseTuple(('wechat_mini', '微信小程序'))
    WECHAT_WEB = ChineseTuple(('wechat_web', '微信H5商城'))
    UNWECHAT = ChineseTuple(('unwechat', '非微信渠道'))


class EshopItemPromoterEnum(ChineseEnum):
    Jerry_ST_K3_0 = ChineseTuple(('Jerry_ST_K3_0', 0.4))
    CRM_H5_ReadingVIPLifetime_0 = ChineseTuple(('CRM_H5_ReadingVIPLifetime_0', 1.5))
    K3GE_SPU = ChineseTuple(('K3GE_SPU', 1))
    CRM_H5_BundleCDS002_SPU = ChineseTuple(('CRM_H5_BundleCDS002_SPU', 0.5))
    CC_ST_K1_6_5 = ChineseTuple(('CC_ST_K1_6_5', 0))
    AutomationTest_K1MA_SPU = ChineseTuple(('AutomationTest_K1MA_SPU', 0.4))
    K1MA_SPU_TGR = ChineseTuple(('K1MA_SPU_TGR', 1))


class EshopItemPartnerEnum(ChineseEnum):
    Jerry_ST_K3_0 = ChineseTuple(('Jerry_ST_K3_0', 0.4))
    CRM_H5_ReadingVIPLifetime_0 = ChineseTuple(('CRM_H5_ReadingVIPLifetime_0', 1))
    K3GE_SPU = ChineseTuple(('K3GE_SPU', 1))
    CRM_H5_BundleCDS002_SPU = ChineseTuple(('CRM_H5_BundleCDS002_SPU', 0.5))
    CC_ST_K1_6_5 = ChineseTuple(('CC_ST_K1_6_5', 0))
    AutomationTest_K1MA_SPU = ChineseTuple(('AutomationTest_K1MA_SPU', 0.4))
    K1MA_SPU_TGR = ChineseTuple(('K1MA_SPU_TGR', 1))


class EshopLevelEnum(ChineseEnum):
    partner = ChineseTuple(('partner', 0.3))
    promoter = ChineseTuple(('promoter', 0.2))


class PromoterOperationEnum(ChineseEnum):
    delete_promoter = ChineseTuple(('删除推广人信息', 'delete_promoter'))
    delelte_promoter_wechat = ChineseTuple(('删除微信绑定与首次登录记录', 'delelte_promoter_wechat'))
    delete_fan_purchase_record = ChineseTuple(('删除粉丝购买的课程记录', 'delete_fan_purchase_record'))
    update_promoter = ChineseTuple(('修改推广人信息', 'update_promoter'))
    delete_pingxxorder_and_ghs = ChineseTuple(('删除订单与规划师', 'delete_pingxxorder_and_ghs'))
    update_promoter_xshare_fans_expirets = ChineseTuple(('修改锁粉日期', 'update_promoter_xshare_fans_expirets'))
    delete_promoter_xshare_fans = ChineseTuple(('删除锁粉信息', 'delete_promoter_xshare_fans'))

class EshopCommodityStorageTypeEnum(ChineseEnum):
    type_a = ChineseTuple((1, 1))
    type_b = ChineseTuple((2, 2))

class EshopCommodityStorageStateEnum(ChineseEnum):
    state_a = ChineseTuple((0, 0))
    state_b = ChineseTuple((1, 1))
    state_c = ChineseTuple((2, 2))
    state_d = ChineseTuple((3, 3))

class EshopOrderStateEnum(ChineseEnum):
    order_state_a = ChineseTuple((1, 1))
    order_state_b = ChineseTuple((2, 2))
    order_state_c = ChineseTuple((3, 3))
    order_state_d = ChineseTuple((4, 4))
    order_state_e = ChineseTuple((5, 5))
    order_state_f = ChineseTuple((6, 6))

class EshopRedeemStateEnum(ChineseEnum):
    redeem_state_a = ChineseTuple((1, 1))
    redeem_state_b = ChineseTuple((2, 2))
    redeem_state_c = ChineseTuple((3, 3))

def get_enum():
    chinese = ChannelEnum.get_chinese('wechat_mini_group')
    print(chinese, ChannelEnum.WECHAT_MINI_GROUP.original_value.value, ChannelEnum.WECHAT_MINI_GROUP.value)


if __name__ == '__main__':
    lis = {}
    for item in EshopLevelEnum:
        lis.update({item.value: item.chinese})
    print(lis)

