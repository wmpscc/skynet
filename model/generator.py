# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from model.connection import getDBSession

Base = declarative_base()

class Generator(Base):
    # 表的名字
    __tablename__ = 'generator'

    # 表的结构
    id = Column(Integer, primary_key=True)


class DbGenerator:

    def __init__(self):

        self.session = getDBSession()

    def id(self):
        generator = Generator()
        self.session.add(generator)
        self.session.commit()
        return generator.id