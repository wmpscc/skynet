# -*- coding: UTF-8 -*-
'''
Created on Oct 19, 2010

@author: Peter
'''
import numpy as np
import json


#------------新逻辑------------#

def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(line)
    return class_label_vector

def file2arrayexpand(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(line.split(' '))
    return class_label_vector

# 载入训练数据
def loadDataSet ():

    trainMatrix = file2arrayexpand("input/bayes/macan2014_train_dispersed.txt")

    trainCategory = file2array("input/bayes/macan2014_train_cat.txt")

    return trainMatrix, trainCategory

# 存储训练结果
def savetrain(content):
    fo = open("input/bayes/macan2014_train.txt", "w")
    fo.write(content)

# 朴素贝叶斯训练
def trainNB0(trainMatrix, trainCategory):

    # P(A)计算
    category = {}
    category_num = len(trainCategory)
    for category_name in trainCategory:
        category_key = "c:"+bytes(category_name)
        if category.has_key(category_key) :
            category[category_key] += 1
        else:
            category[category_key] = 1
    for key,value in category.items() :
        category[key] = bytes(value)+"/"+bytes(category_num)


    # print category

    # P(B)计算
    characteristics = {}
    for atom_line_val in trainMatrix :
        for atom_key,atom_col in enumerate(atom_line_val) :
            d_key = "d:"+bytes(atom_key)
            t_key = "t:"+bytes(atom_col)

            if characteristics.has_key(d_key) :
                if characteristics[d_key].has_key(t_key):
                    characteristics[d_key][t_key] += 1
                else:
                    characteristics[d_key][t_key] = 1
            else:
                characteristics[d_key] = {}
                characteristics[d_key][t_key] = 1

    for key,value in characteristics.items() :
        for di_key, value in value.items():
            characteristics[key][di_key] = bytes(value)+"/"+bytes(category_num)

    #print characteristics

    # P(B|A)计算
    category_characteristics = {}
    category_characteristics_total = {}

    for atom_line_key,atom_line_val in enumerate(trainMatrix) :

        c_key = "c:" + bytes(trainCategory[atom_line_key])

        for atom_key,atom_col in enumerate(atom_line_val) :
            d_key = "d:" + bytes(atom_key)
            t_key = "t:" + bytes(atom_col)


            #switch
            if category_characteristics.has_key(d_key) == False :
                category_characteristics[d_key] = {}
                category_characteristics[d_key][t_key] = {}
                category_characteristics[d_key][t_key][c_key] = 1


            elif category_characteristics[d_key].has_key(t_key) == False:

                category_characteristics[d_key][t_key] = {}
                category_characteristics[d_key][t_key][c_key] = 1

            elif category_characteristics[d_key][t_key].has_key(c_key) == False:
                category_characteristics[d_key][t_key][c_key] = 1

            else:
                category_characteristics[d_key][t_key][c_key] += 1


        if category_characteristics_total.has_key(c_key) == False:
            category_characteristics_total[c_key] = 1

        else:
            category_characteristics_total[c_key] += 1

    for atom_line_key,atom_line_val in category_characteristics.items() :
        for atom_key,atom_col in atom_line_val.items() :

            for atom_key_inner, atom_col_inner in atom_col.items():
                category_characteristics[atom_line_key][atom_key][atom_key_inner] = bytes(atom_col_inner)+"/"+bytes(category_characteristics_total[atom_key_inner])


    content = {
        "category" : category,
        "characteristics" : characteristics,
        "category_characteristics" : category_characteristics,
        "total" : len(trainMatrix)
    }

    content = json.dumps(content)
    return content

# 按照训练结果分类
def classifyNB(vec2Classify):
    file_context = open("input/bayes/macan2014_train.txt").read()
    content = json.loads(file_context)

    category = content["category"]
    characteristics = content["characteristics"]
    category_characteristics = content["category_characteristics"]
    total = content["total"]

    probability = {}

    for category_key, category_val in category.items():

        # P(B|A)
        c_key = bytes(category_key)
        probability[c_key] = 1
        for atom_key,atom_col in enumerate(vec2Classify):
            d_key = "d:" + bytes(atom_key)
            t_key = "t:" + bytes(atom_col)

            if category_characteristics.has_key(d_key) and category_characteristics[d_key].has_key(t_key) and category_characteristics[d_key][t_key].has_key(c_key):
                pba_operation = category_characteristics[d_key][t_key][c_key].split("/")
                probability[c_key] *=float(pba_operation[0])/float(pba_operation[1])
            else:
                # 此处算法待评估
                pba_operation = category[c_key].split("/")
                probability[c_key] *= float(pba_operation[0])/float(pba_operation[1])

            # P(B)
            if characteristics[d_key].has_key(t_key):
                pb_operation = characteristics[d_key][t_key].split("/")
                probability[c_key] = probability[c_key] / (float(pb_operation[0]) / float(pb_operation[1]))
            else:
                # 此处算法待评估
                probability[c_key] = probability[c_key] / (1/float(total))
        # P(A)
        pa_operation = category_val.split("/")
        probability[c_key] *= float(pa_operation[0])/float(pa_operation[1])

    sort_probability = sorted(probability.items(),key=lambda item:item[1],reverse=True)
    most_likely = sort_probability[0][0].split(":")
    return most_likely[1]



# 机器训练
trainMatrix, trainCategory = loadDataSet()
content = trainNB0(trainMatrix, trainCategory)
savetrain(content)

# 验证正确率
def dating_class_test():

    testMatrix = file2arrayexpand("input/bayes/macan2014_test_dispersed.txt")
    testCategory = file2array("input/bayes/macan2014_test_cat.txt")

    error_count = 0.0
    for key,line in enumerate(testMatrix):
        cls = classifyNB(line)
        print "the classifier came back with: %s, the real answer is: %s" % (cls, testCategory[key])
        if (cls != testCategory[key]): error_count += 1.0
        #print key,line,cls
    print "the total error rate is: %f" % (error_count/len(testCategory))

dating_class_test()

# cls = classifyNB(['0', '12', '51'])
# print cls


# def loadDataSetV2 ():
#     trainMatrix = [
#                        ['sneezing', 'nurse'],
#                        ['sneezing', 'farmer'],
#                        ['headache', 'workers'],
#                        ['headache', 'workers'],
#                        ['sneezing', 'teachers'],
#                        ['headache', 'teachers']
#                   ]
#
#
#     trainCategory = ['cold', 'allergy', 'concussion', 'cold', 'cold', 'concussion']  # 1 is abusive, 0 not
#     return trainMatrix, trainCategory
#
#
#
# trainMatrix, trainCategory = loadDataSetV2()
# content = trainNB0(trainMatrix, trainCategory)
# savetrain(content)
#
# cl = classifyNB(['sneezing','workers'])
# print cl








