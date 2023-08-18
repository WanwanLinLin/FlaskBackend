# -*- coding: utf-8 -*-
from flask import Flask
from flask_caching import Cache
from users import bp as users_bp
from trades import bp as trades_bp
from goods import bp as goods_bp
from account import bp as account_bp
from admin_trade_mark import bp as admin_trade_mark_bp
from admin_file_ontroller import bp as admin_file_controller_bp
from admin_category_management import bp as admin_category_management_bp
from admin_spu_management import bp as admin_spu_management_bp
from admin_sku_management import bp as admin_sku_management_bp
from flask_cors import CORS
from db import Base, engine
from account import user_cli
from extension import swagger

# 初始化数据库
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.serect_key = "SERECT"
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)
app.cli.add_command(user_cli)
# init_swagger(app)
swagger.register(app)
# 处理中文编码
app.config["JSON_AS_ASCII"] = False

# 注册蓝图
# # 前台部分的模块
app.register_blueprint(users_bp, url_prefix="/v1/users")
app.register_blueprint(trades_bp, url_prefix="/v1/trades")
app.register_blueprint(goods_bp, url_prefix="/v1/goods")
# # 后台管理部分的模块
app.register_blueprint(account_bp, url_prefix="/v1/admin")
app.register_blueprint(admin_trade_mark_bp, url_prefix="/v1/admin/product")
app.register_blueprint(admin_file_controller_bp, url_prefix="/v1/admin/fileController")
app.register_blueprint(admin_category_management_bp, url_prefix="/v1/admin/categoryManagement")
app.register_blueprint(admin_spu_management_bp, url_prefix="/v1/admin/spuManagement")
app.register_blueprint(admin_sku_management_bp, url_prefix="/v1/admin/skuManagement")


@app.get("/")
def hello():
    return "There will be a flask-vue project!!"


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")
