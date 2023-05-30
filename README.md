说明：

    1.已经废弃的集合：Goods_se
    2.develop分支用于创建新版本的后端
    3.接口文档地址： http://127.0.0.1:8000/apidoc/swagger
    4.Python版本：3.8.16
    5.为了省事，基本所有的数据都用mongo存储


尚品汇，启动！(方式)：

    1.准备好Python虚拟环境，推荐miniconda
    2.安装依赖项：pip install -r requirements.txt
    3.准备好 mysql, mongo, redis 数据库，其中mysql，要事先创建一个数据库，
    运行项目会自动创建表，数据库配置细节详见根目录下的db.py和nosql_db.py
    4.命令行进入app目录下，运行 python run.py 即可成功启动项目


待优化事项：
    
    1.文件上传接口可能有点问题
    2.商品搜索建议自行添加elasticsearch进行优化
    ...

    
    