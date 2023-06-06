# nothing to do
import string, random
from account.models import AdminUser
from db import SessionLocal
from nosql_db import r_3
from flask import current_app


# 生成一个随机的X-API-KEY用于验证后台管理人员登录
def get_x_api_key():
    s = string.ascii_letters.upper()
    r = ["".join([random.choice(s) for _ in range(9)]) for _ in range(4)]
    return f"{r[0]}-{r[1]}-{r[2]}-{r[3]}"

try:
    admin_user = AdminUser(username="Julia",
                           encrypt_password="Julia",
                           level="1")
    # 对管理员的密码进行加密
    admin_user.set_password("Julia")
    session = SessionLocal()
    session.add(admin_user)
    session.commit()
    # 设置密钥
    x_api_key = get_x_api_key()
    r_3.setex("Julia", 60 * 60 * 60 * 24 * 30 * 2, x_api_key)
    r_3.setex(x_api_key, 60 * 60 * 60 * 24 * 30 * 2, "Julia")
    print("管理员添加成功！账号：Julia ，密码：Julia")
except Exception as e:
    # current_app.logger.error(e)
    print("管理员已存在，请勿重复添加！")