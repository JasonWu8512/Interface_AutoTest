# -*- coding: utf-8 -*-
"""
@Time    : 2021/2/19 10:34 上午
@Author  : Demon
@File    : DBConfigs.py
"""

from config.env.domains import Domains

"""
CONFIG_MAP = dict(
    default={
        'database': 'test',
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Test1234',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform0_dev={
        'host': '10.10.116.154',
        'port': 3306,
        'user': 'eduplatform0',
        'password': 'AB^NnAwOPlPM1eOs',
        'database': 'eduplatform0',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform1_dev={
        'host': '10.10.116.154',
        'port': 3306,
        'user': 'eduplatform1',
        'password': 'Cx^&1l7CmaXQ@*H@',
        'database': 'eduplatform1',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform1_rc={
        'host': '10.60.247.225',
        'port': 3306,
        'user': 'eduplatform1_r',
        'password': '*5OSPATff%DuPF4M',
        'database': 'eduplatform1',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform2_rc={
        'host': '10.60.247.225',
        'port': 3306,
        'user': 'eduplatform2_r',
        'password': '#j!$*VTsmdnQTQ7r',
        'database': 'eduplatform2',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform3_rc={
        'host': '10.60.247.225',
        'port': 3306,
        'user': 'eduplatform3_r',
        'password': 'O6MYS9D#ZG&b6Or&',
        'database': 'eduplatform3',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform4_rc={
        'host': '10.60.247.225',
        'port': 3306,
        'user': 'eduplatform4_r',
        'password': '&k8Np%AbNcxBv8&Y',
        'database': 'eduplatform4',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform5_rc={
        'host': '10.60.70.177',
        'port': 3306,
        'user': 'eduplatform5_r',
        'password': 'S#q5V13RN9Ly^T4z',
        'database': 'eduplatform5',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform6_rc={
        'host': '10.60.70.177',
        'port': 3306,
        'user': 'eduplatform6_r',
        'password': 'V%UW%CCPyCN5VNTP',
        'database': 'eduplatform6',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform7_rc={
        'host': '10.60.70.177',
        'port': 3306,
        'user': 'eduplatform7_r',
        'password': 'e^B5X%uZLqyZ2kZQ',
        'database': 'eduplatform7',
        'max_connections': 20,
        'stale_timeout': None
    },
    eduplatform8_rc={
        'host': '10.60.70.177',
        'port': 3306,
        'user': 'eduplatform8_r',
        'password': 'u2aAo88&g4iCOjfy',
        'database': 'eduplatform8',
        'max_connections': 20,
        'stale_timeout': None
    },
    tirion_test={
        'host': '10.50.109.175',
        'port': 3306,
        'user': 'tirion',
        'password': 'h4vvjdk8nKU3$KYV',
        'database': 'tirion',
        'max_connections': 20,
        'stale_timeout': None
    },
    crm_prod_readonly={
        'host': '10.60.248.21',
        'port': 3306,
        'user': 'readonly',
        'password': '2GTfq8fPQEdXEWZS',
        'database': 'tirion',
        'max_connections': 20,
        'stale_timeout': None
    },
    xelephant_dev={
        'host': '10.60.248.21',
        'port': 3306,
        'user': 'readonly',
        'password': '2GTfq8fPQEdXEWZS',
        'database': 'tirion',
        'max_connections': 20,
        'stale_timeout': None
    }
    
)
"""
CONFIG_MAP = dict(
    jlgg_fat={'host': '10.161.112.11', 'port': 3306, 'user': 'user', 'password': 'jkP0*2u#zdYXvcD7'},
    crm_fat={'host': '10.161.112.11', 'port': 3306, 'user': 'leads_assign', 'password': '29vkZE983M2M5g92'},
    crm_prod={'host': '10.161.112.11', 'port': 3306, 'user': 'leads_assign', 'password': '29vkZE983M2M5g92'},
    default_dev={'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'Test1234'},
    # 课程中台
    eduplatform0_dev={'host': '10.10.116.154', 'port': 3306, 'user': 'eduplatform0', 'password': 'AB^NnAwOPlPM1eOs'},
    eduplatform1_dev={'host': '10.10.116.154', 'port': 3306, 'user': 'eduplatform1', 'password': 'Cx^&1l7CmaXQ@*H@'},
    eduplatform0_fat={'host': 'eduplatform.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eduplatform0',
                      'password': 'N0HvMFSO%yu&LTRf'},
    eduplatform1_fat={'host': 'eduplatform.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eduplatform1',
                      'password': 'iCUsBQGw#5cdh2eg'},

    eduplatform1_rc={'host': '10.60.247.225', 'port': 3306, 'user': 'eduplatform1_r', 'password': '*5OSPATff%DuPF4M'},
    eduplatform2_rc={'host': '10.60.247.225', 'port': 3306, 'user': 'eduplatform2_r', 'password': '#j!$*VTsmdnQTQ7r'},
    eduplatform3_rc={'host': '10.60.247.225', 'port': 3306, 'user': 'eduplatform3_r', 'password': 'O6MYS9D#ZG&b6Or&'},
    eduplatform4_rc={'host': '10.60.247.225', 'port': 3306, 'user': 'eduplatform4_r', 'password': '&k8Np%AbNcxBv8&Y'},
    eduplatform5_rc={'host': '10.60.70.177', 'port': 3306, 'user': 'eduplatform5_r', 'password': 'S#q5V13RN9Ly^T4z'},
    eduplatform6_rc={'host': '10.60.70.177', 'port': 3306, 'user': 'eduplatform6_r', 'password': 'V%UW%CCPyCN5VNTP'},
    eduplatform7_rc={'host': '10.60.70.177', 'port': 3306, 'user': 'eduplatform7_r', 'password': 'e^B5X%uZLqyZ2kZQ'},
    eduplatform8_rc={'host': '10.60.70.177', 'port': 3306, 'user': 'eduplatform8_r', 'password': 'u2aAo88&g4iCOjfy'},
    tirion_test_dev={'host': '10.50.109.175', 'port': 3306, 'user': 'tirion', 'password': 'h4vvjdk8nKU3$KYV'},
    crm_prod_readonly_dev={'host': '10.60.248.21', 'port': 3306, 'user': 'readonly', 'password': '2GTfq8fPQEdXEWZS'},
    # 象数
    xelephant_dev={'host': '10.60.248.21', 'port': 3306, 'user': 'readonly', 'password': '2GTfq8fPQEdXEWZS'},
    # eshop
    eshop_fat={'host': 'eshop.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eshop', 'password': '^8#rtg0j8$VoV29f'},
    eshop_orders_fat={'host': 'eshop.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eshop_orders',
                      'password': 'g@hBAZ%aK1HJKL#7'},
    eshop_orderbiz_fat={'host': 'eshop.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eshop_orderbiz',
                        'password': '@IvSWrz^3&MZRgPE'},
    eshop_biz_fat={'host': 'eshop.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'eshop_biz',
                   'password': 'qbz1*dTz%7c*qlox'},
    eshop_promotion_fat={'host': 'eshop.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'promotion',
                         'password': 'I0!jOF7fimgRnA9b'},
    trade_account_fat={'host': 'trade-account.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'trade_account',
                       'password': 'G*nKz#FgPqhv6ubw'},
    trade_settlement_fat={'host': 'trade-settlement.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'settlement',
                          'password': 'FotMgW84^dVXsmAf'},
    # crm 规划师
    crm_jaina_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'jaina', 'password': 'tkk*H$mNJcvb82Qr'},
    crm_jaina_dev={'host': '10.50.112.178', 'port': 3306, 'user': 'test', 'password': 'testtest'},
    # crm 班主任
    crm_thrall_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'thrall',
                    'password': 'ktG^P!qi!hq#hg6D'},
    # crm 班主任C端库
    crm_leads_assign_fat={'host': 'crm_leads_assign.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'crm_leads_assign',
                          'password': 'Sj@XfQCY!M^x5ZPZ'},
    # crm 公共库，
    crm_alliance_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'alliance',
                      'password': 'lJF8VhVDOpgjS4@k'},
    # crm 课程中台B端库
    crm_tirion_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'tirion',
                    'password': 'h4vvjdk8nKU3$KYV'},
    # crm 标注库
    crm_elune_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'elune', 'password': 'Y1jXH5nNMV$wynG3'},
    # crm 客服库
    crm_mergo_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'mergo', 'password': 'SSu%ni0dBD0&cFTy'},
    # crm 推广人库
    crm_zarya_fat={'host': 'crm.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'zarya', 'password': 'eC!1E9Q$8gSZ3gG8'},
    # 下沉 数据库
    saturn_dev={'host': '10.10.116.154', 'port': 3306, 'user': 'omo_saturn', 'password': 'cpuZ7v3dEPK$I^ML'},
    saturn_fat={'host': 'omo.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'u_ygritte', 'password': '1qaz@WSX'},
    # jlgl用户分流服务 数据库
    user_strategy_fat={'host': 'user_strategy.fat.mysql.jlgltech.com', 'port': 3306, 'user': 'user_strategy',
                   'password': 'bXH#5EY#*5O3*3Fo'},
    # zero 数据库
    zero_fat={'host': 'jira.mysql.jlgltech.com', 'port': 3306, 'user': 'root', 'password': '123456'},
)

if __name__ == '__main__':
    print(Domains.Env)
    Domains.set_env_path('dev')
    print(Domains.set_env_path('dev'))
