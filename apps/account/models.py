# -*- coding: utf-8 -*-
# 后台管理系统的用户表
from db import Base
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class AdminUser(Base):
    __table_args__ = {'extend_existing': True}
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


if __name__ == '__main__':
    import string, random
    from db import SessionLocal
    from nosql_db import r_3
    from flask import current_app

    # 生成一个随机的X-API-KEY用于验证后台管理人员登录
    def get_x_api_key():
        s = string.ascii_letters.upper()
        r = ["".join([random.choice(s) for _ in range(9)]) for _ in range(4)]
        return f"{r[0]}-{r[1]}-{r[2]}-{r[3]}"

    session = SessionLocal()
    admin_user = AdminUser(username="Julia",
                           encrypt_password="Julia",
                           level=1)
    # 对管理员的密码进行加密
    admin_user.set_password("Julia")
    try:
        session.add(admin_user)
        session.commit()
        x_api_key = get_x_api_key()
        r_3.setex("Julia", 60 * 60 * 24 * 30 * 2, x_api_key)
        r_3.setex(x_api_key, 60 * 60 * 24 * 30 * 2, "Julia")
    except Exception as e:
        # current_app.logger.error(e)
        session.rollback()
