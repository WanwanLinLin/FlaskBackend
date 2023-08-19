说明：

    1.已经废弃的集合：Goods_se
    2.develop分支用于创建新版本的后端
    3.接口文档地址： http://127.0.0.1:8000/apidoc/swagger
    4.Python版本：3.8.16
    5.为了省事，基本所有的数据都用mongo存储


尚品汇，启动！(方式)：
    
    1. git clone -b develop https://github.com/WanwanLinLin/FlaskBackend.git    
    
    2.准备好Python虚拟环境，推荐 miniconda
    
    3.安装依赖项：pip install -r requirements.txt
    
    4.准备好 mysql, mongo, redis 数据库，其中mysql，要事先创建一个数据库，
    运行项目会自动创建表，数据库配置细节详见根目录下的db.py和nosql_db.py
    
    5. cd ./apps
    
    6.运行 python get_an_admin.py , 创建一名1级管理员，
      账号：admin
      密码：admin
    
    7.运行 python run.py 即可成功启动项目


待优化事项：

    1.商品搜索建议自行添加elasticsearch进行优化
    ...


欢迎向我私信：
B站
![image](https://github.com/WanwanLinLin/FlaskBackend/blob/develop/erweima/B%E7%AB%99.jpg?raw=true)

抖音
![image](https://github.com/WanwanLinLin/FlaskBackend/blob/develop/erweima/%E6%8A%96%E9%9F%B3.jpg?raw=true)



![image](D:/TyporaImages/shopcart.png)