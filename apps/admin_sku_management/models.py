# -*- coding: utf-8 -*-
from apps.nosql_db import client

"""
存放sku信息的数据库
    注意：一个SPU可能会有多个SKU实例
"""
Goods_se_details_sku = client.goods.Goods_se_details_sku