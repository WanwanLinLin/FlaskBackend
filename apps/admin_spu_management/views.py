# -*- coding: utf-8 -*-
import math, time, os
from pydantic import error_wrappers
from .validate import UpdateOrSaveSpuInfo
from flask import Blueprint, request, jsonify
from .models import Goods_se_sale_attrs, Goods_se_image_list, Goods_se_details_sku
from apps.admin_trade_mark import Goods_trademark
from apps.goods import Goods_se, Goods_se_attrs, Goods_se_details

bp = Blueprint("admin_spu_management", __name__)


# 获取SPU列表的接口
@bp.route("/product/<int:page>/<int:limit>", methods=["GET", "POST"])
def get_spu_list(page, limit):
    category3_id = request.args.get("category3Id")
    category3_id = str(category3_id)

    spu_info = list(Goods_se_details.find({"category3Id": category3_id}, {"_id": 0}))
    records = []
    for x_ in spu_info:
        records.append({
            "id": x_["spuId"],
            "spuName": x_["spuName"],
            "description": x_["description"],
            "category3Id": x_["category3Id"],
            "tmId": x_["tmId"],
            "spuSaleAttrList": None,
            "spuImageList": None
        })

    # 实现简单的分页功能
    # 该变量用于表示跳过前面多少条
    limit_start = (page - 1) * limit
    # 获取品牌总数量
    total = len(records)
    # 获取实际需要展示的条数
    records = records[limit_start:page * limit]
    # 获取分页总数
    pages = int(math.ceil(total / limit))

    data = {
        "records": records,
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


# 获取SPU基础属性的接口
@bp.route("/product/baseSaleAttrList", methods=["GET", "POST"])
def get_base_sale_attr_list():
    sale_attr_list = list(Goods_se_sale_attrs.find({}, {"_id": 0}))

    return jsonify({
        "code": 200,
        "message": "获取成功",
        "data": sale_attr_list,
        "ok": True
    })


# 获取SPU基本信息的接口
@bp.route("/product/getSpuById/<int:spu_id>", methods=["GET", "POST"])
def get_spu_by_id(spu_id):
    spu_info = Goods_se_details.find_one({"spuId": spu_id}, {"_id": 0})
    if not spu_info:
        return jsonify({
            "code": 201,
            "message": "获取失败!",
            "data": None,
            "ok": False
        })

    data = {
        "id": spu_info["spuId"],
        "spuName": spu_info["spuName"],
        "description": spu_info["description"],
        "category3Id": spu_info["category3Id"],
        "tmId": spu_info["tmId"],
        "spuSaleAttrList": spu_info["spuSaleAttrList"]
    }
    return jsonify({
        "code": 200,
        "message": "获取成功!",
        "data": data,
        "ok": True
    })


# 获取SPU图片的接口
@bp.route("/product/spuImageList/<int:spu_id>", methods=["GET", "POST"])
def get_spu_image_list(spu_id):
    spu_image_list = list(Goods_se_image_list.find({"spuId": spu_id}, {"_id": 0}))

    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": spu_image_list,
        "ok": True
    })


