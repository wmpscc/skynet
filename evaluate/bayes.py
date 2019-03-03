from sklearn.naive_bayes import GaussianNB
import numpy as np

def file2arrayexpand(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(list(map(int, line.split(' '))))
    return class_label_vector

def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(int(line))
    return class_label_vector

def classifyNB(vec2Classify):
    trainMatrix = file2arrayexpand("input/bayes/macan2014_train_dispersed.txt")

    trainCategory = file2array("input/bayes/macan2014_train_cat.txt")

    model = GaussianNB()

    model.fit(trainMatrix, trainCategory)
    predicted = model.predict(vec2Classify)
    return predicted[0]

def dating_class_test():

    testMatrix = file2arrayexpand("input/bayes/macan2014_test_dispersed.txt")
    testCategory = file2array("input/bayes/macan2014_test_cat.txt")

    error_count = 0.0
    for key,line in enumerate(testMatrix):
        cls = classifyNB([line])
        actual = testCategory[key]

        notice = ""
        if (cls != actual):
            error_count += 1.0
            notice = "fail"

        print "the classifier came back with: %s, the real answer is: %s %s" % (cls, actual, notice)

        #print key,line,cls
    print "the total error rate is: %f" % (error_count/len(testCategory))
    print "right num is: %f" % int((len(testCategory)-error_count))
    print "error num is: %f" % int(error_count)

dating_class_test()

#s = classifyNB([[0,5,3,0,0,2016,0]])
# s = classifyNB([[0,5,3,0,0,2016,0]])
# print s


