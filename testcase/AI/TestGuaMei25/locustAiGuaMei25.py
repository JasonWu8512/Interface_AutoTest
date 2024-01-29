# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/26 4:55 下午
@Author  : Demon
@File    : locustAiGuaMei25.py
"""

# 瓜美2.5智能推题压力测试
import arrow
import requests
from locust import HttpUser, TaskSet, task, User
# from utils.middleware.dbLib import MySQL
import json
import time
import random

def api_get_rank(lst):
    body = {"bid": "test_161819646983a"}
    lst.client.post("/playground/v3/rank", verify=False, json=body)


def api_get_recall(lst):
    body = {"bid": "test_161819646983a"}
    lst.client.post("/playground/v3/recall", verify=False, json=body)


class UserTaskRequest(TaskSet):
    def on_start(self):
        '''初始化数据，每个虚拟用户只执行一次'''
        base = '9dfa206827c948fea94b1b6aaed8ef6e'
        with open('./locust-uid.txt', 'r') as f:
            self.uids = [_ if _ else base for _ in f.read().split('\n')]

    def get_user(self):
        return random.choice(self.uids)

    @task(2)
    def get_ai_playground(self):
        headers = {'Content-Type': 'application/json'}
        body = {"bid": self.get_user(), "gameType": random.choice(["listen", "speak"])}
        resp = self.client.post("http://fat.jiliguala.com/api/aiplayground/v1/download", headers=headers,
                                verify=False, json=body, catch_response=True)
        print(resp.text)
        if resp.status_code == 200:
            resp.success()
            assert resp.json()['code'] == 0
            # assert len(resp.json().get('data').get('top20Kgs')) == 10
        else:
            resp.failure('FAIL')

    # @task(3)
    # def get_lesson_get_newer_study_record(self):
    #     headers = {'Content-Type': 'application/json'}
    #     body = {"bid": self.get_user(), "gameType": random.choice(["listen", "speak"])}
    #     url = f"http://10.50.79.103:60200/api/v1/studyFlow/getNewerStudyRecordByBid/{self.get_user()}"
    #     resp = self.client.post(url, headers=headers,
    #                             verify=False, json=body, catch_response=True)
    #     print(resp.text)
    #     if resp.status_code == 200:
    #         resp.success()
    #         assert resp.json()['code'] == 0
    #     else:
    #         resp.failure('FAIL')

    # @task(1)
    # def get_lesson_get_newer_study_record(self):
    #     headers = {'Content-Type': 'application/json'}
    #     body = {"bid": self.get_user(), "gameType": random.choice(["listen", "speak"])}
    #     url = f"http://10.50.79.103:60200/api/v1/studyFlow/getNewerStudyRecordByBid/{self.get_user()}"
    #     resp = self.client.post(url, headers=headers,
    #                             verify=False, json=body)
    #     print(resp.text)
    #     assert resp.json()['code'] == 0
    #     # if resp.status_code == 200:
    #     #     resp.success()
    #     #
    #     # else:
    #     #     resp.failure('FAIL')

    def param_section_upload(self):
        gamePredId = str(arrow.get(time.time()).int_timestamp) + str(random.randint(0, 111))
        roundId = random.choice(('20001', '20002', '20003', '20004', '20005', '20006'))
        sentenceDetail = []
        for i in range(10, 20):
            temp = {
                "knowledgeId": "GEKLT5244533",
                "gamePredId": gamePredId,
                "audioUrl": None,
                "displayScore": 0,
                "roundId": roundId,
                "skillId": "GESLS2784867",
                "predScore": 0,
                "audioTag": None,
                "realScore": 0
            }
            sentenceDetail.append(temp)
        param = {
            "sectionType": "tap-bubbles",
            "subLessonId": "K1PA00101",
            "sentenceDetail": sentenceDetail,
            "gameId": "K1PA00101",
            "bid": self.get_user(),
            "lessonId": "K1PA001",
            "roundDetail": [],
            "detail": [],
            "sectionId": "L1PA00102sec01",
            "score": 7
        }
        return json.dumps(param)

    # def on_stop(self):
    #     '''销毁数据，每个虚拟用户只执行一次'''
    #     self.client.post("/SignOut",{"CustomerGuid":"c7d7e646-9ce2-499b-a22e-a3c98d4545fe"})


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8098"
    min_wait = 1000
    max_wait = 5000
    tasks = [UserTaskRequest]



lesson_mock = {
    "code": 0,
    "data": {
        "bid": "test_161819646983a",
        "guaMei": [
            {
                "knowledgeId": "GEKWP4068708",
                "skillId": "GESLS2784867",
                "finishTime": 1618023669,
                "displayScore": 64,
                "realScore": 23,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP9382663",
                "skillId": "GESLS2784867",
                "finishTime": 1618023669,
                "displayScore": 6,
                "realScore": 38,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP4801379",
                "skillId": "GESLS2784867",
                "finishTime": 1618023669,
                "displayScore": 54,
                "realScore": 66,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKLT9197999",
                "skillId": "GESLS2784867",
                "finishTime": 1617678069,
                "displayScore": 18,
                "realScore": 11,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP5684816",
                "skillId": "GESLS2784867",
                "finishTime": 1617850869,
                "displayScore": 96,
                "realScore": 63,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP5534423",
                "skillId": "GESLS2784867",
                "finishTime": 1617678069,
                "displayScore": 86,
                "realScore": 60,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP3622904",
                "skillId": "GESLS2784867",
                "finishTime": 1615777269,
                "displayScore": 76,
                "realScore": 3,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP5572970",
                "skillId": "GESLS2784867",
                "finishTime": 1615777269,
                "displayScore": 76,
                "realScore": 3,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP6372595",
                "skillId": "GESLS2784867",
                "finishTime": 1616209269,
                "displayScore": 88,
                "realScore": 83,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP1319055",
                "skillId": "GESLS2784867",
                "finishTime": 1614913269,
                "displayScore": 17,
                "realScore": 50,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP8054284",
                "skillId": "GESLS2784867",
                "finishTime": 1615431669,
                "displayScore": 44,
                "realScore": 20,
                "count": 1,
                "audioTag": ""
            }
        ],
        "playGround": [
            {
                "knowledgeId": "GEKLT2875254",
                "skillId": "GESLS2784867",
                "finishTime": 1617764469,
                "displayScore": 72,
                "realScore": 18,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP7066399",
                "skillId": "GESLS2784867",
                "finishTime": 1617764469,
                "displayScore": 72,
                "realScore": 18,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKLT2273396",
                "skillId": "GESLS2784867",
                "finishTime": 1617678069,
                "displayScore": 37,
                "realScore": 12,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP4863713",
                "skillId": "GESLS2784867",
                "finishTime": 1618023669,
                "displayScore": 39,
                "realScore": 25,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP4066400",
                "skillId": "GESLS2784867",
                "finishTime": 1618110069,
                "displayScore": 83,
                "realScore": 3,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP5030618",
                "skillId": "GESLS2784867",
                "finishTime": 1617332469,
                "displayScore": 97,
                "realScore": 22,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP0886090",
                "skillId": "GESLS2784867",
                "finishTime": 1616641269,
                "displayScore": 32,
                "realScore": 84,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP0128431",
                "skillId": "GESLS2784867",
                "finishTime": 1616554869,
                "displayScore": 64,
                "realScore": 60,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP9229750",
                "skillId": "GESLS2784867",
                "finishTime": 1617332469,
                "displayScore": 23,
                "realScore": 74,
                "count": 1,
                "audioTag": ""
            },
            {
                "knowledgeId": "GEKWP3787705",
                "skillId": "GESLS2784867",
                "finishTime": 1615086069,
                "displayScore": 92,
                "realScore": 88,
                "count": 1,
                "audioTag": ""
            }
        ]
    },
    "requestId": "79d055675ee04bc0"
}

recall = {
		"code": 0,
		"data": [{
			"knowledgeId": "GEKWP7066399",
			"predScore": 86
		}, {
			"knowledgeId": "GEKWP4068708",
			"predScore": 96
		}, {
			"knowledgeId": "GEKWP9382663",
			"predScore": 64
		}, {
			"knowledgeId": "GEKWP4801379",
			"predScore": 74
		}, {
			"knowledgeId": "GEKLT2273396",
			"predScore": 67
		}, {
			"knowledgeId": "GEKLT9197999",
			"predScore": 63
		}, {
			"knowledgeId": "GEKWP4863713",
			"predScore": 69
		}, {
			"knowledgeId": "GEKWP8431769",
			"predScore": 12
		}, {
			"knowledgeId": "GEKWP5684816",
			"predScore": 31
		}, {
			"knowledgeId": "GEKWP4066400",
			"predScore": 49
		}, {
			"knowledgeId": "GEKWP5534423",
			"predScore": 5
		}, {
			"knowledgeId": "GEKWP5572970",
			"predScore": 90
		}, {
			"knowledgeId": "GEKWP5030618",
			"predScore": 84
		}, {
			"knowledgeId": "GEKWP0886090",
			"predScore": 60
		}, {
			"knowledgeId": "GEKWP0128431",
			"predScore": 72
		}, {
			"knowledgeId": "GEKWP9229750",
			"predScore": 70
		}, {
			"knowledgeId": "GEKWP6372595",
			"predScore": 76
		}, {
			"knowledgeId": "GEKWP1319055",
			"predScore": 72
		}, {
			"knowledgeId": "GEKWP3787705",
			"predScore": 72
		}, {
			"knowledgeId": "GEKWP8054284",
			"predScore": 50
		}, {
			"knowledgeId": "GEKWP3622904",
			"predScore": 72
		}]
	}

rank = recall



if __name__ == "__main__":
    import os
    # os.system("locust -f locustAiGuaMei25.py --host=http://10.42.103.131:51001") # dev
    os.system("locust -f locustAiGuaMei25.py")
    os.system("locust -f locustAiGuaMei25.py --host=http://rcx.jiliguala.com")
