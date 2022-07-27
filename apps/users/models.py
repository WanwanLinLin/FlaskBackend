# -*- coding: utf-8 -*-
import redis
from apps.db import client
from apps.db import pool


# 登录注册集合
User = client.users.information

# 收货地址集合
Shipping_address = client.users.shipping_address


