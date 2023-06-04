# -*- coding: utf-8 -*-
import json
import math
import time
from datetime import timedelta, datetime

from flask import Blueprint, jsonify, request, g
from flask_pydantic_spec import Response as fp_Response

from auth import login_required, parse_jwt
from extension import swagger
from nosql_db import r_2
from utils import create_numbering, get_order_code
from .models import (Orders, Shipping_address, User, Goods_se_details_sku)
from .validate import ShippingAddress, SubmitOrder, Header, SubmitOrderQuery

# 创建 “我的交易” 蓝图
bp = Blueprint("trades", __name__)


# 增加订单的接口
@bp.post("/addToCart/<string:sku_id>/<string:sku_num>")
@swagger.validate(resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def add_to_cart(sku_id, sku_num):
    uuid_ = request.headers.get("userTempId")
    token_ = request.headers.get('token')

    # 以下为数据库字段
    sku_id = int(sku_id)
    sku_num = int(sku_num)

    # 用户已经登录
    if token_:
        username = parse_jwt(token_, User)["username"]
        goods = Goods_se_details_sku.find_one({"id": sku_id})
        default_img = goods["defualtImg"]
        # 订单表与商品表关联的id
        connect_goods_se_sku_id = goods["id"]
        name = goods["skuName"]
        purchase_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        price = int(goods["price"])
        payment = price * sku_num
        order_number = create_numbering(16)
        status = "To_Be_Delivered"

        y_ = Orders.find_one({"name": name, "userTempId": token_})
        # 修改订单
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

            Orders.update_one({"name": name, "userTempId": token_},
                              {"$set": {"purchase_time": purchase_time,
                                        "purchase_num": sku_num,
                                        "price": price,
                                        "payment": payment,
                                        }})

        # 增加订单
        else:
            Orders.insert_one({"purchase_time": purchase_time,
                               "purchase_num": sku_num,
                               "price": price,
                               "payment": payment,
                               "status": status,
                               "order_number": order_number,
                               "name": name,
                               "connect_goods_se_id": connect_goods_se_sku_id,
                               "userTempId": token_,
                               "default_img": default_img,
                               "isChecked": 0,
                               "isOrdered": 0,
                               })

        # 将未登录时的购物车加入到已登录的购物车中
        if username:
            uuid_list = list(Orders.find({"userTempId": uuid_}))
            token_list = list(Orders.find({"userTempId": token_}))
            for u_ in uuid_list:
                for t_ in token_list:
                    if u_["name"] == t_["name"]:
                        Orders.update_many({"name": t_["name"]},
                                           {"$set": {"purchase_num": t_["purchase_num"] + u_["purchase_num"],
                                                     "payment": (t_["purchase_num"] + u_["purchase_num"]) * t_[
                                                         "price"]}})
                        # 删除数据库中的一条数据，因为同一账号同一商品重复的最多两条
                        Orders.delete_one({"name": t_["name"], "userTempId": uuid_})
                        # print("这里执行了")
                    else:
                        # print("这里也执行了")
                        Orders.update_one({"name": u_["name"], "userTempId": uuid_},
                                          {"$set": {"userTempId": token_,
                                                    "purchase_num": u_["purchase_num"]}})

    # 用户未登录
    else:
        goods = Goods_se_details_sku.find_one({"id": sku_id})
        default_img = goods["defualtImg"]
        # 订单表与商品表关联的id
        connect_goods_se_sku_id = goods["id"]
        name = goods["skuName"]
        purchase_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        price = goods["price"]
        payment = price * sku_num
        order_number = create_numbering(16)
        status = "To_Be_Delivered"

        y_ = Orders.find_one({"name": name, "userTempId": uuid_})
        # 修改订单
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

            Orders.update_one({"name": name, "userTempId": uuid_},
                              {"$set": {"purchase_time": purchase_time,
                                        "purchase_num": sku_num,
                                        "price": price,
                                        "payment": payment,
                                        }})

        # 增加订单
        else:
            Orders.insert_one({"purchase_time": purchase_time,
                               "purchase_num": sku_num,
                               "price": price,
                               "payment": payment,
                               "status": status,
                               "order_number": order_number,
                               "name": name,
                               "connect_goods_se_id": connect_goods_se_sku_id,
                               "userTempId": uuid_,
                               "default_img": default_img,
                               "isChecked": 0,
                               "isOrdered": 0,
                               })

    return jsonify({"code": 200,
                    "message": "成功",
                    "data": None,
                    "ok": True
                    })


# 查询购物车中订单的接口
@bp.get("/cartList")
@swagger.validate(resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def cart_list():
    x_ = request.headers.get("userTempId")
    y_ = request.headers.get('token')
    # print(x_)
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    data = [{"cartInfoList": [], "activityRuleList": None, "createTime": create_time}]

    if y_:
        info = Orders.find({"userTempId": y_}, {"_id": 0, "userTempId": 0})
    else:
        info = Orders.find({"userTempId": x_}, {"_id": 0, "userTempId": 0})

    for x in info:
        x['price'] = int(x['price'])
        data[0]["cartInfoList"].append(x)
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "ok": True
    })


