from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import operator
from sklearn import preprocessing

def file2matrixnumber(filename, colnum):
    fr = open(filename)
    number_oflines = len(fr.readlines())
    return_mat = np.zeros((number_oflines, colnum))
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split(' ')
        return_mat[index, :] = list_from_line[0:colnum]
        index += 1
    return return_mat

def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

def file2matrixstr(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split(' ')
        class_label_vector.append(list_from_line)
    return np.array(class_label_vector)

def one_hot_norm(data_set):
    enc = preprocessing.OneHotEncoder()
    enc.fit(data_set)
    return enc.transform(data_set).toarray()

def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(int(line))

    return class_label_vector

def classifyNB(vec2Classify, n_name):

    dating_data_mat_linear = file2matrixnumber("input/knn/"+bytes(n_name)+"/macan2014_train_dispersed.txt", 3)
    norm_mat_linear = z_score_norm(dating_data_mat_linear)
    norm_mat_linear = norm_mat_linear.tolist()

    testCategory = file2array("input/knn/"+bytes(n_name)+"/macan2014_train_cat.txt")


    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(norm_mat_linear,testCategory)

    predicted = knn_classifier.predict(vec2Classify)
    return predicted[0]


def dating_class_test(n_name):
    dating_data_mat_linear = file2matrixnumber("input/knn/"+bytes(n_name)+"/macan2014_test_dispersed.txt", 3)
    norm_mat_linear = z_score_norm(dating_data_mat_linear)
    testMatrix = norm_mat_linear.tolist()

    testCategory = file2array("input/knn/"+bytes(n_name)+"/macan2014_test_cat.txt")


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
        if cha >= 5 or cha <= -5 :
            too_many = "many"

        print "the classifier came back with: %s, the real answer is: %s %s %s" % (cls, actual, notice, too_many)

        #print key,line,cls
    rate = right_count/len(testCategory)
    print "the total right rate is: %f" % (rate)
    print "error num is: %f" % int((len(testCategory)-right_count))
    print "right num is: %f" % int(right_count)

    return rate

def dating_class_test_all():

    total = 0
    for n_name in range(10):
        total += dating_class_test(n_name)

    print "\n"

    print "avg rate is: %f" % (total/10)

dating_class_test_all()



