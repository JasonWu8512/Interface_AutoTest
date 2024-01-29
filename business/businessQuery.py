# coding=utf-8
# @Time    : 2020/9/9 5:41 下午
# @Author  : keith
# @File    : businessQuery
# 命名规范 : 表名前缀一致的聚合

from config.env.domains import Domains
from utils.decorators import switch_db
from utils.middleware.mongoLib import MongoClient


class ggrCustomerRightQuery:
    """ggrCuetomerRight相关的mongo操作"""

    @switch_db("ggr_customer_rights")
    def query_table_info(self, table, **kwargs):
        # 查询mongo表数据，传递参数则不限制条数
        with MongoClient("ggr_customer_rights", table) as client:
            return client.find(kwargs) if kwargs else client.find(kwargs).limit(10)


class ghsQuery:
    """ghs相关的mongo操作"""

    @switch_db("jlgl")
    def get_stu_user_devices(self, **kwargs):
        # 查询学院设备信息
        with MongoClient("JLGL", "user_devices") as client:
            return client.find(kwargs).limit(10)

    @switch_db("jlgl")
    def query_table_info(self, table, **kwargs):
        # 查询mongo表数据，传递参数则不限制条数
        with MongoClient("JLGL", table) as client:
            return client.find(kwargs) if kwargs else client.find(kwargs).limit(10)

    @switch_db("jlgl")
    def ghs_user(self, **kwargs):
        """获取用户规划师信息"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "ghs_user") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def delete_ghs_user(self, **kwargs):
        """
        删除用户英语科目规划师绑定记录
        """
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "ghs_user") as client:
            client.delete_one(query)

    @switch_db("systemlesson")
    def delete_math_ghs_user(self, **kwargs):
        """
        删除用户思维科目规划师绑定记录
        """
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("SYSTEMLESSON", "systemUserPlanner") as client:
            client.delete_one(query)


class lessonQuery:
    """lesson相关的mongo操作"""

    @switch_db("jlgl")
    def delete_lessonbuy(self, **kwargs):
        """基于用户id删除购买课程"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "lessonbuy") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def get_lessonbuy(self, **kwargs):
        """基于用户id查询课程数据"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "lessonbuy") as client:
            return client.find_one(query)

    @switch_db('jlgl')
    def update_check_record(self, uid, kwargs: dict):
        """更新uid对应的打卡挑战记录"""
        query = {}
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "check") as client:
            client.update_one({"_id": uid}, {"$set": query}, upsert=True)

    @switch_db('jlgl')
    def delete_check_record(self, uid):
        """删除uid对应的打卡挑战记录"""
        with MongoClient("JLGL", "check") as client:
            client.delete_one({"_id": uid})

    @switch_db("jlgl")
    def update_lessonbuy_math(self, user_id, pts):
        """更新用户思维返现时间"""
        with MongoClient("JLGL", "lessonbuy") as client:
            return client.update_one(
                {"_id": user_id}, {"$set": {"MATC.K1MATC.meta.startts": pts, "MATC.K1MATC.meta.endts": pts}}
            )

    def update_lessonbuy_english(self, user_id, pts):
        """更新用户英语返现时间"""
        with MongoClient("JLGL", "lessonbuy") as client:
            return client.update_one(
                {"_id": user_id}, {"$set": {"TC.K1GETC.meta.startts": pts, "TC.K1GETC.meta.endts": pts}}
            )
class wcuserQuery:
    """wc_user相关的mongo操作"""

    @switch_db("jlgl")
    def update_wc_users(self, unionId, **kwargs):
        """根据unionId修改uid"""
        query = {}
        if not kwargs:
            raise ("必须指定修改条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
            if isinstance(value, bool) or isinstance(value, int):
                query.update({key: value})
        with MongoClient("JLGL", "wc_users") as client:
            client.update_one({"unionId": unionId}, {"$set": query})



class openuserQuery:
    """openuser相关的mongo操作"""

    @switch_db("jlgl")
    def get_openuser(self, **kwargs):
        """获取openuesr"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "openuser") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def delete_openuser(self, **kwargs):
        """删除openuesr"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "openuser") as client:
            client.delete_one(query)


class pingxxorderQuery:
    """pingxxorder相关的mongo操作"""

    @switch_db("jlgl")
    def insert_pingxxorder(self, order):
        """新增订单记录"""
        with MongoClient("JLGL", "pingxxorder") as client:
            client.insert_one(order)

    @switch_db("jlgl")
    def delete_pingxxorder(self, **kwargs):
        """删除购买订单"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "pingxxorder") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def delete_many_pingxxorder(self, uid):
        """根据uid删除该用户的所有购买订单"""
        with MongoClient("JLGL", "pingxxorder") as client:
            client.delete_many({"uid": uid})

    @switch_db("jlgl")
    def get_pingxxorder(self, **kwargs):
        """
        获取pingxxorder订单详情
        """
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "pingxxorder") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_pingxxorder_many(self, **kwargs):
        """
        获取pingxxorder订单详情
        """
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "pingxxorder") as client:
            return client.find(query)


