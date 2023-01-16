# -*- coding: utf-8 -*-
import re

from typing import Optional
from pydantic import BaseModel, validator, Field


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


class SubmitOrder(BaseModel):
    consignee: str
    consigneeTel: str = Field(min_length=11)
    deliveryAddress: str
    paymentWay: str
    orderComment: str
    orderDetailList: list


class Header(BaseModel):
    Token: str


class SubmitOrderQuery(BaseModel):
    tradeNo: str

