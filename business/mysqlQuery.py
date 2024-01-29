# -*- coding: utf-8 -*-
# @Time: 2021/3/21 4:20 下午
# @Author: ian.zhou
# @File: mysqlQuery
# @Software: PyCharm
import time

from utils.middleware.dbLib import MySQL
from config.env.domains import Domains


class HwQuery(object):
    # dm = Domains()
    """user相关的mysql操作"""

    def __init__(self):
        # self.config = self.dm.set_env_path('fat')
        self.user_inter = MySQL(pre_db='jlgg', db_name='user')
        self.crm_leads_assign = MySQL(pre_db='crm', db_name='leads_assign')

    def phone_query_user_inter(self, phone, area_code):
        """查询海外user_inter用户信息"""
        sql = f"SELECT * FROM inter_user where phone='{phone}' and area_code='{area_code}'"
        print(sql)
        phone_query = self.user_inter.query(sql)
        print(phone_query)
        return phone_query[0]

    def mail_query_user_inter(self, mail):
        """查询海外user_inter用户信息"""
        sql = f"SELECT * FROM inter_user where email='{mail}'"
        print(sql)
        mail_query = self.user_inter.query(sql)
        print(mail_query)
        return mail_query[0]

    def uid_query_leads_assign(self, uid):
        """查询海外leads_assign班主任信息"""
        time.sleep(6)
        sql = f"SELECT * FROM salesman_user_binding where uid='{uid}'"
        print(sql)
        uid_crm_leads_assign = self.crm_leads_assign.query(sql)
        print(uid_crm_leads_assign)
        return uid_crm_leads_assign[0]


