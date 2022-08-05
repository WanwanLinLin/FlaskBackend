# -*- coding: utf-8 -*-
import math

from .validate import VaListModel
from pydantic import error_wrappers
from flask import Blueprint, jsonify, request
from .models import Goods, Goods_se, Goods_se_attrs, CategoryListModel, SeCategoryListModel, ThCategoryListModel

bp = Blueprint("goods", __name__)


# 展示所有nft的接口
@bp.route("/display", methods=["GET", "POST"])
def display():
    info = list(Goods.find({}, {"_id": 0, "id": 0}))
    print(info)

    l = []
    for x in info:
        l.append(x)

    return jsonify({"info": l})


# 返回所有类别列表数据(三级联动)
@bp.route("/getBaseCategoryList", methods=["GET", "POST"])
def get_base_category_list():
    first_list = CategoryListModel.query.all()
    # print(first_list)
    data = []

    for i, x in enumerate(first_list, start=1):
        data.append({"categoryName": x.name,
                     "categoryId": x.id,
                     "categoryChild": []})
        l = SeCategoryListModel.query.filter(SeCategoryListModel.category_par == x.id).all()
        # print(l)
        # print(x.my_CategoryListModel[0].name)
        if l:

            for i_, y in enumerate(l, start=1):
                data[i - 1]["categoryChild"].append({"categoryName": y.name,
                                                     "categoryId": y.id,
                                                     "categoryChild": []})
                l_ = ThCategoryListModel.query.filter(ThCategoryListModel.category_par == y.id).all()
                # print(y.id)
                # print(y)
                print(l_)
                if l_:
                    for z in l_:

                        if z.category_par == y.id:
                            # print(y.id)
                            data[i - 1]["categoryChild"][i_ - 1]["categoryChild"].append({"categoryName": z.name,
                                                                                          "categoryId": z.id,
                                                                                          })

    return jsonify({
        "code": 200,
        "message": "成功！",
        "ok": True,
        "data": data
    }
    )


# 根据筛选条件返回商品的列表
@bp.route("/list", methods=["GET", "POST"])
def list_():
    try:
        # print("这里执行了——1")

        VaListModel(**request.get_json())
    except error_wrappers.ValidationError as e:
        print(e)
        return e.json()
    else:
        X = request.get_json()
        print(X)
        # print("这里执行了——2")
        trademark_list = []
        attrs_list = []
        goods_list = []

        # 第一种情况：前端不传参数
        if not X:
            all_info = list(Goods_se.find({}, {"_id": 0}))
            attrs_info = list(Goods_se_attrs.find({}, {"_id": 0, "connect_name": 0}))
            # print(attrs_info, "\n")
            for x in all_info:
                trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
            # 获取不重复的品牌数据
            trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]

            for x_ in all_info:
                attrs_list_ = list(Goods_se_attrs.find({"connect_name": x_["tmName"]}, {"_id": 0, "connect_name": 0}))
                x_["attrs"] = attrs_list_
                goods_list.append(x_)
            # print(goods_list, "\n")

            for y in attrs_info:
                attrs_list.append(y)

            return jsonify({
                "code": 200,
                "message": "成功",
                "data": {
                    "trademarkList": trademark_list,
                    "attrsList": attrs_list,
                    "goodsList": goods_list,
                    "total": 11,
                    "pageSize": 10,
                    "pageNo": 1,
                    "totalPages": 4
                },
                "ok": True
            })

        # 第二种情况，前端传递来了参数
        category1_id = request.json.get("category1Id")
        category2_id = request.json.get("category2Id")
        category3_id = request.json.get("category3Id")
        category_name = request.json.get("categoryName")
        keyword = request.json.get("keyword")
        props = request.json.get("props")
        trademark = request.json.get("trademark")
        order = request.json.get("order")
        page_no = request.json.get("pageNo")
        page_size = request.json.get("pageSize")
        print("keyword: ", keyword)

        # 先实现简单的分页效果
        # 该变量用于表示跳过前面多少条
        limit_start = (page_no - 1) * page_size

        if category1_id:
            all_info_2 = list(Goods_se.find({"category1Id": category1_id,
                                             "category1Name": category_name},
                                            {"_id": 0}))
        elif category2_id:
            all_info_2 = list(Goods_se.find({"category2Id": category2_id,
                                             "category2Name": category_name},
                                            {"_id": 0}))
        else:
            all_info_2 = list(Goods_se.find({"category3Id": category3_id,
                                             "category3Name": category_name},
                                            {"_id": 0}))
        print(all_info_2, "\n")

        if all_info_2 and keyword:
            # 这是对应同时使用三级类目导航和keyword导航的情况的情况
            for x in all_info_2:
                # if x["tmName"] == keyword:
                if keyword in x["tmName"]:
                    trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

            for x_ in all_info_2:
                # if x_["tmName"] == keyword:
                if keyword in x_["tmName"]:
                    attrs_list_ = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
                                                           {"_id": 0, "connect_name": 0}))
                    x_["attrs"] = attrs_list_
                    goods_list.append(x_)

            if goods_list:
                attrs_list += goods_list[0]["attrs"]

        elif all_info_2:
            # 这是对应只有三级类目导航的情况
            for x in all_info_2:
                trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

            for x_ in all_info_2:
                attrs_list_ = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
                                                       {"_id": 0, "connect_name": 0}))
                x_["attrs"] = attrs_list_
                goods_list.append(x_)

            if goods_list:
                attrs_list += goods_list[0]["attrs"]

        elif keyword:
            # 这是对应只有 keyword 的情况
            # all_info_3 = list(Goods_se.find({"tmName": keyword}, {"_id": 0}))
            # 实现了简易版的模糊搜索
            all_info_3 = list(Goods_se.find({}, {"_id": 0}))
            for x in all_info_3:
                if keyword in x["tmName"]:
                    trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})

            for x_ in all_info_3:
                if keyword in x_["tmName"]:
                    attrs_list_ = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
                                                       {"_id": 0, "connect_name": 0}))
                    x_["attrs"] = attrs_list_
                    goods_list.append(x_)
            # .sort("id", 1).limit(page_size).skip(limit_start)
            if goods_list:
                attrs_list += goods_list[0]["attrs"]

        else:
            all_info_4 = list(Goods_se.find({}, {"_id": 0}))
            attrs_info = list(Goods_se_attrs.find({}, {"_id": 0, "connect_name": 0}))
            # print(attrs_info, "\n")
            for x in all_info_4:
                trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
            # 获取不重复的品牌数据
            trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]

            for x_ in all_info_4:
                attrs_list_ = list(Goods_se_attrs.find({"connect_name": x_["tmName"]}, {"_id": 0, "connect_name": 0}))
                x_["attrs"] = attrs_list_
                goods_list.append(x_)
            # print(goods_list, "\n")

            for y in attrs_info:
                attrs_list.append(y)


        # 采用切片方式方便分页
        goods_list = goods_list[limit_start:page_no*page_size]
        # 获取不重复的品牌数据
        trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]

        # 获取分页总数
        page_total = int(math.ceil(len(goods_list) / page_size))

        return jsonify({
            "code": 200,
            "message": "成功",
            "data": {
                "trademarkList": trademark_list,
                "attrsList": attrs_list,
                "goodsList": goods_list,
                "total": len(goods_list),
                "pageSize": page_size,
                "pageNo": page_no,
                "totalPages": page_total
            },
            "ok": True
        })
