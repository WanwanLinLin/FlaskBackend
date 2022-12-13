# -*- coding: utf-8 -*-
import math

from db import SessionLocal
from .validate import VaListModel
from pydantic import error_wrappers
from flask import Blueprint, jsonify, request
from .models import (Goods, Goods_se_attrs, Goods_se_details_sku,
                     Goods_se_details, CategoryListModel, SeCategoryListModel, ThCategoryListModel)
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from extension import swagger

bp = Blueprint("goods", __name__)

session = SessionLocal()


# 返回所有类别列表数据(三级联动)的接口
@bp.get("/getBaseCategoryList")
# @swagger.validate(resp=Response(HTTP_200=None, HTTP_403=None), tags=['goods'])
def get_base_category_list():
    first_list = session.query(CategoryListModel).all()
    data = []

    for i, x in enumerate(first_list, start=1):
        data.append({"categoryName": x.name,
                     "categoryId": x.id,
                     "categoryChild": []})
        l = session.query(SeCategoryListModel).filter(SeCategoryListModel.category_par == x.id).all()
        if l:
            for i_, y in enumerate(l, start=1):
                data[i - 1]["categoryChild"].append({"categoryName": y.name,
                                                     "categoryId": y.id,
                                                     "categoryChild": []})
                l_ = session.query(ThCategoryListModel).filter(ThCategoryListModel.category_par == y.id).all()
                if l_:
                    for z in l_:

                        if z.category_par == y.id:
                            data[i - 1]["categoryChild"][i_ - 1]["categoryChild"].append({"categoryName": z.name,
                                                                                          "categoryId": z.id,
                                                                                          })

    return jsonify({
        "code": 200,
        "message": "成功！",
        "ok": True,
        "data": data})

