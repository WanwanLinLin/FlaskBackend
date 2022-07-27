# -*- coding: utf-8 -*-
import re

from flask import g
from .models import User
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator


class LoginValidate(BaseModel):
    username: str
    password: str

    @validator("username")
    def three_fifteen(cls, v):
        if len(v) < 3 or len(v) > 15:
            raise ValueError('用户名过长或过短!')
        return v.title()

    @validator("password")
    def three_twenty(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('密码过长或过短!')
        return v


class RegisterValidate(BaseModel):
    username: str
    password: str
    name: str
    age: int
    wallet_address: str

    @validator("password")
    def three_twenty(cls, v):
        if len(v) < 3 or len(v) > 20:
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


class EditMaterial(BaseModel):
    username: Optional[str]
    phone_number: Optional[int]
    email: Optional[str]

    @validator("username")
    def no_repeated(cls, v):
        user = User.find_one({"username": v})
        if user:
            raise ValueError("抱歉，用户名不能重复！")
        if len(v) < 3 or len(v) > 15:
            raise ValueError("抱歉，用户名过长或过短！")
        return v.title()

    @validator("phone_number")
    def match_phone_number(cls, v):
        ret = re.match(r'^1[356789]\d{9}$', str(v))
        if not ret:
            raise ValueError("抱歉，手机号格式不正确!")
        return v

    @validator("email")
    def match_email(cls, v):
        ret = re.match(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$", v)
        if not ret:
            raise ValueError("抱歉，邮箱号格式不正确！")
        return v.title()


class EditPassword(BaseModel):
    password_old: str
    password_new: str
    password_new_confirm: str

    @validator("password_old")
    def val_password_old(cls, v):
        user = User.find_one({"username": g.username})
        if user["password"] != v:
            raise ValueError("抱歉！旧密码不匹配！")
        return v.title()

    @validator("password_new")
    def val_password_new(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('密码过长或过短!')
        return v

    @validator("password_new_confirm")
    def match_password_edit(cls, v, values, **kwargs):
        if "password_new" in values and v != values["password_new"]:
            raise ValueError("抱歉，新密码与确认密码不匹配！！")
        return v


class ShippingAddress(BaseModel):
    customer_name: Optional[str]
    shipping_address: Optional[str]
    customer_number: Optional[int]
    id: Optional[int]

    @validator("customer_name")
    def val_customer_name(cls, v):
        if len(v) < 3 or len(v) > 15:
            raise ValueError("抱歉，用户名过长或过短！")
        return v.title()

    @validator("customer_number")
    def val_customer_number(cls, v):
        ret = re.match(r'^1[356789]\d{9}$', str(v))
        if not ret:
            raise ValueError("抱歉，手机号格式不正确!")
        return v

