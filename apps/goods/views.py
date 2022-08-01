# -*- coding: utf-8 -*-
from .models import Goods, CategoryListModel, SeCategoryListModel, ThCategoryListModel
from flask import Blueprint, jsonify, request

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