# 展示商品列表的接口
@bp.post("/list")
@swagger.validate(body=VaListModel, resp=Response(HTTP_200=None, HTTP_403=None), tags=['goods'])
def list_():
    try:
        VaListModel(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    # print("request.get_json()的值是：", request.get_json())
    trademark_list = []
    attrs_list = []
    goods_list = []

    category1_id = request.json.get("category1Id")
    category2_id = request.json.get("category2Id")
    category3_id = request.json.get("category3Id")
    category_name = request.json.get("categoryName")
    keyword = request.json.get("keyword")
    props = request.json.get("props")
    trademark = request.json.get("trademark")
    # 下面这三个参数都是有默认值的(由前端决定)
    order = request.json.get("order")
    page_no = request.json.get("pageNo")
    page_size = request.json.get("pageSize")

    # 第一种情况：设置默认页面
    if not category1_id and not category2_id and not category3_id and not category3_id and \
            not category_name and not keyword and not \
            props and not trademark:
        all_info = list(Goods_se_details_sku.find({"tmId": 1}, {"_id": 0}))
        attrs_info = list(Goods_se_attrs.find({"connect_category3Id": "4"}, {"_id": 0}))
        for x in all_info:
            trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
        # 获取不重复的品牌数据
        trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]

        for x_ in all_info:
            goods_list.append(x_)
            # print(goods_list, "\n")

        for y in attrs_info:
            attrs_list.append(y)

        # 判断商品的状态是上架还是下架
        is_sale_or_cancel_sale = []
        for x_ in goods_list:
            if x_["isSale"] == 1:
                is_sale_or_cancel_sale.append(x_)
        goods_list = is_sale_or_cancel_sale

        # 首页默认分页效果
        limit_start = (page_no - 1) * page_size
        page_total = int(math.ceil(len(goods_list) / page_size))
        total = len(goods_list)
        goods_list = goods_list[limit_start:page_no * page_size]

        # 处理order参数
        if order == "1:asc":
            goods_list = sorted(goods_list, key=lambda goods_list: goods_list["spuId"])
        elif order == "1:desc":
            goods_list = sorted(goods_list, key=lambda goods_list: goods_list["spuId"], reverse=True)
        elif order == "2:asc":
            goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"])
        else:
            goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"], reverse=True)

        return jsonify({
            "code": 200,
            "message": "成功",
            "data": {
                "trademarkList": trademark_list,
                "attrsList": attrs_list,
                "goodsList": goods_list,
                "total": total,
                "pageSize": page_size,
                "pageNo": page_no,
                "totalPages": page_total
            },
            "ok": True
        })

    # 第二种情况，前端传递来了参数（默认参数除外）
    # 该变量用于表示跳过前面多少条
    limit_start = (page_no - 1) * page_size

    # 处理 trademark 的值
    if trademark:
        trademark = trademark.split(":")
        all_info_2 = list(Goods_se_details_sku.find({"tmId": int(trademark[0])},
                                                    {"_id": 0}))

    # 处理由三级类目列表进行搜索的结果
    elif category1_id:
        all_info_2 = list(Goods_se_details_sku.find({"category1Id": category1_id},
                                                    {"_id": 0}))

    elif category2_id:
        all_info_2 = list(Goods_se_details_sku.find({"category2Id": category2_id},
                                                    {"_id": 0}))
    else:
        all_info_2 = list(Goods_se_details_sku.find({"category3Id": category3_id},
                                                    {"_id": 0}))

    if all_info_2 and keyword:
        # 这是对应同时使用三级类目导航和keyword导航的情况的情况
        for x in all_info_2:
            if keyword in x["skuName"]:
                trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

        for x_ in all_info_2:
            if keyword in x_["tmName"]:
                attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
                                                      {"_id": 0}))
                goods_list.append(x_)

    elif all_info_2:
        # 这是对应只有三级类目导航的情况
        for x in all_info_2:
            trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

        for x_ in all_info_2:
            attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
                                                  {"_id": 0}))
            goods_list.append(x_)

    elif keyword:
        # 这是对应只有 keyword 的情况
        # 实现了简易版的模糊搜索
        all_info_3 = list(Goods_se_details_sku.find({}, {"_id": 0}))
        for x in all_info_3:
            if keyword in x["tmName"] or keyword in x["skuName"]:
                trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

        for x_ in all_info_3:
            if keyword in x_["tmName"] or keyword in x_["skuName"]:
                attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
                                                      {"_id": 0}))
                goods_list.append(x_)

    else:
        pass

    # 处理props参数
    if props:
        props_list = []
        for x in props:
            x = x.split(":")
            for z in goods_list:
                for z_ in z["skuAttrValueList"]:
                    if x[0] == z_["attrId"] and x[1] == z_["valueName"]:
                        if z not in props_list:
                            props_list.append(z)
        goods_list = props_list

    # 判断商品的状态是上架还是下架
    is_sale_or_cancel_sale = []
    for x_ in goods_list:
        if x_["isSale"] == 1:
            is_sale_or_cancel_sale.append(x_)
    goods_list = is_sale_or_cancel_sale

    total = len(goods_list)
    # 采用切片方式方便分页
    goods_list = goods_list[limit_start:page_no * page_size]

    # 获取不重复的品牌数据
    trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]

    # 获取分页总数
    page_total = int(math.ceil(len(goods_list) / page_size))

    # 处理order参数
    if order == "1:asc":
        goods_list = sorted(goods_list, key=lambda goods_list: goods_list["spuId"])
    elif order == "1:desc":
        goods_list = sorted(goods_list, key=lambda goods_list: goods_list["spuId"], reverse=True)
    elif order == "2:asc":
        goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"])
    else:
        goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"], reverse=True)

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": {
            "trademarkList": trademark_list,
            "attrsList": attrs_list,
            "goodsList": goods_list,
            "total": total,
            "pageSize": page_size,
            "pageNo": page_no,
            "totalPages": page_total
        },
        "ok": True
    })


# 展示商品详情的接口
@bp.route("/item/<int:sku_id>", methods=["GET", "POST"])
def item_detail(sku_id):
    try:
        sku_info = Goods_se_details_sku.find_one({"id": sku_id}, {"_id": 0})
        spu_id = sku_info["spuId"]
        item_info = Goods_se_details.find_one({"spuId": spu_id}, {"_id": 0})
        item_info["skuInfo"] = sku_info
    except Exception as e:
        return jsonify({
            "code": 404,
            "message": "该商品的数据详情页面不存在！",
            "data": {},
            "ok": False
        })

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": item_info,
        "ok": True
    })
