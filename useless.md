# from flask_login import LoginManager
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(username):
#     """
#         使用 Flask Login 必须创建一个user_loader回调函数
#         来根据session中取回的user ID（unicode）
#         取得user对象，ID 无效应返回None
#         """
#     from apps.users import User
#     try:
#         user = User.find_one({"username": username})
#     except Exception:
#         user = None
#     return user


# login_manager.init_app(app)
