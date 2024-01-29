''' 
===============
@Project  :  JLGL_autotest
@Author   :  chenxi_zhao
@Data     :  2023/1/6
===============
'''

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.Jiliguala.user.ApiUser import ApiUser


class Apiexpand(object):
    """
    拓展tab详情页
    """
    root = '/api/sc/table'

    def __init__(self,token):
        self.dm = Domains()
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            "Authorization": token,
            "version" : "1",
            # "jlgl-version": "11.33.0"
        }
        # 设置域名host
        self.host = self.dm.set_env_path('prod')["url"]
        print(self.host)

    def api_Tztab(self,bid):
        """
        拓展tab页详情
        """
        self.api_url = "/api/sc/table"
        print(self.host + self.api_url)
        body = {
                'bid': bid,
                'nonce':'2E849E88-86CD-42CC-9890-1CE0AD2B9358'}
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_Tzeg(self):
        """
        拓展详情页儿歌电台
        """
        self.api_url= "/api/audios/channel"
        body = {"nonce":"a0d37de7-f726-470f-ae41-e6ebc4a632d9",
                }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                               headers=self.headers)
        print(resp)
        return resp

    def api_Tzer_list(self,bid):
        """
        拓展儿歌电台列表
        """
        self.api_url = "/api/audios/list"
        body = {
                "bid": bid,
                "channel":"1000",
                "nonce":"b779a565-3c47-482a-81e9-83e6c57e7891"
                }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


    def api_tzky(self):
        """
        拓展每日口语
        """
        self.api_url = "/api/forums/advposts"
        print(self.host + self.api_url)
        body = {"_id":"7ec5b9dcb1c34aadb6cae69d4a9e503f",
                "flr":0,
                "inclusive":1,
                "sort":"asc",
                "nonce":"11f917fa-93ab-45b3-8e60-6ef10974d3fd"
                }

        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_TZch(self):
        """
        拓展每日词汇
        """
        self.api_url = "/api/flashcards/anonymous"

        body = {
            "nonce": "24F5B731-D879-4D25-A1BE-393394DF5E76",
            "rid": "950d263facbc43d6bb7a6a37108cae3b"
        }

        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp


    def api_TZch_list(self):
        """
        拓展每日词汇列表
        """
        self.api_url = "/api/flashcards/anonymous"

        body = {
               "nonce":"3C13CE94-B8A4-45E6-9874-B98916791782",
                }

        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                            headers=self.headers)
        print(resp)
        return resp

    def api_TZ_gsh(self):
        """
        拓展tab故事会
        """
        self.api_url = "/api/videos/channel"

        body = {
            "nonce": "d9a32ccf-1a90-43b5-85f6-86ec57223f2e",
        }

        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_TZgsh_list(self,bid):
        """
        拓展tab故事会列表
        """
        self.api_url = "/api/videos/list"

        body = {
            "bid" : bid,
            "channel" : 1000,
            "nonce":"d2fe07f4-5ab7-4aa2-add4-dfccd4bc3aa3"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_sc(self):
        """
        拓展tab查看全部专辑区详情页
        """
        self.api_url = "/api/sc/album/list"

        body = {"page":0,
                "nonce":"ca37f115-4d75-4003-a4e1-2f0b98310a63"
        }

        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_sc_kc(self,bid):
        """
        进入全部专辑区，点击拓展课学习
        """
        self.api_url = "/api/sc/album"

        body = {
            "bid": bid,
            "albumId": "AlbumCDS009",
            "nonce": "c64c029f-e7d9-42d8-8c54-d136efe70f3a"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_junior(self,bid):
        """
        拓展tab页，点击亲子早教资源
        """
        self.api_url = "/api/home/junior"

        body = {
            "bid": bid,
            "nonce": "89b31bb3-5a14-457d-8f44-c0dd4b52e93a"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_course(self,bid):
        """
        亲子早教资源，点击学习课程
        """
        self.api_url = "/api/seed/course"

        body = {
            "bid": bid,
            "courseId" : "A1PG045",
            "nonce" : "69dded11-ee58-46e3-9a3a-51cdd53a7313"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_byGameld(self,Env):
        """
        口语交流室
        """
        self.api_url = "/api/game/resource/byGameId"

        body = {
            "gameId":"LCXMT001",
            "cocosEnv":Env,
            "nonce":"2dd377f8-a8cd-4e89-8975-2641ec36a9d6"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_byGameId_ggxw(self,Env):
        """
        呱呱小屋
        """
        self.api_url = "/api/game/resource/byGameId"

        body = {
            "gameId": "GG",
            "cocosEnv": Env,
            "nonce": "a4756f0c-cd22-4287-82c8-feb06d8c284c"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_byGameId_home(self,bid):
        """
        呱呱小屋主页
        """
        self.api_url = "/api/guavatar/home"

        body = {
            "bid": bid
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_smartreview_home(self,bid):
        """
        智能闯关
        """
        self.api_url = "/api/smartreview/home"

        body = {
            "bid": bid,
            "nonce": "ae67dbb0-8443-4bc7-a8cb-2be7c7fc48a9"
        }
        resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

    def api_childsong(self,bid,level):
         """
         年课每周儿歌
         """
         self.api_url = "/api/sc/childsong"

         body = {
            "bid": bid,
            "level" : level,
             "nonce":"45294033-96FC-44B4-B9AB-59E7F3955139"
        }
         resp = send_api_request(url=self.host + self.api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
         print(resp)
         return resp

    def api_table(self,bid):
        api_url = "/api/sc/table"
        print(self.host + self.root)
        body = {
                'bid':bid,
                "nonce":"1219afca-4f34-4bc5-b55d-5945017f3afe"
        }

        resp = send_api_request(url=self.host + api_url, paramType='params', paramData=body, method="get",
                                headers=self.headers)
        print(resp)
        return resp

if __name__ == '__main__':

    dm = Domains()
    config = dm.set_env_path('fat')
    dm.set_domain(config['url'])
    user = ApiUser()
    expandBid = config["expandTab"]
    cocosEnv = config["cocosEnv"]
    CS_user = config["CS_user"]
    token = user.get_token(typ="mobile", u=CS_user["user"], p=CS_user["pwd"])
    token1 = user.get_token(typ="mobile", u="11111130149", p="Jlgl168.")
    expandapi = Apiexpand(token = token)
    expandapi1= Apiexpand(token = token1)
    # resp = expandapi.api_Tztab(expandBid["bid"])
    # resp1 = expandapi.api_Tzeg()
    # resp2 = expandapi.api_Tzer_list(expandBid["bid"])
    # resp3 = expandapi.api_tzky()
    # resp4 = expandapi.api_TZch_list()
    # resp5 = expandapi.api_TZch()
    # resp6 = expandapi.api_TZ_gsh()
    # resp7 = expandapi.api_TZgsh_list(expandBid["bid"])
    # resp8 = expandapi.api_sc()
    # resp9 = expandapi.api_sc_kc(expandBid["bid"])
    # resp10 = expandapi.api_junior(expandBid["bid"])
    # resp11 = expandapi.api_course(expandBid["bid"])
    # resp12 = expandapi.api_byGameld(cocosEnv["Env"])
    # resp13 = expandapi.api_byGameId_ggxw(cocosEnv["Env"])
    # resp14 = expandapi.api_byGameId_home(expandBid["bid"])
    # resp15 = expandapi.api_smartreview_home(expandBid["bid"])
    resp = expandapi1.api_childsong()
