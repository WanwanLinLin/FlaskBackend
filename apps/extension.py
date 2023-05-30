# -*- coding: utf-8 -*-
from flask_pydantic_spec import FlaskPydanticSpec


swagger = FlaskPydanticSpec("FlaskBackend", title="商品汇前后台接口文档", version="v1.0")


def init_swagger(app):
    swagger.register(app)