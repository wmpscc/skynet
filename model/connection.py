# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 数据库连接
def getDBSession():
    engine = create_engine('mysql+mysqlconnector://root:421421mfw@localhost:3306/car')

    # 创建DBSession类型
    DBSession = sessionmaker(bind=engine)

    return DBSession()