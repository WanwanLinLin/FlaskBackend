# -*- coding: utf-8 -*-
# 后台管理系统的用户表
from db import Base
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class AdminUser(Base):
    __tablename__ = "AdminUser"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=True, default=None)
    encrypt_password = Column(String(255), default="", nullable=False)
    level = Column(String(15))

    def set_password(self, password: str):
        self.encrypt_password = generate_password_hash(
            password, method="pbkdf2:sha512", salt_length=64
        )

    def check_password(self, value):
        return check_password_hash(self.encrypt_password, value)
