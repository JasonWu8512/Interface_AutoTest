# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 11:38 上午
@Author  : Demon
@File    : AI_data.py
"""

import flask, json
from flask import request, Response
from testcase.AI.TestGuaMei25.TestMockFlow import TestMockFlow
# from testcase.Crm.est_tag import rank, recall
import time

'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)
# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@server.route('/playground/v3/recall', methods=['get', 'post'])
def recall():
    # 获取通过url请求传参的数据
    bid = request.get_json().get('bid')
    # 获取url请求传的密码，明文
    time.sleep(10)
    data = json.load(open('../../Crm/uid_score.json'))[bid]
    # data = json.loads(recall)
    return Response(json.dumps(data), content_type='application/json')

@server.route('/playground/v3/rank', methods=['get', 'post'])
def lesson_data():
    # 获取通过url请求传参的数据
    # data = json.load(open('./uid_score_flow.json', 'r'))
    bid = request.get_json().get('bid')
    data = json.load(open('../../Crm/uid_score.json'))[bid]
    return Response(json.dumps(data), content_type='application/json')

@server.route('/api/v1/studyFlow/getNewerStudyRecordByBid/<string:bid>', methods=['get', 'post'])
def get_name_data(bid):
    data = json.load(open('../../Crm/uid_score_flow.json', 'r'))
    info = data.get(bid)
    print(info)
    if info:
        return Response(json.dumps(info), content_type='application/json')
    #     info = TestAI().test_re_rank_between_10_20(bid=bid, score_rule=[2,5,3,2,3,1,1,2,1])
    # info = {'code': 0, 'requestId': 'd2fc3fc876bf29c4', 'data': [{'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP7106560', 'realScore': 8, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1617855085000, 'displayScore': 86, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP9382663', 'realScore': 50, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1617941485000, 'displayScore': 98, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP5572970', 'realScore': 42, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1618027885000, 'displayScore': 63, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP3840378', 'realScore': 91, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1617941485000, 'displayScore': 78, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP4863713', 'realScore': 67, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1617855085000, 'displayScore': 68, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKLT4725996', 'realScore': 46, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1617941485000, 'displayScore': 76, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP1362640', 'realScore': 23, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1618114285000, 'displayScore': 61, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP7060644', 'realScore': 1, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1618200685000, 'displayScore': 39, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKLT5951404', 'realScore': 40, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1617941485000, 'displayScore': 45, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKLT2875254', 'realScore': 27, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1618200685000, 'displayScore': 40, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP6921048', 'realScore': 45, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1615867885000, 'displayScore': 92, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP7951639', 'realScore': 71, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1617509485000, 'displayScore': 83, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKLT1255136', 'realScore': 100, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1616559085000, 'displayScore': 78, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP6672879', 'realScore': 23, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1616991085000, 'displayScore': 64, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP4534284', 'realScore': 44, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1616386285000, 'displayScore': 69, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP0409996', 'realScore': 8, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1616386285000, 'displayScore': 46, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP9382663', 'realScore': 38, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1615608685000, 'displayScore': 92, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP7106560', 'realScore': 92, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1614917485000, 'displayScore': 60, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP9229750', 'realScore': 100, 'reviewType': 'playGround', 'bid': 'test_1618287085898', 'finishTime': 1615349485000, 'displayScore': 67, 'audioTag': '', 'audioUrl': ''}, {'skillId': 'GESLS2784867', 'sublessonId': 'K1GEF00205', 'knowledgeId': 'GEKWP2761731', 'realScore': 9, 'reviewType': 'guamei', 'bid': 'test_1618287085898', 'finishTime': 1615176685000, 'displayScore': 29, 'audioTag': '', 'audioUrl': ''}]}
    # print(info)

    resonse = {"code": 0, "data": {"bid": bid}, "requestId": "79d055675ee04bc0"}
    guamei = []
    play = []
    for _ in info.get('data'):
        oper = {
            "knowledgeId": _['knowledgeId'],
            "skillId": _['skillId'],
            "finishTime": _['finishTime'],
            "displayScore": _['displayScore'],
            "realScore": _['realScore'],
            "count": 1,
            "audioTag": _['audioTag'],
        }
        if _['reviewType'] == 'guamei':
            guamei.append(oper)
        else:
            play.append(oper)
    if guamei:
        resonse['data']['guaMei'] = guamei
    if play:
        resonse['data']['playground'] = play
    print('中台MOCK', resonse)

    return Response(json.dumps(resonse), content_type='application/json')

if __name__ == '__main__':
    server.run(debug=True, port=8923, host='0.0.0.0')# 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问