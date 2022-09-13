# -*- coding: utf-8 -*-
"""
这是一个可传入参数的装饰器，用于验证post请求的字段
"""
from functools import wraps
from pydantic import error_wrappers
from flask import request, jsonify


def check_field(one_validate_class):
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            try:
                one_validate_class(**request.get_json())
            except error_wrappers.ValidationError as e:
                return e.json()
            return func(*args, **kwargs)

        return decorate

    return wrapper