class EshopQuery:
    """Eshop相关的mysql操作"""

    def __init__(self):
        self.eshop = MySQL(pre_db='eshop', db_name='eshop')
        self.eshop_orders = MySQL(pre_db='eshop_orders', db_name='eshop_orders')
        self.eshop_orderbiz = MySQL(pre_db='eshop_orderbiz', db_name='eshop_orderbiz')
        self.eshop_biz = MySQL(pre_db='eshop_biz', db_name='eshop_biz')
        self.eshop_promotion = MySQL(pre_db='eshop_promotion', db_name='promotion')
        self.trade_account = MySQL(pre_db='trade_account', db_name='trade_account')
        self.trade_settlement = MySQL(pre_db='trade_settlement', db_name='settlement')
        self.app_international

    def query_eshop_orders(self, sql):
        res = self.eshop_orders.query(sql)
        return res

    def execute_eshop_orders(self, sql):
        self.eshop_orders.execute(sql)

    def excute_eshop_promotion(self, sql):
        self.eshop_promotion.execute(sql)

    def execute_trade_settlement(self, sql):
        self.trade_settlement.execute(sql)

    def delete_order_invoice_record(self, order_no):
        """通过order_no删除订单开票记录"""
        if not order_no:
            raise ('必须指定订单号')
        query = f'DELETE invoice_order_lock,invoice_apply_order,invoice_apply,invoice ' \
                f'FROM invoice_order_lock ' \
                f'LEFT JOIN invoice_apply_order ON invoice_apply_order.order_no=invoice_order_lock.order_no ' \
                f'LEFT JOIN invoice_apply ON invoice_apply.id=invoice_apply_order.invoice_apply_id ' \
                f'LEFT JOIN invoice ON invoice.id=invoice_apply.invoice_id ' \
                f'WHERE invoice_order_lock.order_no="{order_no}"'
        self.trade_settlement.execute(query)

    def query_user_subject(self, user_no):
        """查询用户学科信息"""
        if not user_no:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM activity_subject_seq WHERE user_no="{user_no}" ORDER BY create_at'
        res = self.eshop_promotion.query(query)
        return res

    def delete_user_subject(self, user_no):
        """删除用户学科信息"""
        if not user_no:
            raise ('必须指定删除条件')
        query = f'DELETE FROM activity_subject_seq WHERE user_no="{user_no}"'
        self.eshop_promotion.execute(query)

    def query_user_order_snap(self, user_no):
        """查询用户双月课订单快照信息"""
        if not user_no:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM activity_order_snap WHERE user_no="{user_no}"'
        res = self.eshop_promotion.query(query)
        return res

    def delete_user_promtion_order_snap(self, user_no):
        """删除用户优惠中心订单快照表双月课订单"""
        if not user_no:
            raise ('必须指定删除条件')
        query = f'DELETE FROM activity_order_snap WHERE user_no="{user_no}"'
        self.eshop_promotion.execute(query)

    def set_6week_system_course(self, sgu_no):
        """设置可享受6周课优惠SGU"""
        if not sgu_no:
            raise ('必须指定SGU商品')
        query = f'INSERT INTO activity_scope (activity_id, ref_type, ref_sub_type, ref_id, type) VALUES ' \
                f'( 3, 2, 3, "{sgu_no}", 0);'
        self.eshop_promotion.execute(query)

    def delete_6week_system_course(self, sgu_no):
        """删除可享受6周课优惠SGU"""
        if not sgu_no:
            raise ('必须指定SGU商品')
        query = f'DELETE FROM activity_scope WHERE ref_id="{sgu_no}"'
        self.eshop_promotion.execute(query)

    def set_system_course_blacklist(self, sgu_no):
        """设置正价课拓科优惠黑名单"""
        if not sgu_no:
            raise ('必须指定SGU商品')
        query = f'INSERT INTO activity_scope (activity_id, ref_type, ref_sub_type, ref_id, type) VALUES ' \
                f'( 1, 2, 3, "{sgu_no}", 1);'
        self.eshop_promotion.execute(query)

    def delete_system_course_blacklist(self, sgu_no):
        """删除正价课拓科优惠黑名单"""
        if not sgu_no:
            raise ('必须指定SGU商品')
        query = f'DELETE FROM activity_scope WHERE ref_id="{sgu_no}"'
        self.eshop_promotion.execute(query)

    def query_user_coupon(self, user_no):
        """查询用户拥有的优惠券"""
        if not user_no:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM coupon_grant WHERE user_no="{user_no}"'
        res = self.eshop_promotion.query(query)
        return res

    def query_coupon_strategy(self, coupon_id):
        """查询优惠券的金额"""
        if not coupon_id:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM coupon_strategy WHERE coupon_id="{coupon_id}"'
        res = self.eshop_promotion.query(query)
        return res

    def delete_user_coupon(self, user_no):
        """删除用户拥有的优惠券"""
        if not user_no:
            raise ('必须指定SGU商品')
        query = f'DELETE FROM coupon_grant WHERE user_no="{user_no}"'
        self.eshop_promotion.execute(query)

    def query_coupon(self, redirect_url):
        """查询优惠券id"""
        if not redirect_url:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM coupon WHERE redirect_url="{redirect_url}"'
        res = self.eshop_promotion.query(query)
        return res

    def delete_coupon(self, coupon_id):
        """通过优惠券id删除优惠券相关信息"""
        if not coupon_id:
            raise ('必须指定删除条件')
        query = f'DELETE coupon,coupon_scope,coupon_strategy,coupon_grant FROM coupon ' \
                f'LEFT JOIN coupon_scope ON coupon.id=coupon_scope.coupon_id ' \
                f'LEFT JOIN coupon_strategy ON coupon.id=coupon_strategy.coupon_id ' \
                f'LEFT JOIN coupon_grant ON coupon.id=coupon_grant.coupon_id ' \
                f'WHERE coupon.id={coupon_id}'
        self.eshop_promotion.execute(query)

    def delete_sxu_record(self, sxu_id):
        """通过sxu id删除SXU相关信息"""
        if not sxu_id:
            raise ('必须指定删除条件')
        query = f'DELETE commodity,commodity_map,commodity_sgu_map,commodity_spec_map,' \
                f'commodity_stock,commodity_tag_map FROM commodity ' \
                f'LEFT JOIN commodity_map ON commodity_map.spu_id=commodity.id ' \
                f'LEFT JOIN commodity_sgu_map ON commodity_sgu_map.sgu_id=commodity.id ' \
                f'LEFT JOIN commodity_spec_map ON commodity_spec_map.spu_id=commodity.id ' \
                f'LEFT JOIN commodity_stock ON commodity_stock.sxu_id=commodity.id ' \
                f'LEFT JOIN commodity_tag_map ON commodity_tag_map.commodity_id=commodity.id ' \
                f'WHERE commodity.id={sxu_id}'
        self.eshop.execute(query)

    def query_user_order(self, order_no):
        """查询用户订单信息"""
        if not order_no:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM orders WHERE order_no="{order_no}"'
        res = self.eshop_orders.query(query)
        return res

    def delete_order_by_order_no(self, order_no):
        """通过order_no删除order信息"""
        if not order_no:
            raise ('必须指定删除条件')
        query = f'DELETE orders,orders_address,orders_biz,orders_detail,orders_promotion,charges,' \
                f'orders_refund FROM orders ' \
                f'LEFT JOIN orders_address ON orders_address.orders_id=orders.id ' \
                f'LEFT JOIN orders_biz ON orders_biz.orders_id=orders.id ' \
                f'LEFT JOIN orders_detail ON orders_detail.orders_id=orders.id ' \
                f'LEFT JOIN orders_promotion ON orders_promotion.orders_id=orders.id ' \
                f'LEFT JOIN charges ON charges.orders_id=orders.id ' \
                f'LEFT JOIN orders_refund ON orders_refund.orders_id=orders.id ' \
                f'WHERE orders.order_no="{order_no}"'
        self.eshop_orders.execute(query)

    def delete_order_by_user_no(self, user_no):
        """通过user_no删除用户所有order信息"""
        if not user_no:
            raise ('必须指定删除条件')
        query = f'DELETE orders,orders_address,orders_biz,orders_detail,orders_promotion,charges,' \
                f'orders_refund FROM orders ' \
                f'LEFT JOIN orders_address ON orders_address.orders_id=orders.id ' \
                f'LEFT JOIN orders_biz ON orders_biz.orders_id=orders.id ' \
                f'LEFT JOIN orders_detail ON orders_detail.orders_id=orders.id ' \
                f'LEFT JOIN orders_promotion ON orders_promotion.orders_id=orders.id ' \
                f'LEFT JOIN charges ON charges.orders_id=orders.id ' \
                f'LEFT JOIN orders_refund ON orders_refund.orders_id=orders.id ' \
                f'WHERE orders.user_no="{user_no}"'
        self.eshop_orders.execute(query)

    def delete_promotion_record(self, promotion_id):
        """通过promotion id删除promotion信息"""
        if not promotion_id:
            raise ('必须指定删除条件')
        query = f'DELETE promotion_groupon,promotion_groupon_commodity_map FROM promotion_groupon ' \
                f'LEFT JOIN promotion_groupon_commodity_map ' \
                f'ON promotion_groupon_commodity_map.promotion_groupon_id=promotion_groupon.id ' \
                f'WHERE promotion_groupon.groupon_no="{promotion_id}"'
        self.eshop_biz.execute(query)

    def delete_promotion_by_spu_no(self, spu_no):
        """通过spu_no删除关联的promotion信息"""
        if not spu_no:
            raise ('必须指定删除条件')
        query = f'DELETE promotion_groupon,promotion_groupon_commodity_map FROM promotion_groupon ' \
                f'LEFT JOIN promotion_groupon_commodity_map ' \
                f'ON promotion_groupon_commodity_map.promotion_groupon_id=promotion_groupon.id ' \
                f'WHERE promotion_groupon.spu_no="{spu_no}"'
        self.eshop_biz.execute(query)

    def delete_marketing_channel_channel_no(self, channel_no):
        """通过channel_no删除渠道"""
        if not channel_no:
            raise ('必须指定删除条件')
        query = f'DELETE FROM orders_marketing_channel WHERE channel_no="{channel_no}"'
        self.eshop_orders.execute(query)

    def delete_commodity_category_category_no(self, category_no):
        """通过category_no删除商品类目"""
        if not category_no:
            raise ('必须指定删除条件')
        query = f'DELETE FROM commodity_category WHERE category_no="{category_no}"'
        self.eshop.execute(query)

    def query_commodity_category_category_no(self, category_no):
        """通过category_no查询商品类目"""
        if not category_no:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM commodity_category WHERE category_no="{category_no}"'
        res = self.eshop.query(query)
        return res

    def delete_commodity_property_code(self, code):
        """通过property_code删除商品属性"""
        if not code:
            raise ('必须指定删除条件')
        query = f'DELETE FROM commodity_property_value WHERE state !=0 and code="{code}" '
        self.eshop.execute(query)

    def query_commodity_property_code(self, code):
        """通过property_code查询商品属性"""
        if not code:
            raise ('必须指定查询条件')
        query = f'SELECT * FROM commodity_property_value WHERE code="{code}"'
        res = self.eshop.query(query)
        return res


