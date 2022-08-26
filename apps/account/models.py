# -*- coding: utf-8 -*-
# 后台管理系统的用户表
from apps import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class AdminUser(db.Model):
    __tablename__ = "AdminUser"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, nullable=True, default=None)
    encrypt_password = db.Column(db.String(255), default="", nullable=False)
    level = db.Column(db.String(15))

    def set_password(self, password: str):
        self.encrypt_password = generate_password_hash(
            password, method="pbkdf2:sha512", salt_length=64
        )

    def check_password(self, value):
        return check_password_hash(self.encrypt_password, value)
