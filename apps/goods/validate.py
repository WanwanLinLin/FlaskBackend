# -*- coding: utf-8 -*-
from enum import Enum
from typing import Optional
from pydantic import BaseModel, validator, Field
from .models import Goods_se, CategoryListModel, SeCategoryListModel, ThCategoryListModel
from db import SessionLocal

session = SessionLocal()


class VaListModel(BaseModel):
    category1Id: Optional[str]
    category2Id: Optional[str]
    category3Id: Optional[str]
    categoryName: Optional[str]
    keyword: Optional[str]
    props: Optional[list]
    trademark: Optional[str]
    order: Optional[str]
    pageNo: Optional[int]
    pageSize: Optional[int]

    @validator("category1Id")
    def is_exists(cls, v):
        # v 为 " " 的情况
        if not v:
            return v.title()
        data = session.query(CategoryListModel).filter(CategoryListModel.id == int(v)).first()
        if not data:
            raise ValueError("抱歉，该一级类目的Id不存在！")
        return v.title()

    @validator("category2Id")
    def is_exists2(cls, v):
        # v 为 " " 的情况
        if not v:
            return v.title()
        data = session.query(SeCategoryListModel).filter(SeCategoryListModel.id == int(v)).first()
        if not data:
            raise ValueError("抱歉，该二级类目的Id不存在！")
        return v.title()

    @validator("category3Id")
    def is_exists3(cls, v):
        # v 为 " " 的情况
        if not v:
            return v.title()
        data = session.query(ThCategoryListModel).filter(ThCategoryListModel.id == int(v)).first()
        if not data:
            raise ValueError("抱歉，该一级类目的Id不存在！")
        return v.title()

    @validator("pageNo")
    def is_reasonable(cls, v):
        if v <= 0:
            raise ValueError("抱歉！页码数应该大于0！")
        return v

    @validator("pageSize")
    def is_reasonable2(cls, v):
        if v <= 0:
            raise ValueError("抱歉！每页条数应该大于0！")
        return v

