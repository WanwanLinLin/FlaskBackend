# -*- coding: utf-8 -*-
from .models import Goods_trademark
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator


class SaveTrademark(BaseModel):
    tmName: str
    logoUrl: str

    # 验证品牌名是否重复
    @validator("tmName")
    def val_tm_name(cls, v):
        info = Goods_trademark.find_one({"tmName": v})
        if info:
            raise ValueError("抱歉，品牌名不能重复！")
        return v


class UpdateTrademark(BaseModel):
    id: int
    tmName: str
    logoUrl: str
