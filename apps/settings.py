# -*- coding: utf-8 -*-
import os

# 保存上传文件的目录
path1 = os.path.dirname(os.path.abspath(__file__))
upload_file_path = os.path.join(path1, "static", "trademark")
print(upload_file_path)
os.remove("D:/github_projects/FlaskProject/static/upload_file/干捞螺蛳粉.png")
