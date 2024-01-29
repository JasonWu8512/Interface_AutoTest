# coding=utf-8
# @Time    : 2020/7/31 4:31 下午
# @Author  : keith
# @File    : basicLib


# -*- coding: utf-8 -*-

import base64
import json
import logging
import os
import uuid
from collections import OrderedDict
from decimal import Decimal

# from business import businessUpdate
from config.env.domains import Domains

try:
    import xml.etree.cElementTree as cLiET
except ImportError:
    import xml.etree.ElementTree as ET


class BasicLib(object):
    dm = Domains()

    # def auth_decorator(self, id, key, uri, method, contentType):
    #     def decorator(func):
    #         def wrapper(*args):
    #             self.hawk.getHawkRequestHeader(id, key, uri, method, contentType)
    #             return func(*args)
    #         return wrapper
    #     return decorator

    def swap_char(self, chars):
        """ 交换字符串的奇偶数位 (swap_char('abcd') => 'badc') """
        return "".join(chars[char: char + 2][::-1] for char in range(0, len(chars), 2))

    def encode_pk(self, number: int):
        return self.swap_char(
            "".join(
                chr(ord(char) + 10 if ord(char) >= 97 else ord(char) + 49)
                for char in hex(number)[2:]
            )
        )

    def setAppUrlPath(self, apiUrl):
        """
        set global App Url Path
        :param apiUrl:
        :return:
        """
        self.dm.set_file_path(apiUrl)

    def getJsonKeyValue(self, jsonData, key):
        """
        get Json Key Value
        :param source:
        :param key:
        :return:
        """
        try:
            value = jsonData[key]
        except ValueError:
            logging.error("not found Json object, return data %s is not correct") % (
                jsonData
            )
            assert False
        return value

    def loadJsonData(self, source):
        """
        load json data
        @param string source
        @return json resp
        """
        try:
            resp = json.loads(source)
        except ValueError:
            msg = "not found JSON object, return data %s is not correct" % (source)
            logging.error(msg)
            assert False, msg
        return resp

    """
    check two dicts
    @:param dict body_data
    @:param dict expected_data
    @:return msg
    """

    def getNodeValueByNodePath(self, nodePath, filePath):
        logging.info(
            "Get the env conf value by node path '%s' with file path '%s'"
            % (nodePath, filePath)
        )

        testDataObj = ET.parse(
            os.path.dirname(os.path.abspath(__file__)) + "\\..\\" + filePath
        )
        try:
            element = testDataObj.getroot().find(nodePath)
        except ValueError:
            element = None
        val = None
        if element != None:
            val = element.text
        return val

    def loadAllConfValuesToDict(self, nodePath, filePath):
        logging.info(
            "get the env conf value by node path '%s' with file path '%s'"
            % (nodePath, filePath)
        )

        testDataObj = ET.parse(
            os.path.dirname(os.path.abspath(__file__)) + "\\..\\" + filePath
        )
        try:
            root = testDataObj.getroot()
        except:
            root = None
        config = {}
        if root != None:
            for item in root.iter():
                if len(item.findall("*")) == 0:
                    if item.text is not None:
                        config[item.tag] = item.text
        return config

    # def log_error(self, error_msg, capture=True):
    #     if type(error_msg) == str:
    #         error_msg = error_msg.decode('utf-8')
    #     raise NGError(error_msg, '', continuable=True)

    # def log_info(self, msg):
    #     if type(msg) == str:
    #         msg = self._convert_to_str(msg)
    #         try:
    #             logger.info(msg.decode("utf-8"))
    #         except:
    #             logger.info(msg)
    #     elif type(msg) == Unicode:
    #         logger.info(msg.encode('utf-8').decode('utf-8'))

    def _convert_to_str(self, item):
        try:
            return str(item)
        except:
            return item

    """
    verify blank
    @param string actual
    @return msg
    """

    def verifyBlank(self, actual, msg=None):
        try:
            assert actual.strip() == ""
        except Exception:
            if msg is None:
                logging.info(self._convert_to_str(actual) + " is not expected as blank")
            else:
                logging.info(self._convert_to_str(actual) + " is not expected as blank")
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(actual)
                    + " is expected as blank"
                    + "</font>"
                )
            else:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(msg)
                    + " Pass"
                    + "</font>"
                )

    """
    verify not blank
    @param string actual
    @return msg
    """

    def verifyNotBlank(self, actual, msg=None):
        try:
            if type(actual) == str:
                assert actual.strip() != ""
            elif type(actual) == list:
                assert len(actual)
        except Exception:
            if msg is None:
                logging.info(
                    self._convert_to_str(actual) + " is not expected as not blank"
                )
            else:
                logging.info(
                    self._convert_to_str(actual) + " is not expected as not blank"
                )
                logging.info(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(actual)
                    + " is expected as not blank"
                    + "</font>"
                )
            else:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(msg)
                    + " Pass"
                    + "</font>"
                )

    """
    verify None
    @param string actual
    @return msg
    """

    def verifyNone(self, actual, msg=None):
        try:
            assert actual == None
        except Exception:
            if msg is None:
                logging.info(self._convert_to_str(actual) + " is not expected as None")
            else:
                logging.info(self._convert_to_str(actual) + " is not expected as None")
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                self.log_info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(actual)
                    + " is expected as None"
                    + "</font>"
                )
            else:
                self.log_info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(msg)
                    + " Pass"
                    + "</font>"
                )

    """
    verify not None
    @param string actual
    @return msg
    """

    def verifyNotNone(self, actual, msg=None):
        try:
            assert actual != None
        except Exception:
            if msg is None:
                logging.error(
                    self._convert_to_str(actual) + " is not expected as not None"
                )
            else:
                logging.info(
                    self._convert_to_str(actual) + " is not expected as not None"
                )
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(actual)
                    + " is expected as not None"
                    + "</font>"
                )
            else:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + self._convert_to_str(msg)
                    + " Pass"
                    + "</font>"
                )

    """
    verify contains str
    @param string actual
    @param string expected
    @return msg
    """

    def verifyContains(self, actual, expected, msg=None):
        try:
            assert actual.find(expected) != -1
        except Exception:
            if msg is None:
                logging.info(
                    self._convert_to_str(actual)
                    + " is not contains "
                    + self._convert_to_str(expected)
                )
            else:
                logging.info(
                    self._convert_to_str(actual)
                    + " is not contains "
                    + self._convert_to_str(expected)
                )
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    self._convert_to_str(actual)
                    + " is contains "
                    + self._convert_to_str(expected)
                )
            else:
                logging.info(self._convert_to_str(msg) + " Pass")

    """
    verify str
    @param string actual
    @param string expected
    @return msg
    """

    def verify(self, actual, expected, msg=None):
        try:
            assert actual == expected
        except Exception:
            if msg is None:
                logging.info(
                    self._convert_to_str(actual)
                    + " is not expected as "
                    + self._convert_to_str(expected)
                )
            else:
                logging.info(
                    self._convert_to_str(actual)
                    + " is not expected as "
                    + self._convert_to_str(expected)
                )
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    self._convert_to_str(actual)
                    + " is expected as "
                    + self._convert_to_str(expected)
                )
            else:
                logging.info(self._convert_to_str(msg) + " Pass")

    """
    verify list
    @:param list actual
    @:param list expect
    @:return msg
    """

    def verifyList(self, actualList, expectList, msg=None):
        try:
            assert actualList == expectList
        except Exception:
            if msg is None:
                self.log_error(
                    self._convert_to_str(actualList)
                    + " is not expected as "
                    + self._convert_to_str(expectList)
                )
            else:
                self.log_info(
                    self._convert_to_str(actualList)
                    + " is not expected as "
                    + self._convert_to_str(expectList)
                )
                self.log_error(self._convert_to_str(msg) + " Failed")

    """
    verify in list
    @:param actual
    @:param list expect
    @:return msg
    """

    def verifyInList(self, actual, expectList, msg=None):
        try:
            assert actual in expectList
        except Exception:
            if msg is None:
                self.log_error(
                    self._convert_to_str(actual)
                    + " is not in "
                    + self._convert_to_str(expectList)
                )
            else:
                self.log_info(
                    self._convert_to_str(actual)
                    + " is not in "
                    + self._convert_to_str(expectList)
                )
                self.log_error(self._convert_to_str(msg) + " Failed")

    """
    verify no duplicate data in list
    @:param list
    @:return msg
    """

    def verifyNoDuplicateInList(self, checkList, msg=None):
        try:
            assert len(checkList) == len(set(checkList))
        except Exception:
            if msg is None:
                logging.info("List has duplicated data.")
            else:
                # print 'List has duplicated data!'
                logging.info("List has duplicated data!")
                logging.error(self._convert_to_str(msg) + " Failed")

    """
    verify dict
    @param dict actual
    @param dict expected
    @return msg
    """

    def verifyDict(self, actualDict, expectedDict, msg=None):
        try:
            assert OrderedDict(actualDict) == OrderedDict(expectedDict)
        except Exception:
            if msg is None:
                logging.error(
                    json.dumps(actualDict, ensure_ascii=False)
                    + " is not expected as "
                    + json.dumps(expectedDict, ensure_ascii=False)
                )
            else:
                logging.info(
                    json.dumps(actualDict, ensure_ascii=False)
                    + " is not expected as "
                    + json.dumps(expectedDict, ensure_ascii=False)
                )
                logging.error(self._convert_to_str(msg) + " Failed")
        else:
            if msg is None:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + json.dumps(actualDict, ensure_ascii=False)
                    + " is expected as "
                    + json.dumps(expectedDict, ensure_ascii=False)
                    + "</font>"
                )
            else:
                logging.info(
                    'BASIC: <font style="color:green;" >'
                    + json.dumps(expectedDict, ensure_ascii=False)
                    + " Pass"
                    + "</font>"
                )

    """
    get App Key
    @param string source
    @return string target
    """

    def getAppKey(self, source, start=3, end=-6):
        target = base64.decodestring(source[start:end] + "=")
        return target

    """
    get uuid by time stamp
    @return string uuidResult
    """

    def getUUidByTimeStamp(self):
        uuidResult = str(uuid.uuid1())
        return uuidResult

    """
    图片转成base64
    """

    def image_to_base64(self, image):
        with open(image, "rb") as f:
            base64_data = base64.b64encode(f.read())
        return base64_data.decode("utf-8")

    """
    求list中数据和
    """

    def get_list_addition(self, list_name):
        data = 0
        for k in list_name:
            if type(k) == str:
                data = self.get_addtion_conver_to_str(k, float(data))
            elif type(k) in (int, float):
                data += k
        return data

    """
    求和， str + float, 再转成str
    """

    def get_addtion_conver_to_str(self, res_str, amount):
        addtion_res = round(float(res_str) + amount, 2)
        decimal_res = Decimal(addtion_res).quantize(Decimal("0.00"))
        return str(decimal_res)


if __name__ == "__main__":
    basic = BasicLib()
    url = Urls()
    # url.set_file_path('alpha')
    config = url.set_env_path("alpha")
    url.set_file_path(config["url"])
    # uri = config['url']

    # print(type(basic.get_addtion_conver_to_str('12.3', 123)))
    # print basic.IdAesDecrypt('f9b13755dd505dedabccd20cf6b8815c')
    # print basic.IdAesDecrypt('badb92ca2ab9749190b805fc7120a153')
    # basic.delete_account('')
    # print basic.verifyUrlRe()
    # print basic.IdAesDecrypt('130cae5ced5f6d09aacd269ff36fae0e')
    # print basic.getAddressbyIp()

    # print(basic.get_sbl_token())
