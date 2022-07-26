# -*- coding: utf-8 -*-
from flask_pydantic_spec import FlaskPydanticSpec


swagger = FlaskPydanticSpec("FlaskBackend")


def init_swagger(app):
    swagger.register(app)