# coding=utf-8
# @Time    : 2020/8/4 3:14 下午
# @Author  : keith
# @File    : apiRequests

import traceback

import requests
import urllib3
from retry import retry
from config.env.domains import Domains


@retry(tries=10, delay=1)
def request(method, url, **kwargs):
    resp_obj = None
    try:
        resp_obj = requests.request(method=method, url=url, timeout=5, **kwargs)
    except Exception as e:
        msg = "send request [%s] %s failed: %s" % (method, url, e)
        print(msg)
        traceback.print_exc()
    return resp_obj


def send_api_request(method, url, paramType=None, paramData=None, headers=None, cookies=None, verify=False, data=None,
                     files=None):
    """
    :param method: 请求method
    :param url: api路由
    :param paramType: body类型 - params、data、json
    :param paramData: 请求body
    :param headers: 请求头
    :param cookies: cookies
    :param verify:  boolean , verify for ssl
    :return:
    """
    urllib3.disable_warnings()
    if url.startswith("http"):
        url = url
    else:
        url = Domains.domain + "%s" % url
    if paramType and paramType.lower() in ["params", "data", "json", 'file']:
        if "params" == paramType.lower():
            respData = request(method=method.upper(), url=url, params=paramData, headers=headers,
                               cookies=cookies, verify=verify)
        elif "json" == paramType.lower():
            respData = request(method=method.upper(), url=url, json=paramData, headers=headers,
                               cookies=cookies, verify=verify)
        elif "file" == paramType.lower():
            # paramData = paramData if isinstance(paramData, dict) else {'file': paramData}
            respData = request(method=method.upper(), url=url, data=data, files=files, verify=verify, cookies=cookies)
        else:
            respData = request(method=method.upper(), url=url, data=paramData, headers=headers,
                               cookies=cookies, verify=verify)
    else:
        respData = request(method=method.upper(), url=url, headers=headers, cookies=cookies, verify=verify)
    # check.equal(respData.status_code, 200)
    # assert respData.status_code == 200
    try:
        resp = respData.json()
        assert not resp.get('rc')
    except ValueError:
        resp = {"text": respData.text}
    resp["status_code"] = respData.status_code
    resp["headers"] = respData.headers
    resp["cookies"] = respData.cookies
    return resp

# class HttpRequests(object):
#
#     @classmethod
#     def request(cls, method, url, **kwargs):
#         try:
#             resp_obj = requests.request(method=method, url=url, **kwargs)
#         except Exception as e:
#             msg = "send request [%s] %s failed: %s" % (method, url, e)
#             print(msg)
#             traceback.print_exc()
#         return resp_obj
#
#     @classmethod
#     def send_api_request(cls, method, url, paramType=None, paramData=None, headers=None, cookies=None, verify=False):
#         """
#         :param method: 请求method
#         :param url: api路由
#         :param paramType: body类型 - params、data、json
#         :param paramData: 请求body
#         :param headers: 请求头
#         :param cookies: cookies
#         :param verify:  boolean , verify for ssl
#         :return:
#         """
#         urllib3.disable_warnings()
#         if url.startswith("http"):
#             url = url
#         else:
#             url = Domains.domain + "%s" % (url)
#         if paramType and paramType.lower() in ["params", "data", "json"]:
#             if "params" == paramType:
#                 respData = cls.request(method=method.upper(), url=url, params=paramData, headers=headers,
#                                         cookies=cookies, verify=verify)
#             elif "json" == paramType:
#                 respData = cls.request(method=method.upper(), url=url, json=paramData, headers=headers,
#                                         cookies=cookies, verify=verify)
#             else:
#                 respData = cls.request(method=method.upper(), url=url, data=paramData, headers=headers,
#                                         cookies=cookies, verify=verify)
#         else:
#             respData = cls.request(method=method.upper(), url=url, headers=headers, cookies=cookies, verify=verify)
#         # check.equal(respData.status_code, 200)
#         try:
#             resp = respData.json()
#         except ValueError:
#             resp = respData.text
#         resp["status_code"] = respData.status_code
#         resp["headers"] = respData.headers
#         return resp

# """
# 发送上传文件的接口请求
# """
#
# def sendFilesRequest(
#         self, uri, data, filename, filepath, headers=None, cookies=None
# ):
#     """
#
#     :param uri:
#     :param data: 一般为空字典
#     :param filename: 上传文件名
#     :param filepath: 上传文件的完整路径
#     :param headers:
#     :param cookies:
#     :return:
#     """
#     if uri.startswith("http"):
#         url = uri
#     else:
#         url = (Domains.server_api or Domains.api) + "%s" % (uri)
#     filepath = filepath.encode("utf-8")
#     logging.info(filepath)
#     with open(filepath, "rb") as f:
#         data["file"] = (filename, f.read())
#     # data['file'] = (filename, codecs.open(filepath, 'rb').read())
#     encode_data = encode_multipart_formdata(data)
#     data = encode_data[0]
#     headers["Content-Type"] = encode_data[1]
#     respData = requests.post(
#         url, headers=headers, data=data, cookies=cookies, verify=False
#     )
#     time = respData.elapsed.microseconds
#     headers["Content-Type"] = "application/json"
#     # 写入接口响应时间
#     respTxt = respData.content.decode("utf-8")
#     displayUrl = url[url.find("/", url.find("//") + 2) + 1:]
#     logging.info(
#         "\n[Request] %s, %s\n[Response %s] %s"
#         % ("post", displayUrl, respData.status_code, respTxt)
#     )
#     try:
#         resp = self.basic.loadJsonData(respTxt)
#     except:
#         resp = respTxt
#     if type(resp) == list or str:
#         respJson = {}
#         respJson["result"] = resp
#         respJson["duration"] = int(time) / 1000
#         return respJson
#     else:
#         resp["duration"] = int(time) / 1000
#         return resp
