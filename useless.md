# from flask_login import LoginManager
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(username):
#     """
#         使用 Flask Login 必须创建一个user_loader回调函数
#         来根据session中取回的user ID（unicode）
#         取得user对象，ID 无效应返回None
#         """
#     from apps.users import User
#     try:
#         user = User.find_one({"username": username})
#     except Exception:
#         user = None
#     return user


# login_manager.init_app(app)


#trademark_image = Goods_trademark.find_one({"id": tm_id})["logoUrl"]
#goods_se_tm_name = Goods_trademark.find_one({"id": tm_id})["tmName"]
# Goods_se.insert_one({
    #         "id": goods_se_spu_id,
    #         "defualtImg": trademark_image,
    #         "title": title,
    #         "price": 666,
    #         "createTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
    #         "tmId": tm_id,
    #         "tmName": goods_se_tm_name,
    #         "category3Id": str(category3_id),
    #         "hotScore": 4.0,
    #         "attrs": None,
    #         "inventory": 1000.0,
    #         "description": description
    # })




# 废弃的 list 接口
# 根据筛选条件返回商品的列表
# @bp.route("/list", methods=["GET", "POST"])
# def list_():
#     try:
#         VaListModel(**request.get_json())
#     except error_wrappers.ValidationError as e:
#         print(e)
#         return e.json()
#     else:
#         X = request.get_json()
#         print("request.get_json()的值是：", X)
#         trademark_list = []
#         attrs_list = []
#         goods_list = []
#
#         category1_id = request.json.get("category1Id")
#         category2_id = request.json.get("category2Id")
#         category3_id = request.json.get("category3Id")
#         category_name = request.json.get("categoryName")
#         keyword = request.json.get("keyword")
#         props = request.json.get("props")
#         trademark = request.json.get("trademark")
#         # 下面这三个参数都是有默认值的(由前端决定)
#         order = request.json.get("order")
#         page_no = request.json.get("pageNo")
#         page_size = request.json.get("pageSize")
#
#         # 第一种情况：设置默认页面
#         if not category1_id and not category2_id and not category3_id and not category3_id and \
#                 not category_name and not keyword and not \
#                 props and not trademark:
#             all_info = list(Goods_se.find({"tmId": 1, "tmName": "桂林卤粉"}, {"_id": 0}))
#             # attrs_info = list(Goods_se_attrs.find({"connect_name": "桂林卤粉"}, {"_id": 0, "connect_name": 0}))
#             attrs_info = list(Goods_se_attrs.find({"connect_category3Id": "4"}, {"_id": 0}))
#             # print(attrs_info, "\n")
#             for x in all_info:
#                 trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
#             # 获取不重复的品牌数据
#             trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]
#
#             for x_ in all_info:
#                 goods_list.append(x_)
#             # print(goods_list, "\n")
#
#             for y in attrs_info:
#                 attrs_list.append(y)
#
#             # 首页默认分页效果
#             limit_start = (page_no - 1) * page_size
#             page_total = int(math.ceil(len(goods_list) / page_size))
#             total = len(goods_list)
#             goods_list = goods_list[limit_start:page_no * page_size]
#
#             # 处理order参数
#             if order == "1:asc":
#                 goods_list = sorted(goods_list, key=lambda goods_list: goods_list["hotScore"])
#             elif order == "1:desc":
#                 goods_list = sorted(goods_list, key=lambda goods_list: goods_list["hotScore"], reverse=True)
#             elif order == "2:asc":
#                 goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"])
#             else:
#                 goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"], reverse=True)
#
#             return jsonify({
#                 "code": 200,
#                 "message": "成功",
#                 "data": {
#                     "trademarkList": trademark_list,
#                     "attrsList": attrs_list,
#                     "goodsList": goods_list,
#                     "total": total,
#                     "pageSize": page_size,
#                     "pageNo": page_no,
#                     "totalPages": page_total
#                 },
#                 "ok": True
#             })
#
#         # 第二种情况，前端传递来了参数（默认参数除外）
#         # 先实现简单的分页效果
#         # 该变量用于表示跳过前面多少条
#         limit_start = (page_no - 1) * page_size
#
#         # 处理 trademark 的值
#         if trademark:
#             trademark = trademark.split(":")
#             all_info_2 = list(Goods_se.find({"tmId": int(trademark[0]),
#                                              "tmName": trademark[1]},
#                                             {"_id": 0}))
#
#         # 处理由三级类目列表进行搜索的结果
#         elif category1_id:
#             all_info_2 = list(Goods_se.find({"category1Id": category1_id,
#                                              "category1Name": category_name},
#                                             {"_id": 0}))
#
#         elif category2_id:
#             all_info_2 = list(Goods_se.find({"category2Id": category2_id,
#                                              "category2Name": category_name},
#                                             {"_id": 0}))
#         else:
#             all_info_2 = list(Goods_se.find({"category3Id": category3_id,
#                                              "category3Name": category_name},
#                                             {"_id": 0}))
#
#         if all_info_2 and keyword:
#             # 这是对应同时使用三级类目导航和keyword导航的情况的情况
#             for x in all_info_2:
#                 # if x["tmName"] == keyword:
#                 if keyword in x["tmName"]:
#                     trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
#
#             for x_ in all_info_2:
#                 # if x_["tmName"] == keyword:
#                 if keyword in x_["tmName"]:
#                     # attrs_list = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
#                     #                                       {"_id": 0, "connect_name": 0}))
#                     attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
#                                                           {"_id": 0}))
#                     goods_list.append(x_)
#
#         elif all_info_2:
#             # 这是对应只有三级类目导航的情况
#             for x in all_info_2:
#                 trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
#
#             for x_ in all_info_2:
#                 # attrs_list = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
#                 #                                       {"_id": 0, "connect_name": 0}))
#                 attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
#                                                       {"_id": 0}))
#                 goods_list.append(x_)
#
#         elif keyword:
#             # 这是对应只有 keyword 的情况
#             # all_info_3 = list(Goods_se.find({"tmName": keyword}, {"_id": 0}))
#             # 实现了简易版的模糊搜索
#             all_info_3 = list(Goods_se.find({}, {"_id": 0}))
#             for x in all_info_3:
#                 if keyword in x["tmName"]:
#                     trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
#
#             for x_ in all_info_3:
#                 if keyword in x_["tmName"]:
#                     # attrs_list = list(Goods_se_attrs.find({"connect_name": x_["tmName"]},
#                     #                                       {"_id": 0, "connect_name": 0}))
#                     attrs_list = list(Goods_se_attrs.find({"connect_category3Id": x_["category3Id"]},
#                                                           {"_id": 0}))
#                     goods_list.append(x_)
#
#         else:
#             # all_info_4 = list(Goods_se.find({}, {"_id": 0}))
#             # # attrs_info = list(Goods_se_attrs.find({}, {"_id": 0, "connect_name": 0}))
#             # # print(attrs_info, "\n")
#             # for x in all_info_4:
#             #     trademark_list.append({"tmId": x["tmId"], "tmName": x["tmName"]})
#             # # 获取不重复的品牌数据
#             # trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]
#             #
#             # for x_ in all_info_4:
#             #     attrs_list = list(Goods_se_attrs.find({"connect_name": x_["tmName"]}, {"_id": 0, "connect_name": 0}))
#             #     goods_list.append(x_)
#             pass
#
#         # 处理props参数
#         # （初稿：暂时保留）
#         # if props:
#         #     props_list = []
#         #     for x in props:
#         #         for z in goods_list:
#         #             if x in z["attrs"]:
#         #                 if z not in props_list:
#         #                     props_list.append(z)
#         #     goods_list = props_list
#         #
#         if props:
#             props_list = []
#             for x in props:
#                 x = x.split(":")
#                 for z in goods_list:
#                     for z_ in z["attrs"]:
#                         z_ = list(z_.split(":"))
#                         if x[1] == z_[1] and x[2] == z_[2]:
#                             if z not in props_list:
#                                 props_list.append(z)
#             goods_list = props_list
#         total = len(goods_list)
#         # 采用切片方式方便分页
#         goods_list = goods_list[limit_start:page_no * page_size]
#
#         # 获取不重复的品牌数据
#         trademark_list = [dict(t) for t in set([tuple(d.items()) for d in trademark_list])]
#
#         # 获取分页总数
#         page_total = int(math.ceil(len(goods_list) / page_size))
#
#         # 处理order参数
#         if order == "1:asc":
#             goods_list = sorted(goods_list, key=lambda goods_list: goods_list["hotScore"])
#         elif order == "1:desc":
#             goods_list = sorted(goods_list, key=lambda goods_list: goods_list["hotScore"], reverse=True)
#         elif order == "2:asc":
#             goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"])
#         else:
#             goods_list = sorted(goods_list, key=lambda goods_list: goods_list["price"], reverse=True)
#
#         # print(goods_list, "\n")
#     return jsonify({
#             "code": 200,
#             "message": "成功",
#             "data": {
#                 "trademarkList": trademark_list,
#                 "attrsList": attrs_list,
#                 "goodsList": goods_list,
#                 "total": total,
#                 "pageSize": page_size,
#                 "pageNo": page_no,
#                 "totalPages": page_total
#             },
#             "ok": True
#         })

