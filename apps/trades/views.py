# -*- coding: utf-8 -*-
import time, binascii, os, math

from functools import wraps
from .models import Orders, Portfolios, NFT_list, Comments, Portfolios_like
from apps.goods import Goods, Goods_se
from flask import Blueprint, jsonify, request

# 创建 “我的交易” 蓝图
bp = Blueprint("trades", __name__)


def create_numbering(length=24):
    """创建一个token"""
    s = binascii.b2a_base64(os.urandom(length))[:-1].decode('utf-8')
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
@bp.route("/addToCart/<string:sku_id>/<string:sku_num>", methods=["GET", "POST"])
def add_to_cart(sku_id, sku_num):
    x_ = request.headers.get("userTempId")
    # 以下为数据库字段
    sku_id = int(sku_id)
    sku_num = int(sku_num)
    goods = Goods_se.find_one({"id": sku_id})
    default_img = goods["defualtImg"]
    # 订单表与商品表关联的id
    connect_goods_se_id = goods["id"]
    name = goods["title"]
    purchase_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    price = goods["price"]
    payment = price * sku_num
    inventory = goods["inventory"] - sku_num
    order_number = create_numbering(8)
    status = "To_Be_Delivered"

    # 更新货物的数量
    Goods_se.update_one({"title": name},
                        {"$set": {"inventory": inventory}})

    y_ = Orders.find_one({"name": name})
    if y_:
        # 根据前端要求，返回三种不同的状态
        if sku_num == 1 or sku_num == -1 or sku_num == 0:
            # 删除或增加商品数量时修改产品的总价格
            payment = y_["payment"] + payment
            # 删除或增加商品数量时修改产品的总数量
            sku_num = y_["purchase_num"] + sku_num
        else:
            # 删除或增加商品数量时修改产品的总价格
            payment = y_["payment"] + payment
            # 删除或增加商品数量时修改产品的总数量
            sku_num = y_["purchase_num"] + sku_num

        Orders.update_one({"name": name},
                          {"$set": {"purchase_time": purchase_time,
                                    "purchase_num": sku_num,
                                    "price": price,
                                    "payment": payment,
                                    "inventory": inventory,
                                    "userTempId": x_
                                    }})
    else:
        Orders.insert_one({"purchase_time": purchase_time,
                           "purchase_num": sku_num,
                           "price": price,
                           "payment": payment,
                           "inventory": inventory,
                           "status": status,
                           "order_number": order_number,
                           "name": name,
                           "connect_goods_se_id": connect_goods_se_id,
                           "userTempId": x_,
                           "default_img": default_img,
                           "isChecked": 0,
                           "isOrdered": 0
                           })

    return jsonify({"code": 200,
                    "message": "成功",
                    "data": None,
                    "ok": True
                    })


# 查询购物车中订单的接口
@bp.route("/cartList", methods=["GET", "POST"])
def cart_list():
    x_ = request.headers.get("userTempId")
    print(x_)
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    data = [{"cartInfoList": [], "activityRuleList": None, "createTime": create_time}]
    info = Orders.find({"userTempId": x_}, {"_id": 0, "userTempId": 0})
    for x in info:
        data[0]["cartInfoList"].append(x)

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "ok": True
    })


# 取消订单的接口
@bp.route("/deleteCart/<string:sku_id>", methods=["DELETE"])
def delete_cart(sku_id):
    sku_id = int(sku_id)
    info = Orders.find_one({"connect_goods_se_id": sku_id})
    Orders.delete_one(info)
    return jsonify({
        "code": 200,
        "message": "成功！！",
        "data": None,
        "ok": True
    })


# 切换订单中商品选中状态的接口
@bp.route("/checkCart/<string:sku_id>/<string:is_checked>", methods=["GET", "POST"])
def check_cart(sku_id, is_checked):
    sku_id = int(sku_id)
    is_checked = int(is_checked)
    Orders.update_one({"connect_goods_se_id": sku_id}
                      , {"$set": {"isChecked": is_checked}})
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": None,
        "ok": True
    })


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

    limit_start = (page - 1) * page_per

    if name:
        result = list(Portfolios.find({"name": name}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = Portfolios.count_documents({"name": name})
    else:
        result = list(Portfolios.find({}, {"_id": 0}).sort("id", 1).limit(page_per).skip(limit_start))
        total = Portfolios.count_documents({})

    page_total = int(math.ceil(total / page_per))
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
    if request.method == "GET":  # 查看评论
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
