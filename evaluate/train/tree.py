from sklearn import tree
import numpy as np
import os



root_dir = os.path.abspath(os.path.join(os.getcwd(), "../"))

def file2arrayexpand(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(list(map(float, line.split(' '))))
    return class_label_vector

def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(int(line))
    return class_label_vector

def classifyNB(vec2Classify, n_name):
    trainMatrix = file2arrayexpand(root_dir+"/input/tree/"+(n_name)+"/macan2014_train_dispersed.txt")
    trainCategory = file2array(root_dir+"/input/tree/"+(n_name)+"/macan2014_train_cat.txt")

    model = tree.DecisionTreeClassifier()
    model.fit(trainMatrix, trainCategory)

    predicted = model.predict(vec2Classify)
    return predicted[0]

def dating_class_test(n_name):

    testMatrix = file2arrayexpand(root_dir+"/input/tree/"+(n_name)+"/macan2014_test_dispersed.txt")
    testCategory = file2array(root_dir+"/input/tree/"+(n_name)+"/macan2014_test_cat.txt")


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