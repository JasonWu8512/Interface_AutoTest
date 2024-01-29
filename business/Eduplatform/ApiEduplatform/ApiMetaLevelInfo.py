# coding=utf-8
# @Time    : 2021/6/8 下午8:09
# @Author  : Sariel
# @File    : ApiMetaLevelInfo

from utils.requests.apiRequests import send_api_request
from config.env.domains import Domains
# from prettyprinter import cpprint


class ApiMetaLevelInfo(object):
    def __init__(self):
        # 请求头文件
        self.host = Domains.domain
        self.root = '/api/v1/metaLevelInfo'

    def api_get_level_meta_info(self, levelId, paidCurrent99, uid, bid):
        """
        获取level基本信息

        :param levelId:         路线图等级
        :param paidCurrent99:   是否包含9块9，1-是，0-否
        :param uid:             用户id,用于区分是否是AB实验/老9块9用户
        :param bid:             baby id
        :return:
        """
        api_url = f"{self.root}/getLevelMetaInfo"
        body = {
            "levelId": levelId,
            "paidCurrent99": paidCurrent99,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_week_meta_info(self, weekId, uid, bid):
        """
        获取week基本信息

        :param weekId:          课程组id
        :param uid:             用户id,用于区分是否是AB实验/老9块9用户
        :param bid:             baby id
        :return:
        """
        api_url = f"{self.root}/getWeekMetaInfo"
        body = {
            "weekId": weekId,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_lesson_meta_info(self, lessonId, uid, bid):
        """
        获取lesson基本信息

        :param lessonId:        课程id
        :param uid:             用户id,用于区分是否是AB实验/老9块9用户
        :param bid:             baby id
        :return:
        """
        api_url = f"{self.root}/getLessonMetaInfo"
        body = {
            "lessonId": lessonId,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_sublesson_meta_info(self, sublessonId, uid, bid):
        """
        获取sublesson基本信息

        :param sublessonId:     子课程id
        :param uid:             用户id,用于区分是否是AB实验/老9块9用户
        :param bid:             baby id
        :return:
        """
        api_url = f"{self.root}/getSublessonMetaInfo"
        body = {
            "sublessonId": sublessonId,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_sublesson_type_meta_info(self, sublessonTypeId):
        """
        获取sublessonType的基本信息

        :param sublessonTypeId: 子课程类型id
        :return:
        """
        api_url = f"{self.root}/getSublessonTypeMetaInfo/{sublessonTypeId}"
        resp = send_api_request(url=api_url, paramType="json", method="post")
        return resp

    def api_get_sublesson_type_meta_info_list(self, sublessonTypeId=[]):
        """
        获取sublessonType集合的基本信息

        :param sublessonTypeId:     子课程id（数组）
        :return:
        """
        api_url = f"{self.root}/getSublessonTypeMetaInfoList"
        resp = send_api_request(url=api_url, paramType="json", paramData=sublessonTypeId, method="post")
        return resp

    def api_get_level_list_info_by_subject(self, subject):
        """
        根据subject获取level数组

        :param subject: 学科，例如：GE、MA、YW
        :return:
        """
        api_url = f"{self.root}/getLevelListInfoBySubject/{subject}"
        resp = send_api_request(url=api_url, paramType="json", method="post")
        return resp

    def api_get_week_meta_by_week_num_info(self, levelId, weekType, uid, bid, weekNum):
        """
        根据weekNum获取周基本信息

        :param levelId:     路线图等级
        :param weekType:    课程组类型
        :param uid:         用户id,用于区分是否是AB实验/老9块9用户
        :param bid:         baby id
        :param weekNum:     这一课程组类型下的第几个，从0开始计数
        :return:
        """
        api_url = f"{self.root}/getWeekMetaByWeekNumInfo"
        body = {
            "levelId": levelId,
            "weekType": weekType,
            "uid": uid,
            "bid": bid,
            "weekNum": weekNum
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_week_num_by_type(self, levelId, weekType, uid, bid):
        """
        获取该level下，这一weekType的周数

        :param levelId:     路线图等级
        :param weekType:    课程组类型
        :param uid:         用户id,用于区分是否是AB实验/老9块9用户
        :param bid:         baby id
        :return:
        """
        api_url = f"{self.root}/getWeekNumByType"
        body = {
            "levelId": levelId,
            "weekType": weekType,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp

    def api_get_meta_level_week_info(self, levelId, paidCurrent99, uid, bid):
        """
        获取课程大纲内容和周主题等信息

        :param levelId:         路线图等级
        :param paidCurrent99:   是否包含9块9，1-是，0-否
        :param uid:             用户id,用于区分是否是AB实验/老9块9用户
        :param bid:             baby id
        :return:
        """
        api_url = f"{self.root}/getMetaLevelWeekInfo"
        body = {
            "levelId": levelId,
            "paidCurrent99": paidCurrent99,
            "uid": uid,
            "bid": bid
        }
        resp = send_api_request(url=api_url, paramType="json", paramData=body, method="post")
        return resp



if __name__ == '__main__':
    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['eduplatform_url'])
    metaLevelInfo = ApiMetaLevelInfo()
    # cpprint(metaLevelInfo.api_get_level_meta_info(levelId="K1GE", paidCurrent99=1, uid="abtestsuibianxie",
    #                                               bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(metaLevelInfo.api_get_week_meta_info(weekId="K1GEE04", uid="abtestsuibianxie",
    #                                              bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(metaLevelInfo.api_get_lesson_meta_info(lessonId="K1GEF001", uid="abtestsuibianxie",
    #                                                bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(metaLevelInfo.api_get_sublesson_meta_info(sublessonId="K1GEF00101", uid="abtestsuibianxie",
    #                                                   bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(metaLevelInfo.api_get_sublesson_type_meta_info(sublessonTypeId="test2TEST2test"))
    # cpprint(metaLevelInfo.api_get_sublesson_type_meta_info_list(sublessonTypeId=["test2TEST2test", "teacherclassT2"]))
    # cpprint(metaLevelInfo.api_get_level_list_info_by_subject("MA"))
    # cpprint(metaLevelInfo.api_get_week_meta_by_week_num_info(levelId="K1GE", weekType="lesson", uid="abtestsuibianxie",
    #                                                          bid="e9f18597eae14a3a9aa3e58ec1967793", weekNum="0"))
    # cpprint(metaLevelInfo.api_get_week_num_by_type(levelId="K1GE", weekType="previewOperation", uid="abtestsuibianxie",
    #                                                bid="e9f18597eae14a3a9aa3e58ec1967793"))
    # cpprint(metaLevelInfo.api_get_meta_level_week_info(levelId="K1GE", paidCurrent99=1, uid="abtestsuibianxie",
    #                                                    bid="e9f18597eae14a3a9aa3e58ec1967793"))
