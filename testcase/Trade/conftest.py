# -*- coding: utf-8 -*-
# @Time: 2021/6/18 8:07 下午
# @Author: ian.zhou
# @File: conftest
# @Software: PyCharm


from business.Jiliguala.operationAdmin.ApiAuth import ApiAdminAuth, Domains
from testcase.Trade.common import CommodityCommon
from business.mysqlQuery import EshopQuery
from business.businessQuery import xshareQuery
from business.zero.mock.ApiMock import ApiMock
import time
import pytest


# @pytest.fixture(scope='session', autouse=True)
# def mock_toggle():
#     """开关mock"""
#     config = Domains.set_env_path('fat')
#     mock = ApiMock()
#     # 开启mock
#     mock.api_update_mock_status(status=True, env=config['env'], server_list=['交易中台'],
#                                 user_email='jerry_zhu@jiliguala.com')
#     time.sleep(120)
#     yield
#     # 关闭mock
#     mock.api_update_mock_status(status=False, env=config['env'], server_list=['交易中台'],
#                                 user_email='jerry_zhu@jiliguala.com')


# @pytest.fixture(scope='session', autouse=True)
# def get_commodity():
#     """获取商品、活动"""
#     config = Domains.set_env_path('fat')
#     Domains.set_domain(config['url'])
#     # 获取管理后台用户token
#     a_user = config['eshop']['admin']['user']
#     a_pwd = config['eshop']['admin']['pwd']
#     a_token = ApiAdminAuth().api_login(username=a_user, password=a_pwd).get('data').get('token')
#     xshare_query, eshop_query = xshareQuery(), EshopQuery()
#     commodity_common = CommodityCommon(a_token=a_token)
#     # 新建一个英语正价课SGU商品
#     sgu_ge = commodity_common.create_sgu(1, ['K1GE_SKU'])
#     # 新建一个思维正价课SGU商品
#     sgu_ma = commodity_common.create_sgu(3, ['K1MA'])
#     # 新建一个英语教具SGU商品
#     sgu_ge_phy = commodity_common.create_sgu(1, ['PHYSICAL_SKU_241'])
#     # 新建一个思维教具SGU商品
#     sgu_ma_phy = commodity_common.create_sgu(3, ['PHYSICAL_SKU_373'])
#     # 新建一个英语双月课SGU商品
#     sgu_ge_six_weeks = commodity_common.create_sgu(1, ['S1GE_W1-6_SKU'])
#     # 新建一个包含上述SGU的SPU
#     spu = commodity_common.create_spu([sgu_ge[1], sgu_ma[1], sgu_ge_phy[1], sgu_ma_phy[1], sgu_ge_six_weeks[1]])
#     # 用上述SPU新建一个真拼团活动
#     pro_real_id = commodity_common.create_promotion(spu_no=spu[1], auto_complete=False)
#     # 用上述SPU新建一个假拼团活动
#     pro_fake_id = commodity_common.create_promotion(spu_no=spu[1])
#     result = {
#         'sgu_system': {
#             'ge': {
#                 'id': sgu_ge[0],
#                 'no': sgu_ge[1]
#             },
#             'ma': {
#                 'id': sgu_ma[0],
#                 'no': sgu_ma[1]
#             }
#         },
#         'sgu_phy': {
#             'ge': {
#                 'id': sgu_ge_phy[0],
#                 'no': sgu_ge_phy[1]
#             },
#             'ma': {
#                 'id': sgu_ma_phy[0],
#                 'no': sgu_ma_phy[1]
#             }
#         },
#         'sgu_trial': {
#             'ge': {
#                 'no': 'K1GETC_99'
#             },
#             'ma': {
#                 'no': 'K1MATC_99'
#             },
#             'ge_ma': {
#                 'no': 'K1GETC_K1MATC_99'
#             }
#         },
#         'sgu_six_weeks': {
#             'ge': {
#                 'id': sgu_ge_six_weeks[0],
#                 'no': sgu_ge_six_weeks[1]
#             }
#         },
#         'spu': {
#             'id': spu[0],
#             'no': spu[1]
#         },
#         'promotion': {
#             'real_id': pro_real_id,
#             'fake_id': pro_fake_id
#         }
#     }
#     yield result
#     sxu_ids = [result['sgu_system']['ge']['id'], result['sgu_system']['ma']['id'], result['sgu_phy']['ge']['id'],
#                result['sgu_phy']['ma']['id'], result['sgu_six_weeks']['ge']['id'], result['spu']['id']]
#     # 删除新建的SXU
#     for sxu_id in sxu_ids:
#         eshop_query.delete_sxu_record(sxu_id=sxu_id)
#     # 删除新建的拼团活动
#     eshop_query.delete_promotion_record(promotion_id=result['promotion']['real_id'])
#     eshop_query.delete_promotion_record(promotion_id=result['promotion']['fake_id'])
#     # 删除真拼团活动关联的团
#     xshare_query.delete_xshare_group_purchase(gpid=result['promotion']['real_id'])


@pytest.fixture(scope='session', autouse=True)
def get_commodity():
    """获取商品、活动"""
    Domains.set_env_path('fat')
    result = {
        'sgu_system': {
            'ge': {
                'id': 6702,
                'no': 'Trade_Automation_Test_SGU_GE'
            },
            'ma': {
                'id': 6709,
                'no': 'Trade_Automation_Test_SGU_MA'
            }
        },
        'sgu_phy': {
            'ge': {
                'id': 6710,
                'no': 'Trade_Automation_Test_SGU_GE_Phy'
            },
            'ma': {
                'id': 6711,
                'no': 'Trade_Automation_Test_SGU_MA_Phy'
            }
        },
        'sgu_trial': {
            'ge': {
                'no': 'K1GETC_99'
            },
            'ma': {
                'no': 'K1MATC_99'
            },
            'ge_ma': {
                'no': 'K1GETC_K1MATC_99'
            }
        },
        'sgu_six_weeks': {
            'ge': {
                'id': 6712,
                'no': 'Trade_Automation_Test_SGU_GE_Six'
            }
        },
        'spu': {
            'id': 8,
            'no': 'Automation-Test'
        },
        'promotion': {
            'real_id': 'DACT_1420',
            'fake_id': 'DACT_1421'
        }
    }
    return result