class SaturnQuery:
    """下沉mysql数据库数据操作"""

    def __init__(self):
        self.saturn = MySQL(pre_db='saturn', db_name='omo_saturn')

    def query_tables(self, sql):
        res = self.saturn.query(sql)
        return res

    def delete_data(self, sql):
        res = self.saturn.execute(sql)
        return res

# if __name__ == '__main__':
#     dm = Domains()
#     dm.set_env_path('prod')
#     print(Domains.Env)
#     user = HwQuery()
#     # user.phone_query_user_inter(phone="123456789")
#     user.uid_query_leads_assign(uid='aed8e7d5c99048e59fd31b6e9d0c6ca0')
# eshop = EshopQuery()
# eshop.delete_order_by_user_no(user_no='c844db9d1b504022adf4c367403ed963')
# eshop.delete_promotion_record(promotion_id='DACT_1161')
# for sxu_id in range(5675, 5679):
#     eshop.delete_sxu_record(sxu_id=sxu_id)
# print(eshop.query_user_subject(user_no='f3147ab0af714b01b5fb1ef6ca1667c2'))
# eshop.delete_order_by_user_no('849455d8de954cf0a07bc26b1173dea7')
# Domains.set_env_path('fat')
# # print(Domains.Env)
# saturn = SaturnQuery()
# res = saturn.query_tables("SELECT COUNT(*) from saturn_product_col_item_map")
# print(res)
