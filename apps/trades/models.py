# -*- coding: utf-8 -*-
import time
from apps.nosql_db import client

# 订单集合
Orders = client.trade.orders

# 个人作品集合
Portfolios = client.trade.portfolios

# nft 列表集合
NFT_list = client.trade.nftlists

# 评论表集合
Comments = client.trade.comments

# 点赞表集合
Portfolios_like = client.trade.portfolios_likes

# 收货地址集合
Shipping_address = client.users.shipping_address

# 登录注册集合
User = client.users.information


# zuopin_ = Portfolios.find_one({"id": 3})
#
# zuopin = zuopin_["_id"]
# Portfolios_like.insert_one({"id": 2, "comment_por": zuopin,
#                      "portfolios_name": zuopin_["name"],
#                      "username": "SunXiaoChuan",
#                      "comment_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                      })

# for i in range(10):
#     id_list = list(NFT_list.find().sort("id", -1))
#     id = id_list[0]["id"] + 1
#     NFT_list.insert_one({"id": id, "name": "Monkey", "image": f"googou.{i}.cnm"})
#
# for i in range(10):
#     id_list = list(NFT_list.find().sort("id", -1))
#     id = id_list[0]["id"] + 1
#     NFT_list.insert_one({"id": id, "name": "Kid", "image": f"googou.{i}.cnm"})