class promoterQuery:
    """promoter相关的mongo操作"""

    @switch_db('jlgl')
    def get_promoter_own_order(self, **kwargs):
        """获取自购分佣订单记录"""
        query = {}
        if not kwargs:
            raise ('必须指定查询条件')
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_own_order") as client:
            return client.find(query)

    @switch_db("jlgl")
    def get_promoter_accounts(self, **kwargs):
        """获取推广人账号"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_accounts") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def update_promoter_accounts(self, promoterId, **kwargs):
        """根据推广人id修改推广人信息"""
        query = {}
        if not kwargs:
            raise ("必须指定修改条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
            if isinstance(value, bool) or isinstance(value, int):
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_accounts") as client:
            client.update_one({"_id": promoterId}, {"$set": query})

    @switch_db("jlgl")
    def replace_promoter_accounts(self, promoterId, promoter):
        """替换推广人信息，用于新增部分字段"""
        with MongoClient("XSHARE", "promoter_accounts") as client:
            client.replace_one({"_id": promoterId}, promoter)

    @switch_db("jlgl")
    def insert_promoter_accounts(self, promoterAccount):
        """
        插入推广人账号数据
        """
        with MongoClient("XSHARE", "promoter_accounts") as client:
            client.insert_one(promoterAccount)

    @switch_db("jlgl")
    def delete_promoter_accounts(self, **kwargs):
        """删除推广人账号信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_accounts") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def get_promoter_users(self, **kwargs):
        """获取推广人账号"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_users") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def update_promoter_users(self, promoterId, **kwargs):
        """根据推广人id修改推广人信息"""
        query = {}
        if not kwargs:
            raise ("必须指定修改条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_users") as client:
            client.update_one({"_id": promoterId}, {"$set": query})

    @switch_db("jlgl")
    def replace_promoter_users(self, promoterId, promoter):
        """
        替换promoter_users推广人，用于新增部分字段
        """
        with MongoClient("XSHARE", "promoter_users") as client:
            client.replace_one({"_id": promoterId}, promoter)

    @switch_db("jlgl")
    def insert_promoter_users(self, promoterUser):
        """
        插入推广人账号数据
        """
        with MongoClient("XSHARE", "promoter_users") as client:
            client.insert_one(promoterUser)

    @switch_db("jlgl")
    def delete_promoter_users(self, **kwargs):
        """删除推广人账号信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_users") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def get_promoter_wechat(self, **kwargs):
        """获取推广人微信绑定记录"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_wechat") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def insert_promoter_wechat(self, promoterWechat):
        """
        插入推广人微信绑定数据
        """
        with MongoClient("XSHARE", "promoter_wechat") as client:
            client.insert_one(promoterWechat)

    @switch_db("jlgl")
    def delete_promoter_wechat(self, **kwargs):
        """删除推广人账号信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_wechat") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def delete_promoter_paid_bind(self, **kwargs):
        """删除首购信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_paid_bind") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def get_promoter_fans(self, **kwargs):
        """获取推广人粉丝记录"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_relationship") as client:
            return client.find(query)

    @switch_db("jlgl")
    def get_promoter_history_fans(self, **kwargs):
        """获取老表推广人粉丝记录"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "promoter_fans") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_promoter_banner(self, **kwargs):
        """获取推广人banner信息"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_banner") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_promoter_order(self, **kwargs):
        """获取分佣订单记录"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_order") as client:
            return client.find(query)

    @switch_db("jlgl")
    def delete_promoter_order(self, **kwargs):
        """删除分佣信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_order") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def delete_promoter_status_log(self, **kwargs):
        """删除推广人登陆信息"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_status_log") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def get_promoter_withdraw(self, **kwargs):
        """获取提现记录"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promoter_withdraw") as client:
            return client.find_one(query)


