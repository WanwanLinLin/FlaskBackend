# -*- coding: utf-8 -*-
import os

from flask import Blueprint, request, jsonify

bp = Blueprint("admin_file_controller", __name__)


@bp.route("/fileUpload", methods=["GET", "POST"])
def file_upload():
    img = request.files.get("file")
    base_dir = "http://127.0.0.1:8000/static/trademark/"
    full_path = base_dir + img.filename
    img.save("D:/github_projects/FlaskProject/static/trademark/" + img.filename)
    print(full_path)
    return jsonify({
        "code": 200,
        "message": "文件上传成功!",
        "data": full_path,
        "ok": True
    })

