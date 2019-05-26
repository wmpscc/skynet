# -*- coding: UTF-8 -*-
from __future__ import division
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import preprocessing
import sys

sys.path.append('../..')

from model.evaluate import DbEvaluate

#knn算法#
def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

def one_hot_norm(data_set):
    enc = preprocessing.OneHotEncoder()
    enc.fit(data_set)
    return enc.transform(data_set).toarray()


def classifyKnn(vec2Classify, modelId):

    db = DbEvaluate()
    trainModel = db.getKnnModel(modelId)

    dating_data_mat_linear = trainModel['feature']
    testCategory = trainModel['classificate']

    norm_mat_linear = z_score_norm(dating_data_mat_linear)
    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(norm_mat_linear,testCategory)

    predicted = knn_classifier.predict(vec2Classify)
    return predicted[0]


#朴树贝叶斯（高斯模型）#
def classifyBayes(vec2Classify, modelId):

    db = DbEvaluate()
    trainModel = db.getKnnModel(modelId)

    trainMatrix = trainModel['feature']
    trainCategory = trainModel['classificate']

    model = GaussianNB()

    model.fit(trainMatrix, trainCategory)
    predicted = model.predict(vec2Classify)
    return predicted[0]


#决策树#
def classifyTree(vec2Classify, modelId):
    db = DbEvaluate()
    trainModel = db.getKnnModel(modelId)

    trainMatrix = trainModel['feature']
    trainCategory = trainModel['classificate']

    model = tree.DecisionTreeClassifier()
    model.fit(trainMatrix, trainCategory)

    predicted = model.predict(vec2Classify)
    return predicted[0]

#逻辑控制#

def classify(vec2Classify, modelId) :
    price = 0

    knnPrice = classifyKnn([vec2Classify], modelId)
    price += knnPrice

    bayesPrice = classifyBayes([vec2Classify], modelId)
    price += bayesPrice

    treePrice = classifyTree([vec2Classify], modelId)
    price += treePrice

    return round(price/3, 2)




