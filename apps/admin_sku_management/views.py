# -*- coding: utf-8 -*-
"""
如果把SPU比作一个类，那么SKU就是类的实例
"""
from flask import request, jsonify, Blueprint
from apps.admin_spu_management import Goods_se_image_list
from apps.goods import Goods_se, Goods_se_attrs, Goods_se_details

bp = Blueprint("admin_sku_management", __name__)


# 获取某个SPU全部图片的接口
@bp.route("/product/spuImageList/<int:spu_id>", methods=["GET", "POST"])
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
def get_spu_sale_attr_list(spu_id):
    spu_sale_attr_list = Goods_se_details.find_one({"spuId": spu_id})["spuSaleAttrList"]

    return jsonify({
        "code": 200,
        "message": "获取成功！",
        "data": spu_sale_attr_list,
        "ok": True
    })
