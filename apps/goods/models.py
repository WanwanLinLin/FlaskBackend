# -*- coding: utf-8 -*-
from apps.nosql_db import client
from flask_sqlalchemy import SQLAlchemy
from apps import db

# 订单集合
Goods = client.goods.Goods

# 商品分类详情集合
Goods_se = client.goods.Goods_se

# 某个商品的属性集合
Goods_se_attrs = client.goods.Goods_se_attrs

# 某个商品的详细信息的集合SPU
Goods_se_details = client.goods.Goods_se_details

# 某个商品的详细信息的集合SKU
Goods_se_details_sku = client.goods.Goods_se_details_sku


# 一级商品列表模型
class CategoryListModel(db.Model):
    __tablename__ = "first-level-table"

    id = db.Column(db.Integer, primary_key=True, comment="一级表主键")
    name = db.Column(db.String(64), unique=True, comment="一级类目名称")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"


# 二级商品列表模型
class SeCategoryListModel(db.Model):
    __tablename__ = "second-level-table"

    id = db.Column(db.Integer, primary_key=True, comment="二级表主键")
    name = db.Column(db.String(64), unique=True, comment="二级类目名称")
    category_par = db.Column(db.Integer, db.ForeignKey("first-level-table.id"))
    categoryListModel = db.relationship("CategoryListModel", backref="my_CategoryListModel")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"


# 三级商品列表模型
class ThCategoryListModel(db.Model):
    __tablename__ = "third-level-table"

    id = db.Column(db.Integer, primary_key=True, comment="三级表主键")
    name = db.Column(db.String(64), unique=True, comment="三级类目名称")
    category_par = db.Column(db.Integer, db.ForeignKey("second-level-table.id"))
    seCategoryListModel = db.relationship("SeCategoryListModel", backref="my_SeCategoryListModel")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"