# 修改SPU信息的接口
@bp.route("/product/updateSpuInfo", methods=["GET", "POST"])
def update_spu_info():
    try:
        UpdateOrSaveSpuInfo(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    description = request.json.get("description")
    id_ = request.json.get("id")
    spu_name = request.json.get("spuName")
    spu_sale_attr_list = request.json.get("spuSaleAttrList")
    spu_image_list = request.json.get("spuImageList")
    # print(request.get_json())

    # 处理spuSaleAttrList
    new_spu_sale_attr_list = []
    for i, x_ in enumerate(spu_sale_attr_list, start=1):
        dict_ = {
            "id": i,
            'baseSaleAttrId': int(x_['baseSaleAttrId']),
            'saleAttrName': x_['saleAttrName'],
            "spuId": id_
        }
        new_x = []
        for j, y_ in enumerate(x_['spuSaleAttrValueList'], start=1):
            dict_2 = {
                "id": j,
                'baseSaleAttrId': y_['baseSaleAttrId'],
                "saleAttrName": x_['saleAttrName'],
                'saleAttrValueName': y_['saleAttrValueName'],
                "spuId": id_,
                "isChecked": "0"
            }
            new_x.append(dict_2)
        dict_["spuSaleAttrValueList"] = new_x
        new_spu_sale_attr_list.append(dict_)
    # print(new_spu_sale_attr_list)

    # 处理spuImageList
    # 这里采用先全部删除再重新插入的方法
    Goods_se_image_list.delete_many({"spuId": id_})
    id_list = list(Goods_se_image_list.find().sort("id", -1))
    if not id_list:
        id = 1
    else:
        id = id_list[0]["id"] + 1

    for i, x_ in enumerate(spu_image_list, start=int(id)):
        Goods_se_image_list.insert_one({
            "id": i,
            "spuId": id_,
            "imgName": x_["imageName"],
            "imgUrl": x_["imageUrl"]
        })

    # 最后更新Goods_se_details数据库
    # 更新description和spuName
    Goods_se_details.update_one({"spuId": id_},
                                {"$set": {"spuSaleAttrList": new_spu_sale_attr_list,
                                          "spuName": spu_name, "description": description}})

    return jsonify({
        "code": 200,
        "message": "修改成功",
        "data": None,
        "ok": True
    })


# 添加SPU信息的接口
@bp.route("/product/saveSpuInfo", methods=["GET", "POST"])
def save_spu_info():
    try:
        UpdateOrSaveSpuInfo(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    # print(request.get_json())

    tm_id = request.json.get("tmId")
    spu_name = request.json.get("spuName")
    description = request.json.get("description")
    category3_id = request.json.get("category3Id")
    spu_sale_attr_list = request.json.get("spuSaleAttrList")
    spu_image_list = request.json.get("spuImageList")

    # 1.创建一个新的Goods_se的ID，与SPU_ID并用
    goods_se_spu_id_list = list(Goods_se_details.find().sort("spuId", -1))
    if not goods_se_spu_id_list:
        goods_se_spu_id = 1
    else:
        goods_se_spu_id = goods_se_spu_id_list[0]["spuId"] + 1.0

    # 2.处理spuSaleAttrList
    new_spu_sale_attr_list = []
    for i, x_ in enumerate(spu_sale_attr_list, start=1):
        dict_ = {
            "id": i,
            'baseSaleAttrId': int(x_['baseSaleAttrId']),
            'saleAttrName': x_['saleAttrName'],
            "spuId": goods_se_spu_id
        }
        new_x = []
        for j, y_ in enumerate(x_['spuSaleAttrValueList'], start=1):
            dict_2 = {
                "id": j,
                'baseSaleAttrId': y_['baseSaleAttrId'],
                "saleAttrName": x_['saleAttrName'],
                'saleAttrValueName': y_['saleAttrValueName'],
                "spuId": goods_se_spu_id,
                "isChecked": "0"
            }
            new_x.append(dict_2)
        dict_["spuSaleAttrValueList"] = new_x
        new_spu_sale_attr_list.append(dict_)

    # 3.处理spuImageList
    image_id_list = list(Goods_se_image_list.find().sort("id", -1))
    if not image_id_list:
        id = 1
    else:
        id = image_id_list[0]["id"] + 1

    for i, x_ in enumerate(spu_image_list, start=int(id)):
        Goods_se_image_list.insert_one({
            "id": i,
            "spuId": goods_se_spu_id,
            "imgName": x_["imageName"],
            "imgUrl": x_["imageUrl"]
        })

    # 4.增加一条Goods_se_details记录
    Goods_se_details.insert_one({
        "spuId": goods_se_spu_id,
        "spuSaleAttrList": new_spu_sale_attr_list,
        "skuInfo": {},
        "categoryView": {},
        "valuesSkuJson": "",
        "category3Id": str(category3_id),
        "description": description,
        "spuName": spu_name,
        "tmId": tm_id
    })

    return jsonify({
        "code": 200,
        "message": "添加成功",
        "data": None,
        "ok": True
    })


# 删除相应SPU信息的接口
@bp.route("/product/deleteSpu/<int:spu_id>", methods=["DELETE"])
def delete_spu(spu_id):
    # 删除Goods_details中的信息
    Goods_se_details.delete_one({"spuId": spu_id})
    # 删除Goods_se_image_list中的信息
    # 删除SPU对应的图片
    image_name_list = list(Goods_se_image_list.find({"spuId": spu_id}, {"_id": 0}))
    for x_ in image_name_list:
        image_name = x_["imgUrl"].split("/")[-1]
        os.remove(f"D:/github_projects/FlaskProject/static/category_image/{image_name}")
    Goods_se_image_list.delete_many({"spuId": spu_id})

    return jsonify({
        "code": 200,
        "message": "删除成功！",
        "data": None,
        "ok": True
    })
