# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from model.connection import getDBSession
import json

Base = declarative_base()

class Evaluate(Base):
    # 表的名字
    __tablename__ = 'evaluate'

    # 表的结构
    unique_id = Column(String(32), primary_key=True)
    bayes_model = Column(String(20))
    bayes_open = Column(Integer)
    knn_model = Column(String(20))
    knn_open = Column(Integer)
    tree_model = Column(String(20))
    tree_open = Column(Integer)

class DbEvaluate:

    def __init__(self):

        self.session = getDBSession()

    def _getModel(self, unique_id):
        return self.session.query(Evaluate).filter_by(unique_id=unique_id).first()

    def getKnnModel(self, unique_id):
        my_evaluate = self._getModel(unique_id)
        origin = json.loads(my_evaluate.knn_model)
        return origin["train"]

    def getBayesModel(self, unique_id):
        my_evaluate = self._getModel(unique_id)

        origin = json.loads(my_evaluate.bayes_model)
        return origin["train"]

    def getTreeModel(self, unique_id):
        my_evaluate = self._getModel(unique_id)

        origin = json.loads(my_evaluate.tree_model)
        return origin["train"]

    def getKnn(self, unique_id):
        my_evaluate = self._getModel(unique_id)
        origin = json.loads(my_evaluate.knn_model)
        return origin

    def getBayes(self, unique_id):
        my_evaluate = self._getModel(unique_id)

        origin = json.loads(my_evaluate.bayes_model)
        return origin

    def getTree(self, unique_id):
        my_evaluate = self._getModel(unique_id)

        origin = json.loads(my_evaluate.tree_model)
        return origin

    def getOne(self, unique_id):
        return self._getModel(unique_id)

