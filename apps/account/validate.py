# -*- coding: utf-8 -*-
import pydantic
from typing import Optional
from pydantic import BaseModel, validator, Field, root_validator

# pydantic.root_validator(pre=False)


# 验证管理员登陆的账号和密码格式
class ValAdminLogin(BaseModel):
    username: str
    encrypt_password: str


class XApiKey(BaseModel):
    Xapikey: str

    # @root_validator(pre=True)
    # def no(cls, v):
    #     value = v['Xapikey']
    #     del v['Xapikey']
    #     v["XAPIKEY"] = value
    #     return v

