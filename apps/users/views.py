# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
import re

from flask import Blueprint, jsonify, request, g
from flask_pydantic_spec import Response as fp_Response

from auth import create_jwt, login_required
from extension import swagger
from nosql_db import r
from .models import User
from .validate import (LoginValidate, RegisterValidate, EditMaterial,
                       EditPassword, ValToken)

bp = Blueprint("users", __name__)


# 登录
@bp.post("/passport/login")
@swagger.validate(body=LoginValidate,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.find_one({"username": username, "password": password})
    if user:
        token_jwt = create_jwt(username, password)
        r.setex(username, 7 * 24 * 60 * 60, token_jwt)
        nick_name = user["name"]
        user_id = user["id"]
        data = {"nickName": nick_name,
                "name": username,
                "userId": user_id,
                "token": token_jwt}
        return jsonify({
            "code": 200,
            "message": "成功",
            "data": data,
            "ok": True
        })

    return jsonify({
        "code": 404,
        "message": "抱歉，查无此人！",
        "data": None,
        "ok": False

    })


# 用户登录成功后获取用户信息的接口
@bp.get("/passport/auth/getUserInfo")
@login_required
@swagger.validate(headers=ValToken,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def get_user_info():
    username = g.username
    user = User.find_one({"username": username})
    data = {
        "id": user["id"],
        "loginName": user["username"],
        "nickName": user["name"],
        "password": user["password"],
        "name": user["username"],
        "phoneNum": user["phone_number"],
        "email": user["email"],
        "headImg": "http://127.0.0.1:8000/static/head_image/BluSky.png",
        "userLevel": "1"
    }
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "Ok": True
    })


# 用户退出登录后清除用户信息的接口
@bp.get("/passport/logout")
@login_required
@swagger.validate(headers=ValToken,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def logout():

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": None,
        "ok": True
    })


# 注册
@bp.post("/passport/register")
@swagger.validate(body=RegisterValidate, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def register():
    username = request.json.get("username")
    phone_number = request.json.get("phone")
    password = request.json.get("password")
    nick_name = request.json.get("nickName")
    age = request.json.get("age")
    wallet_address = request.json.get("wallet_address")
    email = request.json.get("email")

    # 创建一个自增长id
    id_list = list(User.find().sort("id", -1))
    id = id_list[0]["id"] + 1
    info = {"id": id, "username": username,
            "password": password, "name": nick_name,
            "phone_number": phone_number, "age": age,
            "wallet_address": wallet_address, "email": email}
    User.insert_one(info)

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": None,
        "ok": True
    })


# 获取注册验证码的接口
@bp.get("/passport/sendCode/<string:phone>")
@swagger.validate(resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def send_code_phone(phone):
    ret = re.match(r'^1[356789]\d{9}$', phone)
    if not ret:
        return jsonify({
            "code": 201,
            "message": "抱歉，手机号格式不正确！",
            "ok": False
        })

    # 暂时生成随机验证码
    random_code = "".join([chr(random.randrange(ord('0'), ord('9') + 1)) for _ in range(6)])
    # 使用redis存储随机验证码
    r.setex(phone, 60 * 5, random_code)

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": random_code,
        "ok": True
    })


# 修改用户资料
@bp.put("/edit_material")
@login_required
@swagger.validate(headers=ValToken, body=EditMaterial,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def edit_material():
    info = request.get_json()
    for k in info:
        User.update_one({"username": g.username},
                        {"$set": {k: info[k]}})

    return jsonify({
                    "code": 200,
                    "msg": "用户信息修改成功!",
                    "data": None,
                    "ok": True
                    })


@bp.put("/edit_password")
@login_required
@swagger.validate(headers=ValToken, body=EditPassword,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['users'])
def edit_password():
    password_new = request.json.get("password_new")
    User.update_one({"username": g.username}, {"$set": {"password": password_new}})

    return jsonify({
                    "code": 200,
                    "msg": "亲，密码修改成功！！",
                    "data": None,
                    "ok": True
                    })





