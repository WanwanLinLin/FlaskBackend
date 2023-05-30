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
    x_api_key = get_x_api_key()
    r_3.setex("Julia", 60 * 60 * 24 * 30 * 2, x_api_key)
    r_3.setex(x_api_key, 60 * 60 * 24 * 30 * 2, "Julia")
except Exception as e:
    # current_app.logger.error(e)
    print(e)