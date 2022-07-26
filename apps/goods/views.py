# -*- coding: utf-8 -*-
from .models import Goods
from flask import Blueprint, jsonify, request

bp = Blueprint("goods", __name__)


# 展示所有商品的接口
@bp.route("/display", methods=["GET", "POST"])
def display():
    info = list(Goods.find({}, {"_id": 0, "id": 0}))
    print(info)

    l = []
    for x in info:
        l.append(x)

    return jsonify({"info": l})
