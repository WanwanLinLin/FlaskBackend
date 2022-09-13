# -*- coding: utf-8 -*-
import math, os

from .models import Goods_trademark
from pydantic import error_wrappers
from apps.auth import permission_required
from flask import Blueprint, jsonify, request
from .validate import SaveTrademark, UpdateTrademark

bp = Blueprint("admin_trade_mark", __name__)


# 一次性获取所有品牌的接口
@bp.route("/baseTrademark/getTrademarkList", methods=["GET", "POST"])
@permission_required
def get_trademark_list():
    trademark_list = list(Goods_trademark.find({}))
    data = []
    for x_ in trademark_list:
        data.append({
            "id": x_["id"],
            "tmName": x_["tmName"],
            "logoUrl": x_["logoUrl"]
        })
    return jsonify({
        "code": 200,
        "message": "获取成功",
        "data": data,
        "ok": True
    })


# 获取品牌总数的接口(需要分页)
@bp.route("/baseTrademark/<string:page>/<string:limit>", methods=["GET", "POST"])
@permission_required
def base_trade_mark(page, limit):
    page = int(page)
    limit = int(limit)

    trademark_info = list(Goods_trademark.find({}, {"_id": 0}))
    # print(trademark_info)
    records = []
    for x_ in trademark_info:
        records.append({
            "id": x_["id"],
            "tmName": x_["tmName"],
            "logoUrl": x_["logoUrl"]
        })

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
        "data": data,
        "message": "获取成功！",
        "ok": True
    })


# 添加品牌的接口
@bp.route("/baseTrademark/save", methods=["POST"])
@permission_required
def save_trademark():
    try:
        SaveTrademark(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    tm_name = request.json.get("tmName")
    logo_url = request.json.get("logoUrl")
    id_list = list(Goods_trademark.find().sort("id", -1))
    if id_list:
        id = id_list[0]["id"] + 1
    else:
        id = 1
    Goods_trademark.insert_one({
        "id": id,
        "tmName": tm_name,
        "logoUrl": logo_url
    })
    return jsonify({

        "code": 200,
        "message": "成功",
        "data": None,
        "ok": True
    })


# 这是更新品牌信息的接口
@bp.route("/baseTrademark/update", methods=["PUT"])
@permission_required
def update_trademark():
    try:
        UpdateTrademark(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()

    id = request.json.get("id")
    tm_name = request.json.get("tmName")
    logo_url = request.json.get("logoUrl")

    # 更新对应的品牌信息
    Goods_trademark.update_one({"id": id},
                               {"$set": {"tmName": tm_name, "logoUrl": logo_url}})
    return jsonify({
        "code": 200,
        "message": "更新信息成功!",
        "data": None,
        "ok": True
    })


# 删除品牌的接口
@bp.route("/baseTrademark/remove/<int:id>", methods=["DELETE"])
@permission_required
def remove_trademark(id):
    trademark_info = Goods_trademark.find_one({"id": id})
    if not trademark_info:
        return jsonify({
            "code": 201,
            "message": "该品牌不存在！!",
            "data": None,
            "ok": False
        })

    # 删除品牌名字段
    Goods_trademark.delete_one({"id": id})
    # 删除品牌对应的图片
    image_name = trademark_info["logoUrl"].split("/")[-1]
    os.remove(f"D:/github_projects/FlaskProject/static/trademark/{image_name}")
    return jsonify({
        "code": 200,
        "message": "删除品牌成功!",
        "data": None,
        "ok": True
    })