class promotionQuery:
    """promotion相关的mongo操作"""

    @switch_db("jlgl")
    def delete_promotion_activity(self, **kwargs):
        """删除活动"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "promotion_activity") as client:
            client.delete_one(query)

    @switch_db("jlgl")
    def delete_promotion_activity_group(self, **kwargs):
        """删除拼团"""
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
                print(query)
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            client.delete_one(query)


class usersQuery:
    """users相关的mongo操作"""

    @switch_db("jlgl")
    def get_users(self, **kwargs):
        """获取用户信息"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "users") as client:
            return client.find_one(query)
    @switch_db('jlgl')
    def update_users_guadouBalance(self, uid, guadouBalance):
        """更新users表的guadouBalance"""
        with MongoClient("JLGL", "users") as client:
            return client.update_one({"_id": uid}, {"$set": {"guadouBalance": guadouBalance}})

    @switch_db("jlgl")
    def get_point_order(self, **kwargs):
        """获取钻石商城兑换礼品信息"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "point_order") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_point_user(self, **kwargs):
        """查point_user表钻石情况"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "point_user") as client:
            return client.find_one(query)

    @switch_db('jlgl')
    def update_point_user_num(self, uid):
        """更新point_user表的num"""
        with MongoClient("JLGL", "point_user") as client:
            return client.update_one({"_id": uid}, {"$set": {"items": {}}})

    # @switch_db('jlgl')
    # def update_user_addr(self, uid):
    #     """更新users表的地址为空"""
    #     with MongoClient("JLGL", "users") as client:
    #         return client.update_one({"_id":uid},{"$set":{"addr":{},"name":{},"region":{},"tel":{}}})

    @switch_db('jlgl')
    def update_cdks(self, itemid):
        """更新cdks表的status"""
        with MongoClient("JLGL", "cdks") as client:
            return client.update_one({"itemid": itemid}, {"$set": {"status": True}})

    @switch_db("jlgl")
    def get_user_flags(self, **kwargs):
        """查询user_flags表用户标签"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("JLGL", "user_flags") as client:
            return client.find_one(query)


class xshareQuery:
    """xshare相关的mongo操作"""

    @switch_db("jlgl")
    def delete_xshare_group_purchase(self, **kwargs):
        """
        删除团单
        """
        query = {}
        if not kwargs:
            raise ("必须指定删除条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            client.delete_many(query)

    @switch_db("jlgl")
    def delete_xshare_group_purchase_many(self, **kwargs):
        """
        删除满足条件所有团单
        """
        query = {}
        if not kwargs:
            raise ('必须指定删除条件')
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            client.delete_many(query)

    @switch_db("jlgl")
    def get_xshare_group_purchase(self, **kwargs):
        """
        查询团单
        """
        query = {}
        if not kwargs:
            raise ("必须指定查询件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_many_xshare_group_purchase(self, **kwargs):
        """
        查询团单多条记录
        """
        query = {}
        if not kwargs:
            raise ("必须指定查询件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            return client.find(query)

    @switch_db("jlgl")
    def update_xshare_group_purchase(self, _id, kwargs: dict):
        """根据团单id修改团单"""
        query = {}
        if not _id:
            raise ("必须指定修改条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_group_purchase") as client:
            client.update_one({"_id": _id}, {"$set": query})

    @switch_db("jlgl")
    def get_pintuan_config(self, **kwargs):
        """
        查询团单配置
        """
        query = {}
        if not kwargs:
            raise ("必须指定查询件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "pintuan_config") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def get_xshare_common_config(self, **kwargs):
        """获取配置"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_common_config") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def delete_xshare_common_config(self, plan_id):
        """删除投放计划下所有配置"""
        with MongoClient("XSHARE", "xshare_common_config") as client:
            for id in plan_id:
                client.delete_many({"campaign": id})

    @switch_db("jlgl")
    def get_xshare_advertising_plan(self, **kwargs):
        """获取投放计划"""
        query = {}
        if not kwargs:
            raise ("必须指定查询条件")
        for key, value in kwargs.items():
            if value:
                query.update({key: value})
        with MongoClient("XSHARE", "xshare_advertising_plan") as client:
            return client.find_one(query)

    @switch_db("jlgl")
    def delete_xshare_advertising_plan(self, plan_id):
        """删除投放计划"""
        with MongoClient("XSHARE", "xshare_advertising_plan") as client:
            for id in plan_id:
                client.delete_one({"campaign": id})

    @switch_db("jlgl")
    def get_tutor_bind_period(self, uid):
        """查班主任绑定情况"""
        with MongoClient("XSHARE", "tutor_bind_subject") as client:
            return client.find({"uid": uid})

    @switch_db("jlgl")
    def update_tutor_bind_period(self, uid, period, subjectType):
        """修改运营期结束时间"""
        with MongoClient("XSHARE", "tutor_bind_subject") as client:
            client.update({"uid": uid, "subjectType": subjectType}, {"$set": {"performance_period": period}})
            return client.find({"uid": uid})

    @switch_db("jlgl")
    def delete_tutor_bind_subject(self, uid):
        """删除用户在班主任绑定表的信息"""
        with MongoClient("XSHARE", "tutor_bind_subject") as client:
            return client.delete_many({"uid": uid})

    @switch_db("jlgl")
    def delete_sms_task(self, uid):
        """删除用户的所有短信任务"""
        with MongoClient("JLGL", "scheduler_tasks") as client:
            return client.delete_many({"taskData.uid": uid, "_beanName": {"$regex": "smsPushTask"}})

    @switch_db("jlgl")
    def update_tutor_bind_subject(self, uid):
        """更新班主任表绑定情况成set"""
        with MongoClient("XSHARE", "tutor_bind_subject") as client:
            return client.update({"uid": uid}, {"$set": {"status": "set"}})

    def delete_xshare_screenshot_history(self, user_id):
        """删除用户历史上传记录"""
        with MongoClient("XSHARE", "xshare_screenshot_history") as client:
            client.delete_one({"uid": user_id})

    @switch_db("jlgl")
    def select_xshare_record(self, user_id):
        """查询用户返现数据"""
        with MongoClient("JLGL", "xshare_record") as client:
            return client.find_one({"initiator": user_id})

    @switch_db("jlgl")
    def update_xshare_record(self, user_id):
        """更新用户返现状态为未返现"""
        with MongoClient("JLGL", "xshare_record") as client:
            client.update_one({"initiator": user_id}, {"$set": {"cashbackHistory": {}}})

    @switch_db("jlgl")
    def select_user_flags(self, user_id):
        """查询用户完课数据"""
        with MongoClient("JLGL", "user_flags") as client:
            return client.find_one({"_id": user_id})

    @switch_db("jlgl")
    def insert_user_flags(self, cashbackData):
        """插入用户完课数据"""
        with MongoClient("JLGL", "user_flags") as client:
            client.insert_one(cashbackData)

    @switch_db("jlgl")
    def update_user_flags(self, user_id, data):
        """更新用户完课数据"""
        with MongoClient("JLGL", "user_flags") as client:
            return client.update_one({"_id": user_id}, {"$set": {"cashback_tc": data}})


