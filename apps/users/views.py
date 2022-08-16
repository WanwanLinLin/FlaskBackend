# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
import random
import requests

from apps import create_jwt, login_required
from apps.nosql_db import r
from apps.error import ApiError
from .models import User
from .validate import (LoginValidate, RegisterValidate, EditMaterial, EditPassword)
from flask import Blueprint, jsonify, request, g
from pydantic import error_wrappers

# from flask_login import login_required, logout_user

bp = Blueprint("users", __name__)


# 登录
@bp.route("/passport/login", methods=["GET", "POST"])
def login():
    try:
        LoginValidate(**request.get_json())
    except error_wrappers.ValidationError as e:
        return e.json()
    else:
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
@bp.route("/passport/auth/getUserInfo", methods=["GET", "POST"])
@login_required
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
        "headImg": user["headImg"],
        "userLevel": "1"
    }
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "Ok": True
    })


# 用户退出登录后清除用户信息的接口
@bp.route("/passport/logout", methods=["GET", "POST"])
@login_required
def logout():
    username = g.username
    # r.delete(username)

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": None,
        "ok": True
    })


# 注册
@bp.route("/passport/register", methods=["GET", "POST"])
def register():
    try:
        RegisterValidate(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
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
@bp.route("/passport/sendCode/<string:phone>", methods=["GET", "POST"])
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
@bp.route("/edit_material")
@login_required
def edit_material():
    try:
        EditMaterial(**request.get_json())
        # print(request.get_json())
        for k in request.get_json():
            print(k)
            print(request.get_json()[k])
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        X = request.get_json()
        for k in X:
            User.update_one({"username": g.username},
                            {"$set": {k: X[k]}})

    return jsonify({"msg": "用户信息修改成功!"})


@bp.route("/edit_password")
@login_required
def edit_password():
    try:
        EditPassword(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        password_new = request.json.get("password_new")
        User.update_one({"username": g.username}, {"$set": {"password": password_new}})

    return jsonify({"msg": "亲，密码修改成功！！"})





