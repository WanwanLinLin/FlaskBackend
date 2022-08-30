# -*- coding: utf-8 -*-
from flask import Flask
from flask_caching import Cache
from apps.users import bp as users_bp
from apps.trades import bp as trades_bp
from apps.goods import bp as goods_bp
from apps.account import bp as account_bp
from apps.admin_trade_mark import bp as admin_trade_mark_bp
from apps.admin_file_ontroller import bp as admin_file_controller_bp
from apps.admin_category_management import bp as admin_category_management_bp
from apps.extension import init_swagger
from flask_login import LoginManager
from flask_cors import CORS
from apps import db, init_database
from apps.account import user_cli

login_manager = LoginManager()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.serect_key = "SERECT"
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)
init_database(app)
app.cli.add_command(user_cli)


@login_manager.user_loader
def load_user(username):
    """
        使用 Flask Login 必须创建一个user_loader回调函数
        来根据session中取回的user ID（unicode）
        取得user对象，ID 无效应返回None
        """
    from apps.users import User
    try:
        user = User.find_one({"username": username})
    except Exception:
        user = None
    return user


login_manager.init_app(app)

# 处理中文编码
app.config["JSON_AS_ASCII"] = False
init_swagger(app)


# 注册蓝图
app.register_blueprint(users_bp, url_prefix="/v1/users")
app.register_blueprint(trades_bp, url_prefix="/v1/trades")
app.register_blueprint(goods_bp, url_prefix="/v1/goods")
app.register_blueprint(account_bp, url_prefix="/v1/admin")
app.register_blueprint(admin_trade_mark_bp, url_prefix="/v1/admin/product")
app.register_blueprint(admin_file_controller_bp, url_prefix="/v1/admin/fileController")
app.register_blueprint(admin_category_management_bp, url_prefix="/v1/admin/categoryManagement")


@app.route("/", methods=["GET", "POST"])
def hello():
    return "There will be a flask project!!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000)
