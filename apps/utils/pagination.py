# -*- coding: utf-8 -*-
# 实现简单的分页效果
import math


def my_pagination(records, page, limit):
    limit_start = (page - 1) * limit
    # 获取总数量
    total = len(records)
    # 获取实际需要展示的条数
    records = records[limit_start:page * limit]
    # 获取分页总数
    pages = int(math.ceil(total / limit))
    return page, total, records
