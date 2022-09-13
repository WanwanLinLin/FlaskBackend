# -*- coding: utf-8 -*-
"""
如果把SPU比作一个类，那么SKU就是类的实例
"""
import time, math

from .validate import SaveSkuInfo
from pydantic import error_wrappers
from .models import Goods_se_details_sku
from flask import request, jsonify, Blueprint
from apps.auth import permission_required
from apps.admin_trade_mark import Goods_trademark
from apps.admin_spu_management import Goods_se_image_list
from apps.goods import (Goods_se, Goods_se_attrs, Goods_se_details,
                        CategoryListModel, SeCategoryListModel, ThCategoryListModel)

bp = Blueprint("admin_sku_management", __name__)


# 获取某个SPU全部图片的接口
@bp.route("/product/spuImageList/<int:spu_id>", methods=["GET", "POST"])
@permission_required
def get_spu_image_list(spu_id):
    spu_image_list = list(Goods_se_image_list.find({"spuId": spu_id}, {"_id": 0}))
    data = []
    for i, x_ in enumerate(spu_image_list, start=1):
        data.append({
            "id": i,
            "spuId": spu_id,
            "imgName": x_["imgName"],
            "imgUrl": x_["imgUrl"]
        }, )

    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": data,
        "ok": True
    })


# 获取某个SPU全部销售属性的接口
@bp.route("/product/spuSaleAttrList/<int:spu_id>", methods=["GET", "POST"])
@permission_required
def get_spu_sale_attr_list(spu_id):
    spu_sale_attr_list = Goods_se_details.find_one({"spuId": spu_id})["spuSaleAttrList"]

    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": spu_sale_attr_list,
        "ok": True
    })


