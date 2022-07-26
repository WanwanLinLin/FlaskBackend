# -*- coding: utf-8 -*-
from apps.goods import Goods_se_attrs
from typing import Optional, List, Dict
from pydantic import BaseModel, validator


class SaveAttrInfo(BaseModel):
    attrValueList: List[dict]
    categoryId: str
    categoryLevel: int
    attrName: str

