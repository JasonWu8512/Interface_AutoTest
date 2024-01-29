# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/4 2:38 下午
@Author  : Demon
@File    : test_temp_data.py
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
from utils.date_helper import get_time_stamp, get_off_set_time, get_any_time_stamp

import requests
def api_recall(data):
    return requests.request(method='post',
                     url='http://10.42.185.53:8083/playground/v3/recall', data=data)

def api_rank(data):
    return requests.request(method='post',
                     url='http://10.42.185.53:8083/playground/v3/rank', data=data)

def api_get_question(body):
    return requests.request(method='post',
                            url='http://10.42.103.131:51001/api/aiplayground/v1/download', json=body)

def temp_data():
    '''召回/精排接口规则'''
    rule = (
        [30, 0],
        # [10, 20], [30, 10], [0, 30], [10, 10]
        [10, 20], [30, 20], [11, 23], [10, 10]
    )
    return rule

def joney_ai_rule_data():
    '''重排规则[2, 5, 3, 2, 3, 1, 1, 2, 1]'''
    rule = (
        [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5, 3, 2, 3, 1, 1, 2, 1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5+1,3+1,2-2,3,1,1,2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5-2,3,2+1,3+1,1,1,2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5,3,2,3-2,1,1,2+2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5,3+1,2,3+1,1-1,1-1,2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5,3+3,2,3,1-1,1,2-2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5,3,2,2,1,0,4,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [2, 5,6,2,1,1,0,2,1]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [4,10,6,0,0,0,0,0,0]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [0,0,0,6,9,5,0,0,0]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [0,0,12,0,0,4,0,0,4]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [0,0,9,0,9,0,2,0,0]],
        # [[2, 5, 3, 2, 3, 1, 1, 2, 1], [0,0,0,0,0,0,5,15,0]],
    )
    return rule

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

def knowledge_id():
    return random.choice(list_id)