# 保存SKU信息的接口
@bp.route("/product/saveSkuInfo", methods=["GET", "POST"])
@permission_required
def save_sku_info():
    try:
        SaveSkuInfo(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    # print(request.get_json())
    category3_id = request.json.get("category3Id")
    spu_id = request.json.get("spuId")
    tm_id = request.json.get("tmId")
    sku_name = request.json.get("skuName")
    price = request.json.get("price")
    weight = request.json.get("weight")
    sku_desc = request.json.get("skuDesc")
    sku_default_img = request.json.get("skuDefaultImg")
    sku_image_list = request.json.get("skuImageList")
    sku_attr_value_list = request.json.get("skuAttrValueList")
    sku_sale_attr_value_list = request.json.get("skuSaleAttrValueList")

    # 1.生成一个新的sku_id
    id_list = list(Goods_se_details_sku.find({}).sort("id", -1))
    if id_list:
        sku_id = id_list[0]["id"] + 1
    else:
        sku_id = 1

    # 2.处理skuImageList
    new_sku_image_list = []
    for i, x_ in enumerate(sku_image_list, start=1):
        new_sku_image_list.append({
            "id": x_['spuImgId'],
            "skuId": sku_id,
            "imageName": x_['imgName'],
            "imageUrl": x_['imgUrl'],
            "spuImgId": x_['spuImgId'],
            "isDefault": str(x_['isDefault'])
        })

    # 3.处理skuAttrValueList
    new_sku_attr_value_list = []
    for i, x_ in enumerate(sku_attr_value_list, start=1):
        new_sku_attr_value_list.append({
            "id": i,
            "attrId": x_['attrId'],
            "valueId": x_['valueId'],
            'valueName': x_['valueName'],
            "skuId": sku_id
        })

    # 4.处理skuSaleAttrValueList
    new_sku_sale_attr_value_list = []
    for i, x_ in enumerate(sku_sale_attr_value_list, start=1):
        new_sku_sale_attr_value_list.append({
            "id": i,
            "saleAttrId": x_['saleAttrId'],
            "saleAttrValueId": x_['saleAttrValueId']
        })

    # 5.反向查询得出对应的category2Id和category1Id以及查出tmName
    category2_id = ThCategoryListModel.query.filter(ThCategoryListModel.id == int(category3_id)).first().category_par
    category1_id = SeCategoryListModel.query.filter(SeCategoryListModel.id == category2_id).first().category_par
    tm_name = Goods_trademark.find_one({"id": tm_id}, {"_id": 0})["tmName"]

    # 6.整合数据
    sku_info = {
        "id": sku_id,
        "spuId": spu_id,
        "price": price,
        "skuName": sku_name,
        "skuDesc": sku_desc,
        "weight": weight,
        "createTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "tmId": tm_id,
        "tmName": tm_name,
        "category3Id": category3_id,
        "category2Id": str(category2_id),
        "category1Id": str(category1_id),
        "skuDefualtImg": sku_default_img,
        "defualtImg": sku_default_img,
        "isSale": 1,
        "skuImageList": new_sku_image_list,
        "skuAttrValueList": new_sku_attr_value_list,
        "skuSaleAttrValueList": new_sku_sale_attr_value_list
    }
    # print(sku_info)
    # 5.插入数据库
    Goods_se_details_sku.insert_one(sku_info)

    return jsonify({
        "code": 200,
        "message": "保存成功！",
        "data": None,
        "ok": True
    })


# 查找某个SPU对应的所有SKU的接口
@bp.route("/product/findBySpuId/<int:spu_id>", methods=["GET", "POST"])
@permission_required
def find_sku_by_spu_id(spu_id):
    data = list(Goods_se_details_sku.find({"spuId": spu_id},
                                          {"_id": 0, "skuImageList": 0,
                                           "skuAttrValueList": 0, "skuSaleAttrValueList": 0}))
    return jsonify({
        "code": 200,
        "message": "查找成功!",
        "data": data,
        "ok": True
    })


# 展示所有SKU的接口
@bp.route("/product/list/<int:page>/<int:limit>", methods=["GET", "POST"])
@permission_required
def get_sku_list(page, limit):
    sku_list = list(Goods_se_details_sku.find({},
                                              {"_id": 0, "skuImageList": 0,
                                               "skuAttrValueList": 0, "skuSaleAttrValueList": 0}))
    # 实现简单的分页效果
    # 该变量用于表示跳过前面多少条
    limit_start = (page - 1) * limit
    # 获取品牌总数量
    total = len(sku_list)
    # 获取实际需要展示的条数
    sku_list = sku_list[limit_start:page * limit]
    # 获取分页总数
    pages = int(math.ceil(total / limit))

    data = {
        "records": sku_list,
        "total": total,
        "size": limit,
        "current": page,
        "searchCount": True,
        "pages": pages
    }
    return jsonify({
        "code": 200,
        "message": "获取成功",
        "data": data,
        "ok": True
    })


# SKU上架的接口
@bp.route("/product/onSale/<int:sku_id>", methods=["GET", "POST"])
@permission_required
def on_sale(sku_id):
    Goods_se_details_sku.update_one({"id": sku_id}, {"$set": {"isSale": 1}})
    return jsonify({
        "code": 200,
        "message": "商品上架成功！",
        "data": None,
        "ok": True
    })


# SKU下架的接口
@bp.route("/product/cancelSale/<int:sku_id>", methods=["GET", "POST"])
@permission_required
def cancel_sale(sku_id):
    Goods_se_details_sku.update_one({"id": sku_id}, {"$set": {"isSale": 0}})
    return jsonify({
        "code": 200,
        "message": "商品下架成功！",
        "data": None,
        "ok": True
    })


# 获取SKU详情的接口
@bp.route("/product/getSkuById/<int:sku_id>", methods=["GET", "POST"])
@permission_required
def get_sku_by_id(sku_id):
    sku_info = Goods_se_details_sku.find_one({"id": sku_id}, {"_id": 0})
    new_sku_attr_value_list = []
    new_sku_sale_attr_value_list = []

    for i, x_ in enumerate(sku_info["skuAttrValueList"], start=1):
        attr_name = Goods_se_attrs.find_one({"attrId": int(x_["attrId"])})["attrName"]
        new_sku_attr_value_list.append({
            "id": x_["id"],
            "attrId": int(x_["attrId"]),
            "valueId": int(x_["valueId"]),
            "skuId": x_["skuId"],
            "attrName": attr_name,
            "valueName": x_["valueName"]
        })

    for i, x_ in enumerate(sku_info["skuSaleAttrValueList"], start=1):
        spu_info = Goods_se_details.find_one({"spuId": sku_info["spuId"]})
        for y_ in spu_info["spuSaleAttrList"]:
            if x_["saleAttrId"] == str(y_["id"]):
                sku_sale_attr_name = y_["saleAttrName"]
                for z_ in y_["spuSaleAttrValueList"]:
                    if x_["saleAttrValueId"] == str(z_["id"]):
                        sku_sale_attr_value_name = z_["saleAttrValueName"]
                        new_sku_sale_attr_value_list.append({
                            "id": x_["id"],
                            "skuId": sku_id,
                            "spuId": sku_info["spuId"],
                            "saleAttrValueId": int(x_["saleAttrValueId"]),
                            "saleAttrId": int(x_["saleAttrId"]),
                            "saleAttrName": sku_sale_attr_name,
                            "saleAttrValueName": sku_sale_attr_value_name
                        })

    data = {
        "id": sku_info["id"],
        "spuId": sku_info["spuId"],
        "price": float(sku_info["price"]),
        "skuName": sku_info["skuName"],
        "skuDesc": sku_info["skuDesc"],
        "weight": sku_info["weight"],
        "tmId": sku_info["tmId"],
        "category3Id": int(sku_info["category3Id"]),
        "skuDefaultImg": sku_info["defualtImg"],
        "isSale": sku_info["isSale"],
        "createTime": sku_info["createTime"],
        "skuImageList": sku_info["skuImageList"],
        "skuAttrValueList": new_sku_attr_value_list,
        "skuSaleAttrValueList": new_sku_sale_attr_value_list
    }
    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": data,
        "ok": False
    })
