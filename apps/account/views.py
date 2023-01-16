# -*- coding: utf-8 -*-
"""
后台管理系统权限的视图函数
"""
import logging
import random
import string

import click
from flask import Blueprint, jsonify, current_app, request, g
from flask.cli import AppGroup
from flask_pydantic_spec import Response as fp_Response

from auth import permission_required
from db import SessionLocal
from nosql_db import r_3
from extension import swagger
from .models import AdminUser
from .validate import ValAdminLogin, XApiKey

bp = Blueprint("account", __name__)

user_cli = AppGroup('admin')

logging.basicConfig(level=logging.INFO)     # 配置日志
session = SessionLocal()


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
        logging.info("Incomplete parameters !")
        return
    admin_user = AdminUser(username=username,
                           encrypt_password=encrypt_password,
                           level=level)
    # 对管理员的密码进行加密
    admin_user.set_password(encrypt_password)
    session = SessionLocal()
    try:
        session.add(admin_user)
        session.commit()
        x_api_key = get_x_api_key()
        r_3.setex(username, 60 * 60 * 24 * 30 * 2, x_api_key)
        r_3.setex(x_api_key, 60 * 60 * 24 * 30 * 2, username)
    except Exception as e:
        current_app.logger.error(e)
        session.rollback()
        logging.info('error: Database save failed!')
        return

    logging.info('Successfully created super administrator!')


# 后台管理员登录的接口
@bp.post("/acl/index/login")
@swagger.validate(body=ValAdminLogin,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin'])
def admin_login():
    username = request.json.get("username")
    encrypt_password = request.json.get("encrypt_password")
    info = session.query(AdminUser).filter(AdminUser.username == username).first()
    try:
        assert info.check_password(encrypt_password)
    except Exception as e:
        return jsonify({
            "code": 203,
            "message": "Sorry, your account or password is wrong！!",
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
@bp.get("acl/index/info")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin'])
def get_admin_info():
    username = g.admin_username
    info = session.query(AdminUser).filter(AdminUser.username == username).first()
    data = {
        "name": info.username,
        "encrypt_password": info.encrypt_password,
        "level": info.level,
        "avatar": "http://127.0.0.1:8000/static/head_image/BlueSky.png"
    }
    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": data,
        "ok": True
    })


# 后台管理系统退出登录的接口
@bp.get("/acl/index/logout")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin'])
def admin_logout():
    return jsonify({
        "code": 200,
        "message": "退出登录成功！",
        "data": None,
        "ok": True
    })
