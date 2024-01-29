# coding=utf-8
# @Time    : 2020/7/30 3:00 下午
# @Author  : keith
# @File    : mongoLib


import pymongo

from config.env.domains import Domains


class MongoClient:

    _record = set()

    jlgl_dev = {
        "host": "10.10.25.127",
        "port": 27646,
        # "user": "JLAdmin",
        # "password": "niuniuniu168",
        "user": "JLGLTestWrite",
        "password": "1a5e9dc80b9d4e2e39cb179cc672bc88",
    }
    jlgl_rc = {
        "host": "10.19.69.135",
        "port": 27545,
        "user": "TESTReadOnly",
        "password": "116e8e88252a6dd215b3cefdfad34d20",
    }
    jlgl_fat = {
        "host": "10.100.128.122",
        "port": 27017,
        "user": "JLAdmin",
        "password": "niuniuniu168",
    }
    ggr_dev = {
        "host": "10.10.25.127",
        "port": 27646,
        "user": "GGRTestWrite",
        "password": "87f5dd88484190fa11d5c1c1974b2136",
    }
    ggr_prod = {
        "host": "10.42.143.24",
        "port": 28545,
        "user": "a_ggr",
        "password": "p1SSD*LD#Lqe^BfZ",
    }
    systemlesson_fat = {
        "host": "10.100.128.122",
        "port": 27017,
        "user": "u_young",
        "password": "1qaz@WSX",
    }
    systemlesson_dev = {
        "host": "10.10.25.127",
        "port": 27646,
        "user": "JLAdmin",
        "password": "niuniuniu168",
    }

    # 目前就dev环境mongo
    connect_info = {
        "jlgl_dev": dict(jlgl_dev, **{"database": "JLGL"}),
        "jlgl_rc": dict(jlgl_rc, **{"database": "JLGL"}),
        "jlgl_fat": dict(jlgl_fat, **{"database": "JLGL"}),
        "ggr_dev": dict(ggr_dev, **{"database": "GGR"}),
        "ggr_fat": dict(jlgl_fat, **{"database": "GGR"}),
        "ggr_prod": dict(ggr_prod, **{"database": "GGR"}),
        "systemlesson_fat": dict(systemlesson_fat, **{"database": "SYSTEMLESSON"}),
        "systemlesson_dev": dict(systemlesson_dev, **{"database": "SYSTEMLESSON"}),
        "ggr_customer_rights_fat": dict(systemlesson_fat, **{"database": "ggr_customer_rights"})
    }

    @classmethod
    def get_mongo_setting(cls):
        connect_info = cls.connect_info.get(Domains.DbKey)
        # if "dev.jiliguala" in Domains.domain:
        #     connect_info = cls.connect_info.get("jlgl_dev")
        # elif "rc.jiliguala" in Domains.domain:
        #     connect_info = cls.connect_info.get("jlgl_rc")
        # elif "fat.jiliguala" in Domains.domain:
        #     connect_info = cls.connect_info.get("jlgl_fat")
        # elif "grr" in Domains.domain:
        #     if "dev" in Domains.domain:
        #         connect_info = cls.connect_info.get("grr_dev")
        #     elif "fat" in Domains.domain:
        #         connect_info = cls.connect_info.get("grr_fat")
        return connect_info

    def __init__(self, database, collection=None, mongo_server=None):
        """
        :param database: 需要操作的数据库
        :param collection:  需要操作的集合(表)
        :param mongo_server: 目前mongo_server不需要传入，默认是test配置
        """
        # if mongo_server and mongo_server not in ("jlgl_dev", "ggr_dev"):
        #     raise Exception("mongo_server is in (dev, prd)")
        self.database = database
        self.collection = collection if collection else None
        self.mongo_server = mongo_server
        # 如果 mongo_server为空，则默认为dev
        # self.connect = (
        #     self.connect_info.get("host")
        #     if not self.mongo_server
        #     else self.connect_info.get(mongo_server)
        # )
        self.mongo_server = self.get_mongo_setting()
        self.mongo_host = self.mongo_server.get("host")
        self.mongo_port = self.mongo_server.get("port")
        self.mongo_account = self.mongo_server.get("user")
        self.mongo_password = self.mongo_server.get("password")

    def __enter__(self):
        self.client = self.get_client(self.database)
        self._client = (
            self.client[self.database][self.collection]
            if self.collection
            else self.client[self.database]
        )
        return self._client

    def get_client(self, database):
        """ mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]] """
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port, username=self.mongo_account,
                                     password=self.mongo_password, authSource=database, authMechanism='SCRAM-SHA-1')
        return client


    @classmethod
    def return_mongo_client(cls, client):
        if cls._record:
            server = cls._record.pop()
        else:
            server = None
        client.close() if client else None
        if server:
            server.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.return_mongo_client(self.client)


if __name__ == "__main__":
    dm = Domains()
    a = dm.set_env_path('dev')
    dm.set_domain(a['url'])
    with MongoClient(database="JLGL") as client:
        print(client.list_collection_names())
        objs = client['JLGL'].find({"typ": "guest"})
        print(objs)
    # client = pymongo.MongoClient('10.10.25.127', 27646, username='JLGLTestWrite', password="1a5e9dc80b9d4e2e39cb179cc672bc88", authSource='JLGL', authMechanism='SCRAM-SHA-1')
    # print(client['JLGL'].list_collection_names())
