# -*- coding: utf-8 -*-
from goods import Goods_se_attrs
from typing import Optional, List, Dict
from pydantic import BaseModel, validator


class SaveAttrInfo(BaseModel):
    attrValueList: List[dict]
    categoryId: str
    categoryLevel: int
    attrName: str


class XApiKey(BaseModel):
    Xapikey: str


class AddCategory(BaseModel):
    category1: str = None
    category2: str = None
    category3: str = None

