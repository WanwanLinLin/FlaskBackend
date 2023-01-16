# -*- coding: utf-8 -*-
import os

from pathlib import Path
from flask import Blueprint, request, jsonify
from auth import permission_required
from extension import swagger
from flask_pydantic_spec import Response as fp_Response
from flask_pydantic_spec import MultipartFormRequest
from .validate import XApiKey
from utils import create_numbering, TRADEMARK_PATH, CATEGORY_PATH

bp = Blueprint("admin_file_controller", __name__)


# 专门用于处理品牌图片
@bp.post("/fileUpload")
@permission_required
@swagger.validate(headers=XApiKey, body=MultipartFormRequest(),
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage file'])
def file_upload():
    img = request.files.get("file")
    base_dir = "http://127.0.0.1:8000/static/trademark/"
    full_path = base_dir + img.filename

    my_file = Path(TRADEMARK_PATH + img.filename)
    if my_file.exists():
        return jsonify({
            "code": 201,
            "message": "Sorry, the file name cannot be duplicate!",
            "data": None,
            "ok": False
        })

    img.save(TRADEMARK_PATH + '/' + img.filename)
    return jsonify({
        "code": 200,
        "message": "Successfully uploaded the file!",
        "data": full_path,
        "ok": True
    })


# 专门用于增加SPU图片
@bp.post("/fileUpload_2")
@permission_required
@swagger.validate(headers=XApiKey, body=MultipartFormRequest(),
                  resp=fp_Response(HTTP_200=None, HTTP_403=None), tags=['admin manage file'])
def file_upload_2():
    img = request.files.get("file")
    base_dir = "http://127.0.0.1:8000/static/category_image/"
    suffix_name = create_numbering(8)
    full_path = base_dir + f"{suffix_name}_" + img.filename
    img.save(CATEGORY_PATH + '/' + f"{suffix_name}_" + img.filename)
    return jsonify({
        "code": 200,
        "message": "Successfully uploaded the file!",
        "data": full_path,
        "ok": True
    })

# 专门用于删除SPU图片
