# -*- coding: UTF-8 -*-
from sklearn.naive_bayes import GaussianNB
import numpy as np
import os
import sys

sys.path.append('../..')

from model.evaluate import DbEvaluate
from service.train import getModelByGroup

# 分组个数
groupNum = 15
# 每个组测试集占比
testPercentage = 0.2
# 模型id
modelId = "5eaa738b471bb8100538ad4543546a66"

db = DbEvaluate()
trainModel = db.getBayesModel(modelId)

def classifyNB(vec2Classify, n_name):

    trainMatrix, trainCategory = getModelByGroup(n_name, "dispersed", trainModel, groupNum, testPercentage)

    model = GaussianNB()

    model.fit(trainMatrix, trainCategory)
    predicted = model.predict(vec2Classify)
    return predicted[0]

def dating_class_test(n_name):

    testMatrix, testCategory = getModelByGroup(n_name, "test", trainModel, groupNum, testPercentage)

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

        print ("the classifier came back with: %s, the real answer is: %s %s %s" % (cls, actual, notice, too_many))

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