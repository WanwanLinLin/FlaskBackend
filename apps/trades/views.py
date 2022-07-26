# -*- coding: utf-8 -*-
import time, binascii, os, math

from functools import wraps
from .models import Orders, Portfolios, NFT_list, Comments, Portfolios_like
from apps.goods import Goods
from flask import Blueprint, jsonify, request

# 创建 “我的交易” 蓝图
bp = Blueprint("trades", __name__)


def create_token(lenth=24):
    """创建一个token"""
    s = binascii.b2a_base64(os.urandom(lenth))[:-1].decode('utf-8')
    for x in ['+', '=', '/', '?', '&', '%', "#"]:
        s = s.replace(x, "")
    return s


# 用于约束接口必填数据key和必填项目的数据类型的装饰器
def check_request2(one_dict):
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            X = request.json
            for y in X:
                print("X[y] 此时的值是：", type(X[y]))

                if y in one_dict:
                    try:
                        assert type(X[y]) == one_dict[y]
                    except Exception:
                        return jsonify({"err": "验证失败,数据类型不匹配！！"})

            return func(*args, **kwargs)

        return decorate

    return wrapper


# 增加订单的接口
@bp.route("/insert", methods=["GET", "POST"])
@check_request2(one_dict={"goodsname": str, "num": int})
def insert():
    goods_name = request.json.get("goodsname")
    num = request.json.get("num")

    # 以下为数据库字段
    goods = Goods.find_one({"goodsname": goods_name})
    name = goods["goodsname"]
    purchase_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    price = goods["price"]
    payment = price * num
    inventory = goods["inventory"] - num
    order_number = create_token(8)
    status = "To_Be_Delivered"

    # 更新货物的数量
    Goods.update_one({"goodsname": goods_name},
                     {"$set": {"inventory": inventory}})

    Orders.insert_one({"purchase_time": purchase_time,
                       "price": price,
                       "payment": payment,
                       "inventory": inventory,
                       "status": status,
                       "order_number": order_number,
                       "name": name})

    return jsonify({"msg": "订单增加成功！"})


# 查询订单的接口
@bp.route("/inquire", methods=["GET", "POST"])
def inquire():
    l = []
    info = Orders.find({}, {"_id": 0})
    for x in info:
        l.append(x)
    return jsonify({"All_orders": l})


# 取消订单的接口
@bp.route("/cancel_order", methods=["GET", "POST"])
def cancel_order():
    order_num = request.json.get("order_num")
    if order_num:
        info = Orders.find_one({"order_number": order_num})
        Orders.delete_one(info)
        return jsonify({"msg": "取消订单成功！"})
    return jsonify({"err": "取消失败，没有此订单！"})


# 展示作品的接口（实现了简单的分页功能）
@bp.route("/portfolios", methods=["GET", "POST"])
def portfolios():
    name = request.json.get("name")
    page = request.json.get("page")

    # 每页显示的条数
    page_per = 5

    if not page:
        page = 1

    if page < 0:
        return jsonify({"show_status": "It's not ok !"})

    limit_start = (page-1)*page_per

    if name:
        result = list(Portfolios.find({"name": name}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = Portfolios.count_documents({"name": name})
    else:
        result = list(Portfolios.find({}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = Portfolios.count_documents({})

    page_total = int(math.ceil(total/page_per))
    show_status = "It's OK!"

    print(result)
    return jsonify({"datas": {"data_list": result,
                              "name": name,
                              "page": page,
                              "page_per": page_per,
                              "page_total": page_total,
                              "show_status": show_status}})


# 展示所有 nft 的接口（实现了简单的分页功能）
@bp.route("/nft_list", methods=["GET", "POST"])
def nft_list():
    name = request.json.get("name")
    page = request.json.get("page")

    # 每页显示的条数
    page_per = 5

    if not page:
        page = 1

    if page < 0:
        return jsonify({"show_status": "It's not ok !"})

    limit_start = (page - 1) * page_per

    if name:
        result = list(NFT_list.find({"name": name}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = NFT_list.count_documents({"name": name})
    else:
        result = list(NFT_list.find({}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = NFT_list.count_documents({})

    page_total = int(math.ceil(total / page_per))
    show_status = "It's OK!"

    print(result)
    return jsonify({"datas": {"data_list": result,
                              "name": name,
                              "page": page,
                              "page_per": page_per,
                              "page_total": page_total,
                              "show_status": show_status}})


# 查看评论或添加评论的接口
@bp.route("/get_comments", methods=["GET", "POST"])
def get_comments():
    if request.method == "GET":         # 查看评论
        id = request.json.get("id")
        portfolios_name = request.json.get("name")

        print(portfolios_name)
        # 根据作品名对应的 ObjectID 在评论集合里查找对应评论
        Object_ID = Portfolios.find_one({"id": id, "name": portfolios_name})
        print(Object_ID)
        comments = list(Comments.find({"comment_por": Object_ID["_id"]}, {"_id": 0, "comment_por": 0}))
        if comments:
            return jsonify({"comments_": comments})
        return jsonify({"msg": "抱歉，该作品暂时没有评论哦~"})

    else:
        portfolios_id = request.json.get("portfolios_id")
        portfolios_name = request.json.get("portfolios_name")
        Object_ID = Portfolios.find_one({"id": portfolios_id, "name": portfolios_name})

        user_name = request.json.get("user_name")
        image = request.json.get("image")
        content = request.json.get("content")
        comment_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sub_comment = ""

        # 实现自增长的 id
        id_list = list(Comments.find().sort("id", -1))
        id = id_list[0]["id"] + 1
        info = {"id": id, "comment_por": Object_ID["_id"], "username": user_name, "image": image,
                "content": content, "comment_time": comment_time, "sub_comment": sub_comment}
        Comments.insert_one(info)

        # return jsonify({})

        return jsonify({"msg": "添加评论成功！"})


# 点赞作品的接口
@bp.route("/portfolios_like", methods=["GET", "POST"])
def portfolios_like():
    id_ = request.json.get("id")
    portfolios_name = request.json.get("name")
    username = request.json.get("username")

    # 通过 ObjectID 查找对应的作品
    Object_ID = Portfolios.find_one({"id": id_, "name": portfolios_name})
    if Object_ID:
        # 实现自增长的 id
        id_list = list(Portfolios_like.find().sort("id", -1))
        id = id_list[0]["id"] + 1

        like_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info = {
            "id": id,
            "comment_por": Object_ID["_id"],
            "portfolios_name": portfolios_name,
            "username": username,
            "like_time": like_time
        }
        Portfolios_like.insert_one(info)

        return jsonify({"msg": "点赞成功！"})
    return jsonify({"err": "抱歉，未找到该作品~"})


# 获取某个作品点赞总数的接口
@bp.route("/get_portfolios_likes", methods=["GET", "POST"])
def get_portfolios_likes():
    id_ = request.json.get("id")
    portfolios_name = request.json.get("name")
    # 查找对应的作品的 ObjectID
    Object_ID_ = Portfolios.find_one({"id": id_, "name": portfolios_name})
    Object_ID = Object_ID_["_id"]

    # 获取点赞总数
    total = Portfolios_like.count_documents({"comment_por": Object_ID})
    print(total)

    return jsonify({"msg": "获取成功！", "total_likes": total})

