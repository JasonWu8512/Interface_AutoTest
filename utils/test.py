# # coding=utf-8
# # @Time    : 2020/7/31 3:30 下午
# # @Author  : keith
# # @File    : test
# from pymongo import MongoClient
# import pymysql
#
#
# class Database:
#     def __init__(self, address, port, database, user, password):
#         self.mongo_connect = "mongodb://{}:{}@{}:{}/{}".format(
#             user, password, address, port, database
#         )
#
#     def get_client(self):
#         dev_client = MongoClient(self.mongo_connect)
#         return dev_client


# if __name__ == "__main__":
#     db = Database(
#         address="10.19.6.171",
#         port=27646,
#         database="JLGL",
#         user="TESTReadonly",
#         password="443898dc456c2b66bc33f85ecbf15d9b",
#     )
#     # client
#     db = db.get_client()["JLgl"]
#     collections = db.list_collection_names()
#     print(collections)

# 1.连接MySQL
import pymysql
import sqlparse as sqlparse


conn = pymysql.connect ( host="10.161.112.11", port=3306, user="user", passwd="jkP0*2u#zdYXvcD7", charset="utf8", db='user' )
cursor = conn.cursor ( cursor=pymysql.cursors.DictCursor )  # 游标

# 2.发送指令
sql=cursor.execute ( "select * from inter_user limit 10" )
parsed = sqlparse.parse(sql)

conn.commit ()  # 提交指令
statement = parsed[0]



# 3.关闭
cursor.close ()

