# -*- coding: utf-8 -*-
from flask import Response
import pymongo, redis
from flask import Flask
from flask_caching import Cache
from apps.users import bp as users_bp
from apps.trades import bp as trades_bp
from apps.goods import bp as goods_bp
from apps.extension import init_swagger

# 连接数据库
# client = pymongo.MongoClient("mongodb://localhost/", 27017)
# pool = redis.ConnectionPool(host="127.0.1", port=6379, db=3, decode_responses=True)
# r = redis.Redis(connection_pool=pool)


app = Flask(__name__)

app.serect_key = "SERECT"
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)
init_swagger(app)



# 注册蓝图
app.register_blueprint(users_bp, url_prefix="/v1/users")
app.register_blueprint(trades_bp, url_prefix="/v1/trades")
app.register_blueprint(goods_bp, url_prefix="/v1/goods")


@app.route("/", methods=["GET", "POST"])
def hello():
    return "There will be a flask project!!"


if __name__ == '__main__':
    app.run(port=8888)
