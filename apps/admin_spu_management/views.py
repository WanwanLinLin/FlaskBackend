# -*- coding: utf-8 -*-
import math
from flask import Blueprint, request, jsonify
from .models import Goods_se_sale_attrs, Goods_se_image_list
from apps.goods import Goods_se, Goods_se_attrs, Goods_se_details

bp = Blueprint("admin_spu_management", __name__)


# 获取SPU列表的接口
@bp.route("/product/<int:page>/<int:limit>", methods=["GET", "POST"])
def get_spu_list(page, limit):
    category3_id = request.args.get("category3Id")
    category3_id = str(category3_id)

    spu_info = list(Goods_se.find({"category3Id": category3_id}, {"_id": 0}))
    records = []
    for x_ in spu_info:
        records.append({
            "id": x_["id"],
            "spuName": x_["title"],
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
    spu_info_detail = Goods_se_details.find_one({"spuId": spu_id})
    if not spu_info_detail:
        return jsonify({
            "code": 201,
            "message": "获取失败!",
            "data": None,
            "ok": False
        })

    spu_info = Goods_se.find_one({"id": spu_info_detail["connect_goods_se_id"]})

    data = {
        "id": spu_info["id"],
        "spuName": spu_info["title"],
        "description": spu_info["description"],
        "category3Id": spu_info["category3Id"],
        "tmId": spu_info["tmId"],
        "spuSaleAttrList": spu_info_detail["spuSaleAttrList"]
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

    return jsonify({
        "code": 200,
        "message": "修改成功",
        "data": None,
        "ok": True
    })


# 添加SPU信息的接口
@bp.route("/product/saveSpuInfo", methods=["GET", "POST"])
def save_spu_info():

    return jsonify({
        "code": 200,
        "message": "添加成功",
        "data": None,
        "ok": True
    })