class TestAI(object):
    dm = Domains()
    SKILL = ('GESRD7988306', 'GESLS2784867', 'GESSK5592673')
    KNOWLEDGE = ('字母', '音素', '单词/词组')
    @classmethod
    def setup_class(cls):
        """当前类初始化执行方法"""
        cls.config = cls.dm.set_env_path('dev')
        cls.dm.set_domain(cls.config['zero_url'])
        cls.zero = GetUserProperty()
        cls.lesson = ApiLessonCentral(token=cls.zero.get_token)

    def get_record_test_recall_30_more_N(self, uid, ):
        # 获取用户历史所有流水, 游乐场/瓜美使用最新一次记录
        return '''
        select * from knowledge_flow_record0
        where id in (
            SELECT id from (
                SELECT *, ROW_NUMBER() over(PARTITION by(knowledge_id ) ORDER BY finish_time desc ) as rn
                FROM knowledge_flow_record0 
                WHERE bid= '{0}' and review_type = 'guamei'
            )s  WHERE rn = 1
        ) ;
        '''.format(uid, )

    @pytest.mark.parametrize('uid', ['51ccef0a455f437f8a51a0250a788b32', '791728ac8b7a418a97dfadefe6e41b96'])
    def test_recall_30_more_N(self, uid):
        """
        1.30天内召回超过N知识点，组合生成recall接口参数
        2.预测得分结果是否需要验证
        """
        print(uid)
        db_name = self.lesson.api_lesson_get_name(uid=uid, table='knowledge_flow_record').get('data')

        mysql = MySQL(pre_db=db_name.split('.')[0], db_name=db_name.split('.')[0])
        study_infos = mysql.query(self.get_record_test_recall_30_more_N(uid=uid))
        params = dict(bid=uid, context=[], model='dssm')
        for study in study_infos:
            params['context'].append({
                'skillId': study['skill_id'],
                'knowledgeId': study['knowledge_id'],
                'guaMei': {
                    'finishTime': study['finish_time'],
                    'displayScore': study['display_score'],
                    'realScore': study['real_score'],
                    'audioTag': study['audio_tag'],
                    'count': 0
                },
                'playGround': {
                    'finishTime': study['finish_time'],
                    'displayScore': study['display_score'],
                    'realScore': study['real_score'],
                    'audioTag': study['audio_tag'],
                    'count': 0
                },
            })
        # 验证召回流水按照预测得分从低到高排序
        # pre_data = api_recall(params).get('data')
        # assert len(pre_data) == 20
        # zsero = float('-inf')
        # for pre_score in pre_data:
        #     assert (zsero <= pre_score['pred_score']) and (100 >= pre_score['pred_score'] >= 0)
        #     zsero = pre_score['pred_score']

    @pytest.mark.parametrize('uid', ['63207c7cd23f4763a0ca8f5837609830'])
    def test_rank_infos(self, uid,):
        '''精排模型需要的用户'''
        db_name = self.lesson.api_lesson_get_name(uid=uid, table='knowledge_flow_record').get('data')

        mysql = MySQL(pre_db=db_name.split('.')[0], db_name=db_name.split('.')[0])
        study_infos = mysql.query(self.get_record_test_recall_30_more_N(uid=uid))
        params = dict(bid=uid, context=[], model='din')
        for study in study_infos:
            params['context'].append({
                'skillId': study['skill_id'],
                'knowledgeId': study['knowledge_id'],
                'domain': 'domain',
                'knowledgeTypeId': 'knowledgeTypeId',
                'guaMei': {
                    'finishTime': study['finish_time'],
                    'displayScore': study['display_score'],
                    'realScore': study['real_score'],
                    'audioTag': study['audio_tag'],
                    'count': 0
                },
                'knowledgeProperty': {},
                'playGround': {
                    'finishTime': study['finish_time'],
                    'displayScore': study['display_score'],
                    'realScore': study['real_score'],
                    'audioTag': study['audio_tag'],
                    'count': 0
                },
            })
        print(params)
        api_rank(params)

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
            0: random.randint(k1, 100),
            1: random.randint(k2, k1-1),
            2: random.randint(0, k2-1)
        }
        return mapping[index % 3]

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
        for i in range(9):
            for nums in range(score_rule[i]):
                now_date = get_off_set_time(fmt='YYYY-MM-DD HH:mm:ss')
                days = -1 * self.index_get_date(index=i)
                know_id = knowledge_id()
                knowledge = {
                    "skillId": self.get_skilled(),
                    "sublessonId": "K1GEF00205",
                    "knowledgeId": know_id,
                    "realScore": int(random.randint(0, 100)),
                    "reviewType": random.choice(('guamei', 'playGround')),
                    "bid": uid,
                    "finishTime": get_any_time_stamp(base=now_date, days=days),
                    "displayScore": int(random.randint(0, 100)),
                    "audioTag": "",
                    "str_date": get_off_set_time(base=now_date, days=days, fmt='YYYY-MM-DD HH:mm:ss'),
                    "index_days": days,
                    "audioUrl": ""
                    # "audioUrl": "https://qiniucdn.jiliguala.com/dev/upload/2473ec23a1544d679b491604884ed63b_20210222031147.mp3"
                }
                data['data'].append(knowledge)
                # 根据得分规则配置uid每个知识点的预测分数
                _scor = {
                    'knowledgeId': know_id,
                    'predScore': self.index_get_pre_score(index=i)
                }
                # print(knowledge['index_days'], _scor, )
                pre_score['data'].append(_scor)
        return data, pre_score

    @pytest.mark.parametrize('knowledge_date, score_rule', joney_ai_rule_data())
    def test_re_rank_between_10_20(self, knowledge_date, score_rule):
        # 重排知识点 N = 20
        ''' knowledge_flow_record 表格生成json
        1.完全符合规则
        '''
        print(knowledge_date, score_rule)

        data, pre_scores = self.chong_pai_questions(score_rule)
        print(data)
        print(pre_scores)
        '''
        _result = [2, 5, 3, 2, 3, 1, 1, 2, 1] # 依次取数个数
        resu_quests = []
        all_quests = pre_scores.get('data')
        for k, v in enumerate(_result):
            # if k >= len(score_rule):

            # 每个格子可供选择的题目个数，第一轮取数
            pre_quests = all_quests[sum(score_rule[:k]): sum(score_rule[:k]) + v]
            print(sum(score_rule[:k]), v, '*' * 10, pre_quests)
            order_pre_quests = sorted(pre_quests, key=lambda x: x['predScore'])
            resu_quests.extend(order_pre_quests)
        print(resu_quests)
        '''
        # 保存文件
        uid = data['data'][0]['bid']
        # self.write_user_json(fp=f'all_bid_score.json', data=dict(flow=data, score=pre_scores))
        self.write_user_json(fp=f'{uid}_ai_rule.json', data=dict(flow=data, score=pre_scores))

    def test_json_score(self):
        udi_json = filter(lambda x:x.endswith('_ai_rule.json'), os.listdir('.'))
        with open('./uid_score_flow.json', 'w') as f:
            infos = {}
            for _ in udi_json:
                pp = json.load(fp=open(f'./{_}', 'r'))
                uid = pp['flow']['data'][0]['bid']
                infos[uid] = pp['flow']
                print(pp['flow'])
            # f.write(json.dumps(infos))

    def get_0_user_id(self):
        '''获取制定库/表下的uid'''
        def get_uuid():
            uid = f'test_{get_time_stamp()}'
            data_db = self.lesson.api_lesson_get_name(uid=uid, table='knowledge_flow_record').get('data')
            if data_db.split('.')[0].endswith('0') and data_db.endswith('1'):
                print('*' * 10, data_db, uid)
                return uid
            else:
                return self.get_0_user_id()
        return get_uuid()

    @pytest.mark.parametrize('knowledge_rule', ([[2, 5, 3,2,3,1,1,2,1]]))
    def test_eduplatform0_insert_flow(self, knowledge_rule):
        '''课程中台流水 数据插入'''
        uid = self.get_0_user_id()
        data, pre_scores = self.chong_pai_questions(score_rule=knowledge_rule, uids=uid)
        print(data)
        for flow in data.get('data'):
            print(flow)
            sqls = '''INSERT INTO knowledge_flow_record1 (bid, sublesson_id, location_id, real_score, finish_time,
             create_time, update_time, `subject`, game_id, section_id, round_id,
             sentence_id, knowledge_id, skill_id, review_type, display_score)
            VALUES(
                '{uid}', '{sublesson_id}', 'b8b7c9f6a668440da', {real_score}, {finish_time},
                '{create_time}', '{update_time}', 'GE', 'L1U01W2D5Q1', 'L1XX0111sec10', '20001',
                '', '{knowledge_id}', '{skill_id}', '{review_type}', {display_score}
            );
            '''.format(**dict(uid=uid, real_score=flow['realScore'], sublesson_id=flow['sublessonId'], finish_time=flow['finishTime'],
                              create_time=flow['str_date'], update_time=flow['str_date'], knowledge_id=flow['knowledgeId'],
                              skill_id=flow['skillId'],
                              review_type=flow['reviewType'], display_score=flow['displayScore']))
            print(sqls)
            break

    @pytest.mark.parametrize('in_30,out_30', temp_data())
    def test_AI_recall_users(self, in_30, out_30):
        """recall接口所用参数 [30, 0], [10, 20], [30, 10], [0, 30], [10, 10]
        1.近30天内 30，30天外学习 0
        2.近30天内 10，30天外学习 20
        3.近30天内 30，30天外学习 10
        4.近30天内 0，30天外学习 30
        """
        print(in_30, out_30)

        uid = f"test_{get_time_stamp(num=13)}"
        data = dict(bid=uid, predId=shortuuid.uuid(), model='dssm')
        context = []
        for ins in range(in_30):
            context.append(self.generate_30_flow(index=0))
        for out_30outs in range(out_30):
            # index =1 ：第三行日期(30天之外)
            context.append(self.generate_30_flow(index=1))
        data['context'] = json.dumps(context)
        # self.write_user_json(fp=f'{uid}_recall.json', data=data, )
        api_data = api_recall(data=json.dumps(data))
        # api_data = api_rank(data=json.dumps(data))
        assert api_data.json().get('code') == 0
        assert in_30 + out_30 == len(api_data.json().get('data'))
        # print(api_data.elapsed.microseconds, api_data.elapsed.seconds)
        assert api_data.elapsed.seconds <= 2
        for kn in api_data.json().get('data'):
            assert kn.get('predScore')

    def get_skilled(self):
        return random.choice(('GESRD7988306', 'GESLS2784867', 'GESSK5592673'))

    def test_final_case(self):
        pass

    def generate_30_flow(self, index):
        # days = -1 * self.index_get_date(index=index)
        now_date = get_off_set_time(fmt='YYYY-MM-DD HH:mm:ss')
        # typ = random.choice(('guaMei', 'playGround', ['guaMei', 'playGround']))
        typ = random.choice((['guaMei', 'playGround'], ))
        knows = {
            # 'skillId': random.choice(('GESRD7988306', 'GESLS2784867')),
            # 'knowledgeId': knowledge_id()
            'skillId': self.get_skilled(),
            'knowledgeId': knowledge_id()
        }

        # print(typ)
        if isinstance(typ, list):
            for key in typ:
                days = -1 * self.index_get_date(index=random.randint(6, 8) if index == 1 else random.randint(0, 5))
                knows[key] = {
                    'displayScore': int(random.randint(0, 100)),
                    'realScore': int(random.randint(0, 100)),
                    'audioTag': '',
                    'count': 1,
                    'finishTime': get_any_time_stamp(base=now_date, days=days) * 1000,
                    # "str_date": get_off_set_time(base=now_date, days=days, fmt='YYYY-MM-DD HH:mm:ss'),
                }
            # print(knows)
        else:
            days = -1 * self.index_get_date(index=random.randint(6, 8) if index == 1 else random.randint(0, 5))
            knows[typ] = {
                'displayScore': int(random.randint(0, 100)),
                'realScore': int(random.randint(0, 100)),
                'audioTag': '',
                'count': 1,
                'finishTime': get_any_time_stamp(base=now_date, days=days),
                "str_date": get_off_set_time(base=now_date, days=days, fmt='YYYY-MM-DD HH:mm:ss'),
            }
            # knows[typ] = dict(**guamei_play, finishTime=get_any_time_stamp(base=now_date, days=days))
        return knows

    def write_user_json(self, fp, data):
        with open(fp, 'w') as f:
            json.dump(obj=data, fp=f)

    def test_isdj(self):

        print(json.load(open('./_recall.json', 'r')))
        pre_quests = [{'knowledgeId': 'GEKWP3297750', 'predScore': 71}, {'knowledgeId': 'GEKWP4715478', 'predScore': 61}]
        print(sorted(pre_quests, key=lambda x: x['predScore']))
        assert self.parse_knowledge_type(knowledge_id='GEKLT6721024') in ('字母', '音素', '单词/词组')

    def parse_knowledge_type(self, knowledge_id):
        # 解析knowledge类型
        df = pandas.read_excel('./k1.xls')
        # print(df[df['knowledge_id']==knowledge_id]['knowledge_type_text'][0])
        return df[df['knowledge_id']==knowledge_id]['knowledge_type_text'][0]

    @pytest.mark.parametrize('know_nums', [[20, 20],[11, 19],  [21, 29], [30, 30]])
    def test_get_zhishidain_num10(self, know_nums):
        # 获取表中已学知识点等于10的uid/bid  [0, 0], [1,9], [20, 20],[11, 19],  [21, 29], [30, 30], [10, 10]
        uids_ = MySQL(pre_db='eduplatform1', db_name='eduplatform1').query('SELECT DISTINCT bid from knowledge_flow_record0')
        # self.lesson.api_lesson_getNewerStudyRecordByBid(params=["uid"])
        def asert_in_skills(skill):
            return skill['skillId'] in ('GESRD7988306', 'GESLS2784867')
        f = open('./uids_know.txt', 'a')
        df = pandas.read_excel('./k1.xls')
        all_uid = set()
        for data in uids_:
            lesson_data = self.lesson.api_lesson_getNewerStudyRecordByBid(params=[data['bid']])
            # 处理每一个bid数据
            # sd = [{'knowledgeId': 'GESRD7988306', 'skillId': 'GESRD7988306', 'finishTime': 1614243951097, 'displayScore': 0, 'realScore': 0, 'count': 1, 'audioTag': ''}, {'knowledgeId': 'GEKWP4810409', 'skillId': 'GESLS7572288', 'finishTime': 1614243951097, 'displayScore': 0, 'realScore': 0, 'count': 1, 'audioTag': ''}, {'knowledgeId': 'GEKWP9736641', 'skillId': 'GESLS5083384', 'finishTime': 1614244103879, 'displayScore': 0, 'realScore': 0, 'count': 1, 'audioTag': ''}, {'knowledgeId': 'GEKWP4810409', 'skillId': 'GESLS5083384', 'finishTime': 1614244103879, 'displayScore': 0, 'realScore': 0, 'count': 1, 'audioTag': ''}]
            temp = 0
            for guamei in lesson_data.get('data').get('guaMei'):
                # 获取每一个知识点，查看是否是字母单词
                tezt = df[df['knowledge_id'] == guamei['knowledgeId']]['knowledge_type_text']
                if list(tezt.keys()):
                    if tezt[list(tezt.keys())[0]] in self.KNOWLEDGE and guamei['skillId'] in self.SKILL:
                        temp += 1
                        print(guamei['knowledgeId'], tezt[list(tezt.keys())[0]])
            if temp >= know_nums[0] and temp <= know_nums[1]:

                if data['bid'][-1] in '89abcdef':
                    f.write(f'已学知识点={temp}-{know_nums}|uid/bid={data["bid"]}|uid/bid规则：rule=AI\n')
                    all_uid.add('89abcdef')
                elif data['bid'][-1] in '01234567':
                    f.write(f'已学知识点={temp}-{know_nums}|uid/bid={data["bid"]}|uid/bid规则：rule=DD\n')
                    all_uid.add('01234567')
            if len(all_uid) >= 2:
                break
        f.close()
            # in_skill_list = list(filter(asert_in_skills, lesson_data.get('data').get('guaMei')))
            # if len(in_skill_list) == 10:
            #     print(data.get('data').get('bid'))
            #     break

    def test_single_uid_(self):
        #单个用户学习记录查询，并查看知识点类型
        uid = 'f37f702ad6064c79bbe1079283a33735'
        lesson = self.lesson.api_lesson_getNewerStudyRecordByBid(params=[uid])
        df = pandas.read_excel('./k1.xls')
        bosy = {
            "bid": lesson.get('data').get("bid"),
            "predId": 1,
            "model": "dssm"
        }
        temp = []

        for guam in lesson.get('data').get('guaMei'):

            tezt = df[df['knowledge_id'] == guam['knowledgeId']]['knowledge_type_text']
            if list(tezt.keys()):

                if tezt[list(tezt.keys())[0]] in self.KNOWLEDGE and guam.get('skillId') in self.SKILL:
                    knows = {
                        "skillId": guam.get("skillId"),
                        "knowledgeId": guam.get("knowledgeId"),
                        "guaMei": {
                            "displayScore": guam.get("displayScore"),
                            "realScore": guam.get("realScore"),
                            "audioTag": guam.get("audioTag"),
                            "count": guam.get("count"),
                            "finishTime": guam.get("finishTime"),
                        }
                    }
                    temp.append(knows)
                    temp = sorted(temp, key=lambda x: x['skillId'])
                    print(guam.get('skillId'), guam.get('knowledgeId'), tezt[list(tezt.keys())[0]])
                    print(knows)
        bosy['context'] = json.dumps(temp)
        print(json.dumps(bosy))

    def lesson_filter_skill_know(self, uid):
        # 课程中台过滤skill和knowledge
        lesson = self.lesson.api_lesson_getNewerStudyRecordByBid(params=[uid])  # 查询课程中台的
        df = pandas.read_excel('./k1.xls')
        _filter_skill = []
        _filter_know = []
        for guam in lesson.get('data').get('guaMei'):
            tezt = df[df['knowledge_id'] == guam['knowledgeId']]['knowledge_type_text']
            if list(tezt.keys()):
                if tezt[list(tezt.keys())[0]] in self.KNOWLEDGE and guam.get('skillId') in self.SKILL:
                    _filter_know.append(guam.get("knowledgeId"))
                    _filter_skill.append(guam.get("skillId"))
        return _filter_skill, _filter_know

    def get_doudi_yaml(self):
        # 获取兜底配置知识点列表
        with open('./bottomwords.yml', 'r') as f:
            data = yaml.load(f)
            dd_knowledge = []
            for v in data['bottomwords']['wordsList'].values():
                dd_knowledge.extend(v)
            return dd_knowledge

    def test_quests_nums10(self):
        # 验证推题接口至少返回10道题目 且
        uids_ = MySQL(pre_db='eduplatform0', db_name='eduplatform0').query('SELECT DISTINCT bid from knowledge_flow_record1')
        print(len(uids_))
        for data in uids_:
            params = {"bid": data['bid'], "gameType": "listen"}
            resp = api_get_question(params)
            _info = resp.json().get('data')
            print(_info)
            time.sleep(1)
            kg_joey = []  # joey返回知识点
            for kg20 in _info.get('top20Kgs'):
                kg_joey.append(kg20['kgId'])
                if params['gameType'] == 'listen':
                    assert kg20['wrongKgIds']
            less_skill, less_knowledge = self.lesson_filter_skill_know(uid=data['bid'])
            must_in_doudi = set(kg_joey) - set(less_knowledge)

            try:
                assert len(_info.get('top20Kgs')) >= 10
                assert len(list(set(kg_joey))) == len(kg_joey)  # 验证不能含有重复的题目
                assert must_in_doudi.issubset(set(self.get_doudi_yaml())) #验证不在已学知识点的数据必须是兜底
                print(must_in_doudi - set(self.get_doudi_yaml()))
            except AssertionError as e:
                with open('./error.txt', 'a') as f:
                    f.write(data['bid'] + '\n')

    def test_recall_30_more__bakN(self,):
        """
        1.30天内召回超过N知识点，组合生成recall接口参数
        2.预测得分结果是否需要验证
        """
        study_infos = {"test_452324354465nm9": {"code": 0, "data": [{"knowledgeId": "GEKWP5030618", "predScore": 93}, {"knowledgeId": "GEKWP4331578", "predScore": 96}, {"knowledgeId": "GEKWP4128543", "predScore": 83}, {"knowledgeId": "GEKWP3954973", "predScore": 85}, {"knowledgeId": "GEKWP4068708", "predScore": 81}, {"knowledgeId": "GEKWP3622904", "predScore": 85}, {"knowledgeId": "GEKWP5684816", "predScore": 93}, {"knowledgeId": "GEKWP3297750", "predScore": 99}, {"knowledgeId": "GEKWP7914961", "predScore": 83}, {"knowledgeId": "GEKLT2850818", "predScore": 86}, {"knowledgeId": "GEKLT1862444", "predScore": 86}, {"knowledgeId": "GEKWP4715478", "predScore": 94}, {"knowledgeId": "GEKWP7060644", "predScore": 81}, {"knowledgeId": "GEKWP3840378", "predScore": 95}, {"knowledgeId": "GEKLT1255136", "predScore": 85}, {"knowledgeId": "GEKLT3346561", "predScore": 97}, {"knowledgeId": "GEKWP9556260", "predScore": 85}, {"knowledgeId": "GEKWP0179415", "predScore": 94}, {"knowledgeId": "GEKWP6312061", "predScore": 92}, {"knowledgeId": "GEKWP7547219", "predScore": 81}, {"knowledgeId": "GEKWP6220109", "predScore": 79}, {"knowledgeId": "GEKWP4801379", "predScore": 75}, {"knowledgeId": "GEKWP1319055", "predScore": 63}, {"knowledgeId": "GEKWP0977559", "predScore": 68}, {"knowledgeId": "GEKWP0251072", "predScore": 73}, {"knowledgeId": "GEKLT5951404", "predScore": 45}, {"knowledgeId": "GEKWP2427575", "predScore": 57}, {"knowledgeId": "GEKWP9347940", "predScore": 7}, {"knowledgeId": "GEKWP7066399", "predScore": 92}, {"knowledgeId": "GEKWP4534284", "predScore": 91}, {"knowledgeId": "GEKWP4863713", "predScore": 73}, {"knowledgeId": "GEKWP8431769", "predScore": 61}, {"knowledgeId": "GEKWP8517166", "predScore": 68}, {"knowledgeId": "GEKWP2375047", "predScore": 2}, {"knowledgeId": "GEKWP3787705", "predScore": 88}, {"knowledgeId": "GEKWP7763887", "predScore": 76}, {"knowledgeId": "GEKWP5475870", "predScore": 77}, {"knowledgeId": "GEKLT2875254", "predScore": 10}]}}
        uid = 'test_452324354465nm9'
        print(uid)
        # db_name = self.lesson.api_lesson_get_name(uid=uid, table='knowledge_flow_record').get('data')

        # mysql = MySQL(pre_db=db_name.split('.')[0], db_name=db_name.split('.')[0])
        # study_infos = mysql.query(self.get_record_test_recall_30_more_N(uid=uid))
        params = dict(bid=uid, context=[], model='dssm')

        for study in study_infos[uid]['data']:
            print(study)
            params['context'].append({
                'skillId': study['skill_id'],
        #         'knowledgeId': study['knowledge_id'],
                # 'guaMei': {
                #     'finishTime': study['finish_time'],
                #     'displayScore': study['display_score'],
                #     'realScore': study['real_score'],
                #     'audioTag': study['audio_tag'],
                #     'count': 0
                # },
                # 'playGround': {
                #     'finishTime': study['finish_time'],
                #     'displayScore': study['display_score'],
                #     'realScore': study['real_score'],
                #     'audioTag': study['audio_tag'],
                #     'count': 0
                # },
            })
        # 验证召回流水按照预测得分从低到高排序
        pre_data = api_recall(params).get('data')
        print(params)
        # assert len(pre_data) == 20
        # zsero = float('-inf')
        # for pre_score in pre_data:
        #     assert (zsero <= pre_score['pred_score']) and (100 >= pre_score['pred_score'] >= 0)
        #     zsero = pre_score['pred_score']