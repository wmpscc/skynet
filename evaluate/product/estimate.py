# -*- coding: UTF-8 -*-
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
import numpy as np
import operator
from sklearn import preprocessing
import os
import math
import time


root_dir = os.path.abspath(os.path.join(os.getcwd(), "../"))

#工具#
def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(int(line))

    return class_label_vector


def file2arrayexpand(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(list(map(float, line.split(' '))))
    return class_label_vector

def avgInfo(n_name) :
    filename = root_dir + "/input/product/" + n_name + ".txt"
    listCar = file2arrayexpand(filename)

    total = len(listCar)
    kilo = 0
    card = 0
    quality = 0
    for car in listCar:
        kilo += car[0]
        card += car[1]
        quality += car[2]

    timeArray = time.localtime(math.ceil(card/total))
    otherStyleTime = time.strftime("%Y-%m", timeArray)

    return round(kilo/total, 2), otherStyleTime, math.ceil(quality/total)

#knn算法#
def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

def one_hot_norm(data_set):
    enc = preprocessing.OneHotEncoder()
    enc.fit(data_set)
    return enc.transform(data_set).toarray()


def classifyKnn(vec2Classify, n_name):

    dating_data_mat_linear = file2arrayexpand(
        root_dir + "/input/product/"+n_name+".txt")
    norm_mat_linear = z_score_norm(dating_data_mat_linear)


    testCategory = file2array(root_dir+"/input/product/"+n_name+"_cat.txt")


    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(norm_mat_linear,testCategory)

    predicted = knn_classifier.predict(vec2Classify)
    return predicted[0]


#朴树贝叶斯（高斯模型）#
def classifyBayes(vec2Classify, n_name):
    trainMatrix = file2arrayexpand(root_dir+"/input/product/"+n_name+".txt")
    trainCategory = file2array(root_dir+"/input/product/"+n_name+"_cat.txt")

    model = GaussianNB()

    model.fit(trainMatrix, trainCategory)
    predicted = model.predict(vec2Classify)
    return predicted[0]


#决策树#
def classifyTree(vec2Classify, n_name):
    trainMatrix = file2arrayexpand(root_dir+"/input/product/"+n_name+".txt")
    trainCategory = file2array(root_dir+"/input/product/"+n_name+"_cat.txt")

    model = tree.DecisionTreeClassifier()
    model.fit(trainMatrix, trainCategory)

    predicted = model.predict(vec2Classify)
    return predicted[0]

#逻辑控制#

def classify(vec2Classify, n_name) :
    knnPrice = classifyKnn([vec2Classify], n_name)
    print "knn answer is: %sw" % (knnPrice)

    treeBayes = classifyBayes([vec2Classify], n_name)
    print "bayes answer is: %sw" % (treeBayes)

    treePrice = classifyTree([vec2Classify], n_name)
    print "tree answer is: %sw" % (treePrice)

    kilo, card, quality = avgInfo(n_name)
    print "样本平均"
    print "   %s 公里" % (kilo)
    print "   %s 上牌" % (card)
    print "   %s 处异常" % (quality)


classify([3.29,1409795550,14], "macan_2014")


