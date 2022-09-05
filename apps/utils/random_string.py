# -*- coding: utf-8 -*-
import os
import binascii


def create_numbering(length=24):
    """创建一个随机的订单编号"""
    s = binascii.b2a_base64(os.urandom(length))[:-1].decode('utf-8')
    for x in ['+', '=', '/', '?', '&', '%', "#"]:
        s = s.replace(x, "")
    return s