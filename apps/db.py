# -*- coding: utf-8 -*-
# 初始化并使用 postgresql
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})


def init_database(app):
    # 本地测试链接
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:linwan@localhost:5432/Flask_Vue'
    # 线上服务器链接
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@address:port/db_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)