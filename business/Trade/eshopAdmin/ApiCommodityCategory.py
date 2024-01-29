# @Time : 2021/7/30
# @Author : kira
# @File : ApiCommodityCategory.py
# @Software: PyCharm

from config.env.domains import Domains
from utils.requests.apiRequests import send_api_request


class ApiCommodityCategory:
    """
    eshop 商城管理后台---商品类目管理
    """
    root = '/api/eshop-admin'

    def __init__(self, token):
        self.headers = {'admintoken': token}
        self.host = Domains.domain

    def api_get_category_list(self):
        """
        获取商品类目列表
        """
        api_url = f'{self.host}{self.root}/commodity/categories'
        resp = send_api_request(method='get', url=api_url, paramType='params', headers=self.headers)
        return resp

    def api_create_edit_category(self, parentCategoryNo=None, title=None, categoryNo=None, state=None, create=None):
        """
        新增/编辑商品类目
        parentCategoryNo:父级类目编码
        title:类目名称
        categoryNo:类目编码
        state:状态（0：默认项；1：启用；2：禁用）
        create:新建/编辑（true：新建；false：编辑）
        """
        api_url = f'{self.host}{self.root}/commodity/categories'
        body = {
            'parentCategoryNo': parentCategoryNo,
            'title': title,
            'categoryNo': categoryNo,
            'state': state,
            'create': create
        }
        resp = send_api_request(method='post', url=api_url, paramType='json', paramData=body, headers=self.headers)
        return resp

