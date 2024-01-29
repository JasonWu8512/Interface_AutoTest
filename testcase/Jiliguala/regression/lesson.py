# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time     : 2023/9/12 5:15 下午
@Author   : Anna
@File     : lesson.py
"""
import requests
import json
import time

lessons = ["4b45ac90fcf1454399abf5cb72b687f5", "b44ba329e7c64e09ac33dc19b6a4d69b", "0d09434d2bb84dda894f0c3543afaad4",
           "d8d58abc440b4e23ba862a2c05441039", "5e912d830c9e4167953ca026cf44f920"]
# lessons = ["5e912d830c9e4167953ca026cf44f920"]


def getSubLessonByLessonId(roadmapId, lessonId):
    url = "http://courseatom-rc.jlgltech.com/api/v1/study/getNodeChildrenLearningStatus"
    payload = json.dumps({
        "uid": "maoge_base_yr_course_user02",
        "bid": "maoge_base_yr_course_baby02",
        "roadmapId": roadmapId,
        "nodeId": lessonId
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)
    nodeList = res['data']
    nodeSdeqTuple = []
    for node in nodeList:
        nodeSdeqTuple.append((node['nodeSequence'], node['nodeId']))
    print(nodeSdeqTuple)
    return nodeSdeqTuple


def leafNodeComplete(uid, bid, nodeId, score, finishTime):
    url = "http://courseatom-rc.jlgltech.com/api/v1/roadmap/leafNodeComplete"
    payload = json.dumps({
        "uid": uid,
        "bid": bid,
        "nodeId": nodeId,
        "score": score,
        "finishTime": finishTime
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("REQUEST:", uid, bid, nodeId, score, "RESPONSE:", response.text)


uid = "cbe881823840488ca2473bfa7e9304a8"  # 1693808072000
bid = "f552e5052b3b45a0ac5d98710e000398"
score = 100
ts = 1695025959000

for lessonId in lessons:
    sublessonTpList = getSubLessonByLessonId("c2d3f2a250d441a197dfb484eb310f0b", lessonId)
    print("Get Sublesson", len(sublessonTpList), "from", lessonId)
    for sublesson in sublessonTpList:
        leafNodeComplete(uid, bid, sublesson[1], score, ts)
        time.sleep(3)