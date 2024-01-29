# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/18 5:05 下午
@Author  : Demon
@File    : online_check.py
"""


import pandas as pd
import json

df = pd.read_excel('/Users/bianhua/PycharmProjects/tiga/testcase/AI/TestGuaMei25/meta_knowledge_ge.xls')


flow = json.load(open('./flow.json'))

download = json.load(open('./download.json'))

guamei = flow['data']['guaMei'] if flow['data']['guaMei'] else []
play = flow['data']['playground'] if flow['data'].get('playground') else []

gua_play_knowledge = []
for i in guamei:
    gua_play_knowledge.append(i)

for j in play:
    gua_play_knowledge.append(j)

def get_id_type(ids):
    return df[df['knowledge_id'] == ids]['knowledge_type_text']

def get_id_prop(ids):
    return df[df['knowledge_id'] == ids]['knowledge_reference_id']

doudi = ["GEKWP9457639","GEKLT2850818","GEKWP7066399","GEKWP7429338"
    "GEKWP5572970","GEKWP7066399","GEKLT0303810","GEKWP5513572"
    "GEKWP4843725","GEKWP7429338","GEKWP5513572","GEKWP2246127"
    "GEKWP7429338","GEKWP4843725","GEKWP5846663","GEKWP5572970"
    "GEKWP5513572","GEKWP5572970","GEKLT0303810", "GEKWP2246127"
    "GEKWP7066399", "GEKWP5846663", "GEKWP9457639", "GEKLT2850818"
    "GEKLT2850818", "GEKLT0303810", "GEKWP7066399", "GEKWP2246127"
    "GEKLT0303810", "GEKWP5846663", "GEKLT0303810", "GEKWP5572970"
    "GEKWP2246127", "GEKWP5846663", "GEKWP7066399", "GEKWP4843725"
    "GEKWP5846663", "GEKWP2246127","GEKWP4843725", "GEKWP9457639"]




def check_skill(skill):
    skl = skill.get('skillId')
    skills = ('GESRD7988306', 'GESLS2784867', 'GESSK5592673')
    if skl is None:
        return skill in skills
    else:
        return skl in skills
    # KNOWLEDGE = ('字母', '音素', '单词/词组')

def filter_skill(knowledge_list):
    # 筛选skill
    return filter(check_skill, knowledge_list)

# 排序
skill_knowledge_id = filter_skill(gua_play_knowledge)
skill_knowledge_id = sorted(skill_knowledge_id, key=lambda x: x['finishTime'], reverse=True)
print(skill_knowledge_id)
gua_play_knowledge_50_ids = [a['knowledgeId'] for a in skill_knowledge_id]

# print('gua_play_knowledge_50', gua_play_knowledge_50)

for d20 in download.get('data')['top20Kgs']:

    try:
        assert d20['kgId'] in gua_play_knowledge # 检查知识点已学
        print(d20['kgId'], get_id_type(ids=d20['kgId']),  get_id_prop(ids=d20['kgId']), '\n',)
    except Exception as e:
        print('20Kgs', d20['kgId'], d20['kgId'] in doudi)

    for error in d20['wrongKgIds']:
        try:
            assert error in gua_play_knowledge_50_ids[:50] # 检查错误选项知识点 已学
            # print(error, get_id_type(ids=error), )
            # print(get_id_prop(ids=error), '\n')
        except Exception as e:
            print('error', error, error in doudi)

