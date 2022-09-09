# -*- coding: utf-8 -*-
from typing import Optional, List
from pydantic import BaseModel, validator, Field


class SaveSkuInfo(BaseModel):
    category3Id: str
    spuId: int
    tmId: int
    skuName: str
    price: str
    weight: str
    skuDesc: str
    skuDefaultImg: str
    skuImageList: List[dict]
    skuAttrValueList: List[dict]
    skuSaleAttrValueList: List[dict]