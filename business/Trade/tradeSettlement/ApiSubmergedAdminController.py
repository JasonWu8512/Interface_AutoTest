# -*- coding: utf-8 -*-
# @Time    : 2021/4/29 16:01 下午
# @Author  : 万军
# @File    : ApiSubmergedAdminController.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiSubmergedAdminController:
    """
    Trade-Settlement-下沉相关eshop后台api接口
    """
    root = '/api/trade/settlement/submerged/admin'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_submerged_agent_list(self):
        """
        代理商列表
        :return:
        """

        api_url = f'{self.host}{self.root}/submergedAgentList'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_tax_deduct_percent_list(self):
        """
        税收比例
        :return:
        """

        api_url = f'{self.host}{self.root}/taxDeductPercentList'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_settlement_page_list(self, page_num=1, page_size=20, submerged_agent_no=None, settlement_month=None,
                                 check_bill_status=None,
                                 settlement_bill_status=None, invoice_status=None):
        """
        结算列表
        :param page_num: 第几页
        :param page_size: 每页多少
        :param submerged_agent_no: 代理商Id
        :param settlement_month: 结算月份
        :param check_bill_status: 对账单状态/对应界面 账单状态
        :param settlement_bill_status: 结算状态
        :param invoice_status: 发票状态
        :return:
        """

        api_url = f'{self.host}{self.root}/settlementPageList'
        body = {
            'pageNum': page_num,
            'pageSize': page_size,
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
            'checkBillStatus': check_bill_status,
            'settlementBillStatus': settlement_bill_status,
            'invoiceStatus': invoice_status,
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_settlement_detail(self, submerged_agent_no, settlement_month):
        """
        结算详情
        :param submerged_agent_no: 代理商id
        :param settlement_month: 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/settlementDetail/{submerged_agent_no}/{settlement_month}'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
        }
        resp = send_api_request(method='get', url=api_url, paramData=body, paramType='params', headers=self.headers)
        return resp

    def api_broker_age_bill_list(self, submerged_agent_no, settlement_month, order_no=None):
        """
        佣金账单列表
        :param submerged_agent_no: 代理商id
        :param settlement_month: 结算月份
        :param order_no: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/brokerageBillList'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
            'orderNo': order_no
        }
        resp = send_api_request(method='get', url=api_url, paramData=body, paramType="params", headers=self.headers)
        return resp

    def api_refund_broker_age_bill_list(self, submerged_agent_no, settlement_month, order_no=None):
        """
        退款扣除佣金账单列表
        :param submerged_agent_no: 代理商id
        :param settlement_month: 结算月份
        :param order_no: 订单号
        :return:
        """

        api_url = f'{self.host}{self.root}/refundBrokerageBillList'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
            'orderNo': order_no
        }
        resp = send_api_request(method='get', url=api_url, paramData=body, paramType="params", headers=self.headers)
        return resp

    def api_submit_check_bill_audit(self, tax_deduct_percent, submerged_agent_no, settlement_month):
        """
        提交审核
        :param tax_deduct_percent: 税率扣除
        :param submerged_agent_no 代理商Id
        :param settlement_month 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/submitCheckBillAudit'
        body = {
            'taxDeductPercent': tax_deduct_percent,
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_audit_check_bill(self, submerged_agent_no, settlement_month, audit_status, message):
        """
        审核对账单
        :param submerged_agent_no: 代理商Id
        :param settlement_month 结算月份
        :param audit_status 审核状态PASS,REFUND
        :param message 审核意见
        :return:
        """

        api_url = f'{self.host}{self.root}/auditCheckBill'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
            'auditStatus': audit_status,
            'message': message,
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_receive_invoice(self, submerged_agent_no, settlement_month):
        """
        收到发票
        :param submerged_agent_no: 代理商Id
        :param settlement_month 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/receiveInvoice'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_remit_success(self, submerged_agent_no, settlement_month):
        """
        打款成功
        :param submerged_agent_no: 代理商Id
        :param settlement_month 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/remitSuccess'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month,
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_adjust_bill(self, bill_no, adjust_type, adjust_amount, remark):
        """
        调整账单
        :param bill_no: 账单号
        :param adjust_type 调整类型
        :param adjust_amount: 调整额度
        :param remark 调整备注
        :return:
        """

        api_url = f'{self.host}{self.root}/adjustBill'
        body = {
            'billNo': bill_no,
            'adjustType': adjust_type,
            'adjustAmount': adjust_amount,
            'remark': remark
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

    def api_adjust_type_list(self):
        """
        调整类型列表
        :return:
        """

        api_url = f'{self.host}{self.root}/adjustTypeList'
        resp = send_api_request(method='get', url=api_url, headers=self.headers)
        return resp

    def api_export_achievement(self, submerged_agent_no, settlement_month):
        """
        导出绩效
        :param submerged_agent_no: 代理商id
        :param settlement_month 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/exportAchievement/{submerged_agent_no}/{settlement_month}'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp

    def api_export_brokerage(self, submerged_agent_no, settlement_month):
        """
        导出佣金
        :param submerged_agent_no: 代理商id
        :param settlement_month 结算月份
        :return:
        """

        api_url = f'{self.host}{self.root}/exportBrokerage/{submerged_agent_no}/{settlement_month}'
        body = {
            'submergedAgentNo': submerged_agent_no,
            'settlementMonth': settlement_month
        }
        resp = send_api_request(method='get', url=api_url, paramType='params', paramData=body, headers=self.headers)
        return resp


if __name__ == '__main__':
    Domains.set_domain('https://fat.jiliguala.com')
    submerged_admin = ApiSubmergedAdminController('aeb664904a684b7c8a8cf348ce824aab')
    print(submerged_admin.api_submerged_agent_list())
    # print(submerged_admin.api_adjust_bill(bill_no='2509', adjust_type='ADD', adjust_amount=200, remark='d'))





