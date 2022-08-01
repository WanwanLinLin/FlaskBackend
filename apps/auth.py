# -*- coding: utf-8 -*-
import jwt
import datetime
import functools
from apps.nosql_db import r
from jwt import exceptions
from apps.error import ApiError
from functools import wraps
from flask import g, request, current_app, jsonify


# 构造一个密钥
SALT = "zhananbudanchou1234678"

# 构造 headers
headers = {
    "typ": "jwt",
    "alg": "HS256"
}


# 创建 JWT
def create_jwt(username, password):
    payload = {
        "username": username,
        "password": password
    }

    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256",
                        headers=headers)
    return result


def login_required(func):

    @wraps(func)
    def decorate(*args, **kwargs):
        # if hasattr(g, "username"):
        #     return g.username
        auth_jwt = request.headers.get('session-token')
        g.username = None
        try:
            "判断token的校验结果"
            payload = jwt.decode(auth_jwt, SALT, algorithms=['HS256'])
            "获取载荷中的信息赋值给g对象"
            g.username = payload.get("username")
            print(g.username)
            assert r.get(g.username) == auth_jwt
        except Exception as e:
            print(e)
            return jsonify({"err": "Token 认证失败！！!"})

        return func(*args, **kwargs)

    return decorate