# 取消订单的接口
@bp.delete("/deleteCart/<string:sku_id>")
@swagger.validate(resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
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
@bp.get("/checkCart/<string:sku_id>/<string:is_checked>")
@swagger.validate(resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
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


# 获取订单交易页信息的接口
@bp.get("/auth/trade")
@login_required
@swagger.validate(headers=Header, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def auth_trade():
    token_ = request.headers.get('token')
    username = g.username
    user_address_list = []
    detail_array_list = []
    address_list = list(Shipping_address.find({"connect_username": username}, {"_id": 0}))
    detail_list = list(Orders.find({"userTempId": token_}, {"_id": 0}))
    # print(detail_list)
    user_id = User.find_one({"username": username})["id"]
    price = 0

    for x_ in address_list:
        user_address_list.append({
            "id": x_["id"],
            "userAddress": x_["shipping_address"],
            "userId": user_id,
            "consignee": x_["username"],
            "phoneNum": x_["customer_number"],
            "isDefault": x_["isDefault"]
        })

    for i, y_ in enumerate(detail_list, start=1):
        price += int(y_["payment"])
        detail_array_list.append({
            "id": y_["connect_goods_se_id"],
            "orderId": i,
            "skuId": i,
            "skuName": y_["name"],
            "imgUrl": y_["default_img"],
            "orderPrice": y_["payment"],
            "skuNum": y_["purchase_num"],
            "hasStock": True
        })
    # 整合到data里面
    data = {
        "totalAmount": price,
        "userAddressList": user_address_list,
        "tradeNo": create_numbering(24),
        "totalNum": len(detail_array_list),
        "detailArrayList": detail_array_list
    }

    # # 生成结算订单后应该清空购物车
    # Orders.delete_many({"userTempId": token_})

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "ok": False
    })


# 提交订单的接口
@bp.post("/auth/submitOrder")
@login_required
@swagger.validate(headers=Header, query=SubmitOrderQuery, body=SubmitOrder,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def submit_order():
    trade_no = request.args.get("tradeNo")
    token_ = request.headers.get("token")

    # 如果订单号已经存在，则返回错误信息
    info = r_2.hgetall(trade_no)
    if info:
        return jsonify({
            "code": 201,
            "message": "抱歉，该订单号已经存在！",
            "data": trade_no,
            "ok": True
        })

    # 将提交的订单信息以hash形式存到redis中
    req = request.get_json()
    for x_ in req:
        r_2.hset(trade_no, x_, json.dumps(req[x_]))
    # 将token:订单信息以list类型存到redis中，作为唯一标识符
    r_2.rpush(token_, trade_no)

    r_2.expire(token_, 60 * 60)
    r_2.expire(trade_no, 60 * 60)

    # 订单信息提交之后应该删除订单表中的相关信息
    Orders.delete_many({"userTempId": token_})

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": trade_no,
        "ok": True
    })


# 获取订单支付信息的接口
@bp.get("/payment/weixin/createNative/<string:order_id>")
@login_required
@swagger.validate(headers=Header, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def order_payment(order_id):
    # 从redis中获取订单列表的总价格
    order_list = r_2.hget(order_id, "orderDetailList")
    order_list = json.loads(order_list)
    total_price = 0

    for x_ in order_list:
        total_price += int(x_["orderPrice"])

    data = {
        "codeUrl": "weixin://wxpay/bizpayurl?pr=P0aPBJK",
        "orderId": order_id,
        "totalFee": total_price,
        "resultCode": "SUCCESS"
    }
    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "ok": True

    })


