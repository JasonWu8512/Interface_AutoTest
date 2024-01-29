# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/13 11:58 上午
@Author  : Demon
@File    : TestMockFlow.py
"""

import os
import yaml
import json, time
import random
import pytest
import pandas
import shortuuid
from config.env.domains import Domains
from utils.middleware.dbLib import MySQL
from business.zero.GetUserProperty import GetUserProperty
from business.zero.ApiLessonCentral.ApiLessonCentral import ApiLessonCentral
from utils.requests.apiRequests import send_api_request
from utils.date_helper import get_time_stamp, get_off_set_time, get_any_time_stamp

# 初始化字母/单词等数据
ids = {'GEKLT9197999': 23, 'GEKWP1557758': 43, 'GEKWP9362699': 102, 'GEKWP2761731': 50, 'GEKLT2875254': 9,
         'GEKWP2705421': 49, 'GEKWP7763887': 91, 'GEKLT6701544': 19, 'GEKWP2375047': 47, 'GEKWP3840378': 56,
         'GEKWP8054284': 94, 'GEKWP6892957': 83, 'GEKWP5572970': 74, 'GEKWP9870312': 108, 'GEKWP0977559': 37,
         'GEKWP5684816': 75, 'GEKWP1145898': 39, 'GEKWP4534284': 64, 'GEKWP6372595': 80, 'GEKWP3622904': 54,
         'GEKWP5858917': 76, 'GEKWP4331578': 63, 'GEKWP0816763': 35, 'GEKWP4066400': 58, 'GEKWP4801379': 66,
         'GEKWP3620499': 53, 'GEKWP0616039': 31, 'GEKLT0733201': 3, 'GEKWP0816755': 34, 'GEKWP0409996': 30,
         'GEKLT5872643': 15, 'GEKWP8517166': 98, 'GEKWP9158733': 99, 'GEKLT5244533': 14, 'GEKWP9382663': 103,
         'GEKWP8431769': 97, 'GEKWP7630648': 90, 'GEKLT2273396': 6, 'GEKWP9736641': 106, 'GEKWP1080155': 38,
         'GEKWP1344871': 41, 'GEKWP7914961': 92, 'GEKWP6312061': 79, 'GEKWP6672879': 82, 'GEKLT6397006': 18,
         'GEKWP9347940': 101, 'GEKWP0317911': 29, 'GEKLT0458721': 2, 'GEKWP6921048': 84, 'GEKWP4314785': 61,
         'GEKWP7951639': 93, 'GEKWP6671885': 81, 'GEKWP9229750': 100, 'GEKWP1362640': 42, 'GEKLT3346561': 10,
         'GEKWP7106560': 87, 'GEKWP2179185': 46, 'GEKWP8406282': 96, 'GEKLT5951404': 16, 'GEKWP0179415': 27,
         'GEKLT1255136': 4, 'GEKLT6721024': 20, 'GEKWP4317038': 62, 'GEKWP3787705': 55, 'GEKWP5990263': 77,
         'GEKWP1319055': 40, 'GEKLT8740093': 22, 'GEKLT2308503': 7, 'GEKLT8037072': 21, 'GEKWP0759164': 33,
         'GEKWP6220109': 78, 'GEKWP0128431': 25, 'GEKWP1560502': 44, 'GEKWP4068708': 59, 'GEKWP4863713': 68,
         'GEKLT1862444': 5, 'GEKWP9457639': 104, 'GEKWP2078447': 45, 'GEKLT4725996': 12, 'GEKWP5475870': 72,
         'GEKWP7066399': 86, 'GEKWP0251072': 28, 'GEKWP4715478': 65, 'GEKWP4128543': 60, 'GEKWP4810409': 67,
         'GEKWP7060644': 85, 'GEKWP2840398': 51, 'GEKLT4885132': 13, 'GEKWP9556260': 105, 'GEKLT2850818': 8,
         'GEKWP2427575': 48, 'GEKWP0886090': 36, 'GEKLT0303810': 1, 'GEKWP0648386': 32, 'GEKWP3297750': 52,
         'GEKLT4049977': 11, 'GEKLT6052757': 17, 'GEKWP5534423': 73, 'GEKWP5030618': 70, 'GEKWP0138022': 26,
         'GEKWP5202229': 71, 'GEKWP0059042': 24, 'GEKWP8156910': 95, 'GEKWP9736895': 107, 'GEKWP4957894': 69,
         'GEKWP7547219': 89, 'GEKWP3954973': 57, 'GEKWP7422051': 88}
list_id = list(ids.keys())
import requests

def knowledge_id(has_know_id):
    temp_di = random.choice(list_id)
    while temp_di in has_know_id:
        temp_di = random.choice(list_id)
    return temp_di

def api_download(bid):
    # print(json.dumps(data))
    headers = {
        'Content-Type': 'application/json'
    }
    typ = random.choice(['listen', 'speak'])
    data = "{\"bid\": \"{1}\", \"gameType\": \"{0}\"}".format(typ, bid)
    print(data)
    return requests.request(method='post',
                     url='http://fat.jiliguala.com/api/aiplayground/v1/download',
                            data=data, headers=headers, verify=False)


class TestMockFlow(object):
    dm = Domains()
    SKILL = ('GESRD7988306', 'GESLS2784867', 'GESSK5592673')
    KNOWLEDGE = ('字母', '音素', '单词/词组')
    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('rc')
        # cls.dm.set_domain(cls.config['zero_url'])
        # cls.zero = GetUserProperty()
        # cls.lesson = ApiLessonCentral(token=cls.zero.get_token)

    def index_get_date(self, index):
        '''标签数据获取事件范围/index'''
        mapping = {
            0: random.randint(1, 6),
            1: random.randint(8, 29),
            2: random.randint(31, 40)
        }
        return mapping[index // 3]

    def index_get_pre_score(self, index):
        '''标签数据获取随机分数/'''
        k1 = 80
        k2 = 60
        mapping = {
            0: random.randint(k1 + 1, 100),
            1: random.randint(k2 + 1, k1-1),
            2: random.randint(0, k2-1)
        }
        return mapping[index % 3]

    def get_skilled(self, typ='listen'):
        mapping = {
            'listen': ['GESLS2784867'],
            'speak': ['GESRD7988306', 'GESSK5592673']
        }

        return mapping[typ][0]

    def chong_pai_questions(self, score_rule, uids=None):
        """根据规则生成流水数据"""
        uid = f"test_{get_time_stamp(num=13)}" if not uids else uids
        data = {
            "code": 0,
            "requestId": "d2fc3fc876bf29c4",
            "data": []
        }
        pre_score = {
            "code": 0,
            "data": []
        }
        has_know_id = []
        for i in range(9):

            for nums in range(score_rule[i]):
                now_date = get_off_set_time(fmt='YYYY-MM-DD HH:mm:ss')
                days = -1 * self.index_get_date(index=i)

                know_id = knowledge_id(has_know_id)
                has_know_id.append(know_id)
                knowledge = {
                    "skillId": self.get_skilled(typ='listen'),
                    "sublessonId": "K1GEF00205",
                    "knowledgeId": know_id,
                    "realScore": int(random.randint(0, 100)),
                    "reviewType": random.choice(('guamei', 'playGround')),
                    "bid": uid,
                    "finishTime": get_any_time_stamp(base=now_date, days=days) * 1000,
                    "displayScore": self.index_get_pre_score(index=i),
                    "audioTag": "",
                    # "str_date": get_off_set_time(base=now_date, days=days, fmt='YYYY-MM-DD HH:mm:ss'),
                    # "index_days": days,
                    "audioUrl": ""
                    # "audioUrl": "https://qiniucdn.jiliguala.com/dev/upload/2473ec23a1544d679b491604884ed63b_20210222031147.mp3"
                }
                data['data'].append(knowledge)
                # 根据得分规则配置uid每个知识点的预测分数
                _scor = {
                    'knowledgeId': know_id,
                    'predScore': self.index_get_pre_score(index=i)
                }
                pre_score['data'].append(_scor)
        return data, pre_score

    @pytest.mark.parametrize('score_rule', ([[20,5,3,2,3,1,1,2,1]]))
    def test_re_rank_between_10_20(self, score_rule):
        # 重排知识点 N = 20
        ''' knowledge_flow_record 表格生成json
        1.完全符合规则
        '''
        bid = 'test_452324354465nm9'
        data, pre_scores = self.chong_pai_questions(score_rule, uids=bid)

        uid = data['data'][0]['bid']
        if bid[-1] in '89abcdef': # 走AI
            self.write_user_json(fp=f'uid_score_bak.json', data={uid: data})
            print('走AI pre_scores', data)
        return data

    def write_user_json(self, fp, data):
        with open(fp, 'w') as f:
            json.dump(obj=data, fp=f)

    def test_check_flow_score(self):
        flow = json.load(open('./uid_score_flow.json', 'r'))
        score = json.load(open('./uid_score.json', 'r'))
        for _ in flow:
            gua = flow[_]['data'].get('guaMei') if flow[_]['data'].get('guaMei') else []
            pla = flow[_]['data'].get('playground') if flow[_]['data'].get('playground') else []
            sss = [d['knowledgeId'] for d in gua + pla]
            score_li = [a['knowledgeId'] for a in score.get(_)['data']]
            # for d in sss:
            #     # print(score.get(_)['data'])
            #
            #     score_li = [a['knowledgeId'] for a in score.get(_)['data']]
            #     if d['knowledgeId'] not in score_li:
            #         print(_, d['knowledgeId'])
            # subsiss = set(sss).union(set(score_li)) - set(sss).intersection(set(score_li))
            subsiss = set(sss).symmetric_difference(set(score_li))
            if subsiss:
                print(subsiss)
            print(_, '***', len(sss), '*****', len(score_li))

    def test_rc_bid_has_data(self):
        #验证rc-bid是否有数据
        ''
        Domains.set_env_path('dev')
        zero_api = ApiLessonCentral(token=GetUserProperty().get_token)
        # print(zero_api.api_lesson_getNewerStudyRecordByBid(params=['074cb70136ab4e148037f2b06262e92c']).get('data').get(
        #     "guaMei"))
        # mysql = MySQL(pre_db='eduplatform3', db_name='eduplatform3')
        sql = f'select distinct bid from knowledge_record1'
        with open('./locust-uid.txt') as f:
            uids = f.read().split('\n')
        for biddata in uids:
            data = zero_api.api_lesson_getNewerStudyRecordByBid(params=[biddata]).get('data')
            if data.get('guaMei'):
                for gua in data.get('guaMei'):
                    if gua['skillId'] in self.SKILL and gua['knowledgeId'] in list_id:
                        print(gua)
                        break
                else:
                    pass
                break
