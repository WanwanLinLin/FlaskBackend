# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, validator, Field


# 验证管理员登陆的账号和密码格式
class ValAdminLogin(BaseModel):
    username: str
    encrypt_password: str

