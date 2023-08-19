# encoding:utf-8
import string
import random
import logging
from db import SessionLocal
from account.models import AdminUser
from pydantic import BaseModel
from nosql_db import r_3

logging.basicConfig(level=logging.INFO)     # 配置日志


class XApiKey(BaseModel):
    Xapikey: str


def get_x_api_key():
    s = string.ascii_letters.upper()
    r = ["".join([random.choice(s) for _ in range(9)]) for _ in range(4)]
    return f"{r[0]}-{r[1]}-{r[2]}-{r[3]}"


def create_admin_user(username, encrypt_password, level):
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
        session.rollback()
        logging.info('error: Database save failed!')
        return

    logging.info('Successfully created a super administrator!')


if __name__ == '__main__':
    create_admin_user("admin", "admin", "1")