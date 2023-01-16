# -*- coding: utf-8 -*-
from .validate import SaveAttrInfo, XApiKey
from pydantic import error_wrappers
from flask import Blueprint, request, jsonify
from auth import permission_required
from extension import swagger
from flask_pydantic_spec import Response as fp_Response
from goods import Goods_se_attrs
from goods import CategoryListModel, SeCategoryListModel, ThCategoryListModel
from db import SessionLocal

bp = Blueprint("admin_category_management", __name__)
session = SessionLocal()

# 获取商品一级分类的接口
@bp.get("/getCategory1")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def get_category1():
    category1_info = session.query(CategoryListModel).all()
    category1_list = []

    for x_ in category1_info:
        category1_list.append({
            "id": x_.id,
            "name": x_.name
        })

    # print(category1_info)
    return jsonify({
        "code": 200,
        "message": "成功！",
        "data": category1_list,
        "ok": False
    })


# 获取商品二级分类的接口
@bp.get("/getCategory2/<int:category1_id>")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def get_category2(category1_id):
    category2_info = session.query(SeCategoryListModel).filter(SeCategoryListModel.category_par == category1_id).all()
    category2_list = []

    for x_ in category2_info:
        category2_list.append({
            "id": x_.id,
            "name": x_.name
        })
    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": category2_list,
        "ok": True
    })


# 获取商品三级分类的接口
@bp.get("/getCategory3/<int:category2_id>")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def get_category3(category2_id):
    category3_info = session.query(ThCategoryListModel).filter(ThCategoryListModel.category_par == category2_id).all()
    category3_list = []

    for x_ in category3_info:
        category3_list.append({
            "id": x_.id,
            "name": x_.name
        })
    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": category3_list,
        "ok": True
    })


# 获取商品属性的接口
@bp.get("/attrInfoList/<int:category1_id>/<int:category2_id>/<int:category3_id>")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def get_attr_info_list(category1_id, category2_id, category3_id):
    category3_id = str(category3_id)
    data = []
    attr_list = Goods_se_attrs.find({"connect_category3Id": category3_id}, {"_id": 0})
    for i, x_ in enumerate(attr_list, start=1):
        attr_value_list = []
        for j, y_ in enumerate(x_["attrValueList"], start=1):
            attr_value_list.append({
                "id": j,
                "valueName": y_,
                "attrId": x_["attrId"]
            })

        data.append({
            "id": x_["id"],
            "attrName": x_["attrName"],
            "categoryId": category3_id,
            "categoryLevel": 3,
            "attrValueList": attr_value_list
        })
    return jsonify({
        "code": 200,
        "message": "获取成功!",
        "data": data,
        "ok": True
    })


# 这个是添加属性或者修改属性的接口
@bp.post("/saveAttrInfo")
@permission_required
@swagger.validate(headers=XApiKey, body=SaveAttrInfo,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def save_attr_info():
    attr_name = request.json.get("attrName")
    attr_value_list_ = request.json.get("attrValueList")
    category_id = request.json.get("categoryId")
    category_level = request.json.get("categoryLevel")

    attr_name_list = list(Goods_se_attrs.find(
        {"connect_category3Id": category_id}, {"_id": 0}).distinct("attrName"))

    attr_value_list = []
    attr_id_list = []
    for x_ in attr_value_list_:
        if len(x_) == 2:
            attr_id_list.append(x_["attrId"])
            attr_value_list.append(x_["valueName"])
        else:
            attr_value_list.append(x_["valueName"])

    if not attr_id_list:
        # print("哈哈")
        # 此时为增加新属性的操作
        # 首先创建一个自增长的id
        id_list = list(Goods_se_attrs.find().sort("id", -1))
        if not id_list:
            id = 1
        else:
            id = id_list[0]["id"] + 1

        # 处理属性值和属性id，然后将它们插入数据库中

        # 再创建一个自增长的attrId
        attr_id_list = list(Goods_se_attrs.find().sort("attrId", -1))
        if not attr_id_list:
            attr_id = 1
        else:
            attr_id = attr_id_list[0]["attrId"] + 1

        Goods_se_attrs.insert_one({
            "attrId": attr_id,
            "attrValueList": attr_value_list,
            "attrName": attr_name,
            "id": id,
            "connect_category3Id": str(category_id),
            "category_level": str(category_level)
        })

        return jsonify({
            "code": 200,
            "message": "添加属性成功!",
            "data": None,
            "ok": True
        })

    # 此时为修改原有属性的操作
    Goods_se_attrs.update_one({"attrId": attr_id_list[0]},
                              {"$set": {
                                  "attrName": attr_name,
                                  "attrValueList": attr_value_list,
                              }})

    return jsonify({
        "code": 200,
        "message": "修改属性成功!",
        "data": None,
        "ok": True
    })


# 这是删除属性的接口
@bp.get("/deleteAttr/<int:attr_id>")
@permission_required
@swagger.validate(headers=XApiKey,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage category'])
def delete_attr(attr_id):
    Goods_se_attrs.delete_one({"attrId": attr_id})
    return jsonify({
        "code": 200,
        "message": "属性删除成功!",
        "data": None,
        "ok": True
    })
