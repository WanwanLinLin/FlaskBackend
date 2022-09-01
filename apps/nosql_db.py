# -*- coding: utf-8 -*-
import pymongo, redis

# 本地服务器
client = pymongo.MongoClient("mongodb://localhost/", 27017)
# 线上服务器
# client = pymongo.MongoClient("mongodb://root:***********@39.108.51.219:****/")
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=3, decode_responses=True)
pool_2 = redis.ConnectionPool(host="127.0.0.1", port=6379, db=2, decode_responses=True)
pool_3 = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1, decode_responses=True)

# 连接 redis 数据库
# 用于存储jwt_token
r = redis.Redis(connection_pool=pool)
# 用于存储提交订单的信息
r_2 = redis.Redis(connection_pool=pool_2)
# 用户存储后台管理人员的X-API-KEY
r_3 = redis.Redis(connection_pool=pool_3)

