#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入依赖
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类
Base = declarative_base()

# 定义User对象
class Evaluate(Base):
    # 表的名字
    __tablename__ = 'evaluate'

    # 表的结构
    unique_id = Column(String(32), primary_key=True)
    bayes_model = Column(String(20))
    knn_model = Column(String(20))
    tree_model = Column(String(20))


# 初始化数据库链接
engine = create_engine('mysql+mysqlconnector://root:421421mfw@localhost:3306/car')

# 创建DBSession类型
DBSession = sessionmaker(bind=engine)

session = DBSession()

# 添加

# new_user = Evaluate(unique_id='sads', bayes_model='Bob', knn_model='Bob', tree_model='Bob')
# session.add(new_user)
# session.commit()
# session.close()

# 查询

my_evaluate = session.query(Evaluate).filter_by(unique_id="sads").first()
print(my_evaluate.unique_id)