# 查询订单支付状态的接口
@bp.get("/weixin/queryPayStatus/<string:order_id>")
@login_required
@swagger.validate(headers=Header, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def pay_status(order_id):
    pay_info = r_2.hgetall(order_id)

    if not pay_info:
        return jsonify({
            "code": 205,
            "message": "支付超时!",
            "data": None,
            "ok": False
        })

    # 支付成功应该从redis里面删除对应的订单支付信息
    # r_2.delete(order_id)

    return jsonify({
        "code": 200,
        "message": "支付成功!",
        "data": None,
        "ok": True
    })


# 在个人中心展示订单列表的接口
@bp.get("/order/auth/<string:page>/<string:limit>")
@login_required
@swagger.validate(headers=Header, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def center_order_list(page, limit):
    """
    :param page: 页码
    :param limit: 每页显示数量
    :return: JSON
    """
    token_ = request.headers.get("token")
    user_id = User.find_one({"username": g.username})["id"]
    records = []
    page = int(page)
    limit = int(limit)

    # 获取该用户所有订单的列表
    all_order_list = r_2.lrange(token_, 0, -1)
    total = len(all_order_list)
    for i, x_ in enumerate(all_order_list, start=1):
        user_order = r_2.hgetall(x_)
        order_detail_list = json.loads(user_order["orderDetailList"])
        records.append({
            "id": i,
            "consignee": json.loads(user_order["consignee"]),
            "consigneeTel": json.loads(user_order["consigneeTel"]),
            "totalAmount": sum([int(x_["orderPrice"]) for x_ in order_detail_list]),
            "orderStatus": "UNPAID",
            "userId": user_id,
            "paymentWay": json.loads(user_order["paymentWay"]),
            "deliveryAddress": json.loads(user_order["deliveryAddress"]),
            "orderComment": json.loads(user_order["orderComment"]),
            "outTradeNo": get_order_code(),
            "tradeBody": [x_["skuName"] for x_ in order_detail_list][0],
            "createTime": str(datetime.now().replace(microsecond=0)),
            "expireTime": str(datetime.now().replace(microsecond=0) + timedelta(days=1)),
            "processStatus": "UNPAID",
            "trackingNo": None,
            "parentOrderId": None,
            "imgUrl": [x_["imgUrl"] for x_ in order_detail_list][0],
            "orderDetailList": order_detail_list,
            "orderStatusName": "未支付",
            "wareId": None
        })

    # 首页默认分页效果
    limit_start = (page - 1) * limit

    # 采用切片方式方便分页
    records = records[limit_start:page * limit]

    # 获取分页总数
    page_total = int(math.ceil(total / limit))

    data = {
        "records": records,
        "total": total,
        "size": limit,
        "current": page,
        "pages": page_total
    }

    return jsonify({
        "code": 200,
        "message": "成功",
        "data": data,
        "ok": True
    })


# 查看当前用户所有的收货地址的接口
@bp.get("/userAddress/auth/findUserAddressList")
@login_required
@swagger.validate(headers=Header, resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def user_address_list():
    all_shipping_address = list(Shipping_address.find({"connect_username": g.username},
                                                      {"_id": 0}))
    if all_shipping_address:
        return jsonify({
            "code": 200,
            "message": "成功",
            "data": all_shipping_address,
            "ok": True
        })

    return jsonify({
        "code": 201,
        "message": "用户收货地址为空！",
        "data": None,
        "ok": False
    })


# 添加收货地址信息
@bp.route("/add_shipping_address", methods=["GET", "POST"])
@login_required
@swagger.validate(headers=Header, body=ShippingAddress,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def add_shipping_address():
    # 首先获取该用户收货地址总数，看看是否超过6个
    ship_address_count = Shipping_address.count_documents({"username": g.username})
    all_ship_address = Shipping_address.count_documents({})
    if ship_address_count > 5:
        return jsonify({"err": "抱歉，你已经有6个收货地址了，不能再添加更多了"})
    # 创建一个自增长id
    if ship_address_count == 0:
        id = all_ship_address + 1
    else:
        id_list = list(Shipping_address.find().sort("id", -1))
        id = id_list[0]["id"] + 1

    customer_name = request.json.get("customer_name")
    shipping_address = request.json.get("shipping_address")
    customer_number = request.json.get("customer_number")

    Shipping_address.insert_one({"id": id, "customer_name": customer_name,
                                 "shipping_address": shipping_address,
                                 "customer_number": customer_number,
                                 "username": g.username})

    return jsonify({"msg": "收货地址添加成功！！！"})


# 修改收货地址信息
@bp.route("/edit_shipping_address", methods=["GET", "POST"])
@login_required
@swagger.validate(headers=Header, body=ShippingAddress,
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['trades'])
def edit_shipping_address():
    id = request.json.get("id")
    user_address = Shipping_address.find_one({"id": id, "username": g.username})
    if not user_address:
        return jsonify({"err": "抱歉，该收货地址不存在！"})

    X = request.get_json()

    for k in X:
        Shipping_address.update_one({"id": id, "username": g.username},
                                    {"$set": {k: X[k]}})

    return jsonify({"msg": "收货地址信息修改成功！"})
