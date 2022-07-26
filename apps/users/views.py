# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json

import jwt
import requests

from jwt import exceptions
from apps import create_jwt, login_required
from apps.db import r
from apps.error import ApiError
from .models import User
from .validate import LoginValidate, RegisterValidate, EditMaterial
from flask import Blueprint, jsonify, request, g
from pydantic import error_wrappers
# from flask_login import login_required, logout_user

bp = Blueprint("users", __name__)


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

        token_jwt = create_jwt(username, password)
        r.setex(username, 60*60, token_jwt)

        user = User.find_one({"username": username, "password": password})
        print(user)
        if user:
            return jsonify({"msg": "恭喜你登录成功"})
    return jsonify({"msg": "查无此人"})


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
def edit_material():
    try:
        EditMaterial(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        username = request.json.get("username")
        phone_number = request.json.get("phone_number")
        email = request.json.get("email")

        User.update_one({"username": username}, {"$set": {"username"}})

    return jsonify({"msg": "用户信息修改成功!"})


@bp.route("/edit_password")
def edit_password():

    return jsonify({})