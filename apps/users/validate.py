# -*- coding: utf-8 -*-
from .models import User
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator


class LoginValidate(BaseModel):
    username: str
    password: int

    @validator("username")
    def three_fifteen(cls, v):
        if len(v) < 3 or len(v) > 15:
            raise ValueError('用户名过长或过短!')
        return v.title()

    @validator("password")
    def three_twenty(cls, v):
        if len(str(v)) < 3 or len(str(v)) > 20:
            raise ValueError('密码过长或过短!')
        return v


class RegisterValidate(BaseModel):
    username: str
    password: int
    name: str
    age: int
    wallet_address: str

    @validator("password")
    def three_twenty(cls, v):
        if len(str(v)) < 3 or len(str(v)) > 20:
            raise ValueError('密码过长或过短!')
        return v

    @validator("wallet_address")
    def ten_thirty(cls, v):
        if len(v) < 10 or len(v) > 30:
            raise ValueError('钱包地址过长或过短!')
        return v

    @validator("username")
    def no_repeated(cls, v):
        user = User.find_one({"username": v})
        if user:
            raise ValueError("抱歉，用户名不能重复")
        if len(v) < 3 or len(v) > 15:
            raise ValueError('用户名过长或过短!')
        return v.title()