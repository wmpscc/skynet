# -*- coding: UTF-8 -*-
from __future__ import division
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import operator
from sklearn import preprocessing
import os
import sys


sys.path.append('../..')

from model.evaluate import DbEvaluate
from service.train import getModelByGroup

# 分组个数
groupNum = 6
# 每个组测试集占比
testPercentage = 0.2
# 模型id
modelId = "b28c2c3f2a479b809fce69a318ac67b0"

db = DbEvaluate()
trainModel = db.getKnnModel(modelId)
originModel = db.getKnn(modelId)

def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

def one_hot_norm(data_set):
    enc = preprocessing.OneHotEncoder()
    enc.fit(data_set)
    return enc.transform(data_set).toarray()

def classifyNB(vec2Classify, n_name):
    dating_data_mat_linear, testCategory, allIds = getModelByGroup(n_name, "dispersed", trainModel, originModel["ids"], groupNum, testPercentage)

    norm_mat_linear = z_score_norm(dating_data_mat_linear)
    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(norm_mat_linear,testCategory)

    predicted = knn_classifier.predict(vec2Classify)
    return predicted[0]


def dating_class_test(n_name):
    dating_data_mat_linear, testCategory, allIds = getModelByGroup(n_name, "test", trainModel, originModel["ids"], groupNum, testPercentage)

    testMatrix = z_score_norm(dating_data_mat_linear)

    right_count = 0.0
    for key,line in enumerate(testMatrix):
        cls = classifyNB([line], n_name)
        actual = testCategory[key]

        notice = ""
        if (cls == actual):
            right_count += 1.0

        if (cls != actual):
            notice = "fail"

        cha = cls-actual
        too_many = ""
        if cha >= 3 or cha <= -3 :
            too_many = "many"

        print ("pid is %s, the classifier came back with: %s, the real answer is: %s %s %s" % (allIds[key],cls, actual, notice, too_many))

        #print key,line,cls
    rate = right_count/len(testCategory)
    print ("the total right rate is: %f" % (rate))
    print ("error num is: %f" % int((len(testCategory)-right_count)))
    print ("right num is: %f" % int(right_count))

    return rate

def dating_class_test_all():

    total = 0
    for n_name in range(10):
        n_name = '%s' % n_name
        total += dating_class_test(n_name)

    print ("\n")

    print ("avg rate is: %f" % (total/10))

dating_class_test_all()



