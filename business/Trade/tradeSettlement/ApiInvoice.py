# -*- coding: utf-8 -*-
# @Time: 2021/5/5 2:47 下午
# @Author: ian.zhou
# @File: ApiInvoice
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request
from business.common.UserProperty import UserProperty


class ApiInvoiceClient:
    """
    发票开具C端相关接口
    """
    root = '/api/trade/settlement/invoice'

    def __init__(self, token):
        self.headers = {'Authorization': token, "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_invoice_order_list(self):
        """
        获取可开票订单列表
        :return:
        """

        api_url = f'{self.host}{self.root}/orders'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_invoice_apply_prepare(self, orderNos:list):
        """
        开票申请预提交
        :param orderNos: 申请开票的订单号（list类型）
        :return:
        """

        api_url = f'{self.host}{self.root}/apply/prepare'
        body = {
            'orderNos': orderNos
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_invoice_apply(self, orderNos:list, invoiceType=0, buyerType=0, buyerTitle='叽里呱啦', mobile='12345678901',
                          email='trade_test@jiliguala.com', taxId='TEST12345612345'):
        """
        开票申请提交
        :param orderNos: 申请开票的订单号（list类型）
        :param invoiceType: 发票类型 0：增值税电子普通发票 1：增值税纸质普通发票
        :param buyerType: 抬头类型 0：个人 1：企业单位
        :param buyerTitle: 发票抬头
        :param mobile: 收票人手机号
        :param email: 收票人邮箱
        :param taxId: 税号（抬头类型为企业单位时需传入）
        :return:
        """

        api_url = f'{self.host}{self.root}/apply'
        body = {
            'orderNos': orderNos,
            'invoiceType': invoiceType,
            'buyerType': buyerType,
            'buyerTitle': buyerTitle,
            'taxId': taxId,
            'recipient': {
                'mobile': mobile,
                'email': email
            }
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_invoice_detail(self, serialNo):
        """
        获取开票申请详情
        :param serialNo: 开票申请流水号
        :return:
        """

        api_url = f'{self.host}{self.root}/apply/detail'
        body = {
            'serialNo': serialNo
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_invoice_apply_history(self, page=0, pageSize=10):
        """
        获取开票申请历史列表
        :param page: 页码
        :param pageSize: 每页数量
        :return:
        """

        api_url = f'{self.host}{self.root}/apply/history'
        body = {
            'page': page,
            'pageSize': pageSize,
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp


class ApiInvoiceAdmin:
    """
    发票开具管理后台相关接口
    """
    root = '/api/trade/settlement/invoice'

    def __init__(self, token):
        self.headers = {'admintoken': token, "Content-Type": "application/json"}
        self.host = Domains.domain

    def api_get_order_invoice_info(self, orderNo):
        """
        获取订单开票信息
        :param orderNo: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/admin/findAdminInvoiceByOrderNo'
        body = {
            'orderNo': orderNo
        }
        resp = send_api_request(url=api_url, method='get', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_cancel_blocked_invoice_apply(self, orderNo):
        """
        取消阻塞状态的开票申请
        :param orderNo: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/admin/cancelOrderInvoiceApply'
        body = {
            'orderNo': orderNo
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_set_paper_invoice(self, orderNo):
        """
        订单设置为已开纸质发票
        :param orderNo: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/admin/offlineInvoice'
        body = {
            'orderNo': orderNo
        }
        resp = send_api_request(url=api_url, method='post', paramData=body, paramType='params', headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_env_path('fat')
    Domains.set_domain('https://fat.jiliguala.com')
    invoice = ApiInvoiceAdmin(token='3fc61dd62c9741b79384af79bf37dbce')
    print(invoice.api_cancel_blocked_invoice_apply(orderNo='O84083419997089792'))