if __name__ == "__main__":
    dm = Domains()
    dm.set_env_path("fat")
    dm.set_domain("https://fat.jiliguala.com")
    # print(dm.domain)
    # db = promoterQuery()
    # re = db.get_promoter_accounts(_id='JLGL_DP_12063')
    # print(re)
    # db = configQuery()
    # re = db.get_plan_status('27')
    # db.delete_config_channel(['27'])
    # user = ApiUser()
    # user.get_token(typ='mobile', u=18818207214, p=123456)
    # user.api_wechat_app_login("wx18f8075163853984")
    # db.delete_pingxxorder_by_unionid(unionId='o0QSN1eLR21raleJbIEAIdQUKTRQ')
    # print(db.delete_lessonbuy_by_unionid('o0QSN1eLR21raleJbIEAIdQUKTRQ'))
    # db.delete_openuser_by_mobile("13818207214")
    # datd = ghsQuery().get_stu_user_devices(_id='5c8dc30c47fb405282fb89a109f86160')
    # print(datd[0])
    # a=xshareQuery().update_xshare_group_purchase('60750f71d7a2de7271359da4',{'ets':'cts'})
    # b=xshareQuery().delete_xshare_group_purchase(gpid='DACT_998')
    b = xshareQuery().insert_user_flags(
        {"_id": "c3925965514e4bdb9d5f2788b56e5de4", "cashback_tc": {"K1GE": {"K1GEE03": 5}}}
    )
