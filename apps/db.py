# -*- coding：utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 出租屋的mysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:2298315584@127.0.0.1:3306/sph_flask?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()