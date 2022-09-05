# -*- coding: utf-8 -*-
import os

from pathlib import Path
from flask import Blueprint, request, jsonify
from apps.utils import create_numbering

bp = Blueprint("admin_file_controller", __name__)


# 专门用于处理品牌图片
@bp.route("/fileUpload", methods=["GET", "POST"])
def file_upload():
    img = request.files.get("file")
    base_dir = "http://127.0.0.1:8000/static/trademark/"
    full_path = base_dir + img.filename

    my_file = Path("D:/github_projects/FlaskProject/static/trademark/" + img.filename)
    if my_file.exists():
        return jsonify({
            "code": 201,
            "message": "抱歉，文件名不能重复！!",
            "data": None,
            "ok": False
        })

    img.save("D:/github_projects/FlaskProject/static/trademark/" + img.filename)
    print(full_path)
    return jsonify({
        "code": 200,
        "message": "文件上传成功!",
        "data": full_path,
        "ok": True
    })


# 专门用于增加SPU图片
@bp.route("/fileUpload_2", methods=["GET", "POST"])
def file_upload_2():
    img = request.files.get("file")
    base_dir = "http://127.0.0.1:8000/static/category_image/"
    suffix_name = create_numbering(8)
    full_path = base_dir + f"{suffix_name}_" + img.filename
    img.save("D:/github_projects/FlaskProject/static/category_image/" + f"{suffix_name}_" + img.filename)
    # print(full_path)
    return jsonify({
        "code": 200,
        "message": "文件上传成功!",
        "data": full_path,
        "ok": True
    })

# 专门用于删除SPU图片
