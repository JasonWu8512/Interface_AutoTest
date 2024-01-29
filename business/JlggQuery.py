"""
=========
Author:Lisa
time:2022/7/12 5:41 下午
=========
"""

from config.env.domains import Domains
from utils.middleware.dbLib import MySQL


class JlggGuery:
    """JLGG业务相关的mysql操作"""

    def __init__(self):
        self.user = MySQL(pre_db='tiga', db_name='tiga')

    def query_inter_user(self, sql):
        res = self.user.query(sql)
        return res

    def delete_inter_user(self, uid):
        """删除bid对应的分流结果"""
        if not uid:
            raise ('必须指定删除条件')
        query = f'DELETE FROM inter_user WHERE uid="{uid}"'
        self.user.execute(query)


if __name__ == '__main__':
    Domains.set_env_path('fat')
    strategy = JlggGuery()
    # res = strategy.query_user_strategty(
    #     'SELECT * FROM user_strategy.user_strategy where baby_id="316315f791e84bab87e59f0b7aac1f14" order by phase asc; ')
    res = strategy.delete_inter_user("3b6cf5a898e14ee3b61759d35781a99f")
    print(res)
