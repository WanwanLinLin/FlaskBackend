# -*- coding: utf-8 -*-
"""
后台管理系统权限的视图函数
"""
import click
import random
import string
from apps import db
from .models import AdminUser
from .validate import ValAdminLogin
from apps.nosql_db import r_3
from apps.auth import permission_required
from flask.cli import AppGroup
from flask import Blueprint, jsonify, current_app, request, g
from pydantic import error_wrappers

bp = Blueprint("account", __name__)

user_cli = AppGroup('admin')


# 生成一个随机的X-API-KEY用于验证后台管理人员登录
def get_x_api_key():
    s = string.ascii_letters.upper()
    r = ["".join([random.choice(s) for _ in range(9)]) for _ in range(4)]
    return f"{r[0]}-{r[1]}-{r[2]}-{r[3]}"


@user_cli.command('createAdminUser')
@click.argument("username", required=True)
@click.argument("encrypt_password", required=True)
@click.argument("level", required=True)
def create_admin_user(username, encrypt_password, level):
    if not all([username, encrypt_password, level]):
        print("参数不齐全")
        return
    admin_user = AdminUser(username=username,
                           encrypt_password=encrypt_password,
                           level=level)
    # 对管理员的密码进行加密
    admin_user.set_password(encrypt_password)
    try:
        db.session.add(admin_user)
        db.session.commit()
        x_api_key = get_x_api_key()
        r_3.setex(username, 60 * 60 * 24 * 30, x_api_key)
        r_3.setex(x_api_key, 60 * 60 * 24 * 30, username)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        print("数据库保存错误")
        return

    print("超级管理员创建成功！")


# 后台管理员登录的接口
@bp.route("/acl/index/login", methods=["GET", "POST"])
def admin_login():
    try:
        ValAdminLogin(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    username = request.json.get("username")
    encrypt_password = request.json.get("encrypt_password")
    info = AdminUser.query.filter(AdminUser.username == username).first()
    try:
        assert info.check_password(encrypt_password)
    except Exception as e:
        return jsonify({
            "code": 203,
            "message": "账号或密码错误！!",
            "data": None,
            "ok": False
        })
    data = {
        "username": info.username,
        "encrypt_password": info.encrypt_password,
        "XAPIKEY": r_3.get(username)
    }
    return jsonify({
        "code": 200,
        "message": "管理员登陆成功!",
        "data": data,
        "ok": True
    })


# 获取后台管理系统人员信息的接口
@bp.route("acl/index/info", methods=["GET", "POST"])
@permission_required
def get_admin_info():
    username = g.admin_username
    info = AdminUser.query.filter(AdminUser.username == username).first()
    data = {
        "name": info.username,
        "encrypt_password": info.encrypt_password,
        "level": info.level,
        "avatar": "http://127.0.0.1:8000/static/head_image/BlueSky.png"
    }
    # data = {
    #     "name": "Julia",
    #     "avatar": "http://127.0.0.1:8000/static/head_image/BlueSky.png"
    # }
    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": data,
        "ok": True
    })


# 后台管理系统退出登录的接口
@bp.route("/acl/index/logout", methods=["GET", "POST"])
@permission_required
def admin_logout():
    return jsonify({
        "code": 200,
        "message": "退出登录成功！",
        "data": None,
        "ok": True
    })
