# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from model.connection import getDBSession

import model.generator

Base = declarative_base()

class Source(Base):
    # 表的名字
    __tablename__ = 'source'

    # 表的结构
    id = Column(Integer, primary_key=True)
    source_id = Column(String(512))
    type = Column(Integer)
    title = Column(String)
    content = Column(String)
    status = Column(Integer)
    intention = Column(Integer)
    operate_sort = Column(Integer)


class DbSource:

    def __init__(self):

        self.session = getDBSession()

    def getWaitDetermineForeachList(self, id, status, intention):
        return self.session.query(Source).filter(Source.id >id, Source.status==status, Source.intention == intention).order_by(Source.id.asc()).limit(100).all()

    def getDetermineForeachList(self, id, status):
        return self.session.query(Source).filter(Source.id >id, Source.status==status).order_by(Source.id.asc()).limit(100).all()
    def suspectedSell(self, id):

        db = model.generator.DbGenerator()
        operate_sort = db.id()

        cur = self.session.query(Source).get(id)
        cur.intention = 8
        cur.status = 9
        cur.operate_sort = operate_sort
        self.session.add(cur)
        self.session.commit()

    def suspectedBuy(self, id):
        db = model.generator.DbGenerator()
        operate_sort = db.id()

        cur = self.session.query(Source).get(id)
        cur.intention = 4
        cur.status = 9
        cur.operate_sort = operate_sort
        self.session.add(cur)
        self.session.commit()

    def suspectedDefault(self, id):
        db = model.generator.DbGenerator()
        operate_sort = db.id()

        cur = self.session.query(Source).get(id)
        cur.intention = 1
        cur.status = 9
        cur.operate_sort = operate_sort
        self.session.add(cur)
        self.session.commit()