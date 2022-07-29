# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import jwt
import requests

from jwt import exceptions
from apps import create_jwt, login_required
from apps.db import r
from apps.error import ApiError
from .models import User, Shipping_address
from .validate import (LoginValidate, RegisterValidate, EditMaterial, EditPassword,
                       ShippingAddress)
from flask import Blueprint, jsonify, request, g
from pydantic import error_wrappers
# from flask_login import login_required, logout_user

bp = Blueprint("users", __name__)


# 登录
@bp.route("/login", methods=["GET", "POST"])
@login_required
def login():
    try:
        LoginValidate(**request.get_json())
    except error_wrappers.ValidationError as e:
        return e.json()
    else:
        username = request.json.get("username")
        password = request.json.get("password")
        user = User.find_one({"username": username, "password": password})
        print(user)
        print("g.username 的值是2：", g.username)
        if g.username != username:
            return jsonify({"err": "抱歉，Token 认证失败！"})

        # 如果数据库真的有这个用户，就给ta创建对应的jwt_token
        if user:
            token_jwt = create_jwt(username, password)
            r.setex(username, 60 * 60, token_jwt)
            return jsonify({"msg": "恭喜你登录成功"})
    return jsonify({"msg": "查无此人"})


# 注册
@bp.route("/register/", methods=["GET", "POST"])
def register():
    try:
        RegisterValidate(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        username = request.json.get("username")
        password = request.json.get("password")
        name = request.json.get("name")
        age = request.json.get("age")
        wallet_address = request.json.get("wallet_address")
        email = request.json.get("email")

        # 创建一个自增长id
        id_list = list(User.find().sort("id", -1))
        id = id_list[0]["id"] + 1
        info = {"id": id, "username": username, "password": password,
                "name": name, "age": age, "wallet_address": wallet_address,
                "email": email}
        User.insert_one(info)
    return jsonify({"msg": "恭喜你注册成功！"})


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


# 查看当前用户所有的收货地址
@bp.route("/show_shipping_address", methods=["GET", "POST"])
@login_required
def show_shipping_address():
    all_shipping_address = list(Shipping_address.find({"username": g.username},
                                                 {"_id": 0}))
    if all_shipping_address:
        return jsonify({"msg": all_shipping_address})

    return jsonify({"err": "当前收货地址列表为空~"})


# 添加收货地址信息
@bp.route("/add_shipping_address", methods=["GET", "POST"])
@login_required
def add_shipping_address():
    try:
        ShippingAddress(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        # 首先获取该用户收货地址总数，看看是否超过6个
        ship_address_count = Shipping_address.count_documents({"username": g.username})
        all_ship_address = Shipping_address.count_documents({})
        if ship_address_count >5:
            return jsonify({"err": "抱歉，你已经有6个收货地址了，不能再添加更多了"})
        # 创建一个自增长id
        if ship_address_count == 0:
            id = all_ship_address + 1
        else:
            id_list = list(Shipping_address.find().sort("id", -1))
            id = id_list[0]["id"] + 1

        customer_name = request.json.get("customer_name")
        shipping_address = request.json.get("shipping_address")
        customer_number = request.json.get("customer_number")

        Shipping_address.insert_one({"id": id, "customer_name": customer_name,
                                     "shipping_address": shipping_address,
                                     "customer_number": customer_number,
                                     "username": g.username})

    return jsonify({"msg": "收货地址添加成功！！！"})


# 修改收货地址信息
@bp.route("/edit_shipping_address", methods=["GET", "POST"])
@login_required
def edit_shipping_address():
    try:
        ShippingAddress(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        id = request.json.get("id")
        user_address = Shipping_address.find_one({"id": id, "username": g.username})
        if not user_address:
            return jsonify({"err": "抱歉，该收货地址不存在！"})

        X = request.get_json()

        for k in X:
            Shipping_address.update_one({"id": id, "username": g.username},
                                        {"$set": {k: X[k]}})

    return jsonify({"msg": "收货地址信息修改成功！"})