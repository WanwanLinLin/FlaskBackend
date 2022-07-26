# -*- coding: utf-8 -*-
import pymongo, redis

client = pymongo.MongoClient("mongodb://localhost/", 27017)
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=3, decode_responses=True)

# 连接 redis 数据库
r = redis.Redis(connection_pool=pool)