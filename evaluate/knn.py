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

def classifyNB(vec2Classify):
    dating_data_mat_linear = file2matrixnumber("input/knn/macan2014_linear.txt", 5)
    norm_mat_linear = z_score_norm(dating_data_mat_linear)

    dating_data_mat_dispersed = file2matrixstr('input/knn/macan2014_dispersed.txt')
    norm_mat_dispersed = one_hot_norm(dating_data_mat_dispersed)

    testMatrix = np.hstack((norm_mat_linear, norm_mat_dispersed))
    testCategory = file2array('input/knn/macan2014_cat.txt')


    knn_classifier = KNeighborsClassifier()
    knn_classifier.fit(testMatrix,testCategory)

    predicted = knn_classifier.predict(vec2Classify)
    return predicted[0]


def dating_class_test():
    dating_data_mat_linear = file2matrixnumber("input/knn/macan2014_linear.txt", 5)
    norm_mat_linear = z_score_norm(dating_data_mat_linear)

    dating_data_mat_dispersed = file2matrixstr('input/knn/macan2014_dispersed.txt')
    norm_mat_dispersed = one_hot_norm(dating_data_mat_dispersed)

    testCategory = file2array('input/knn/macan2014_cat.txt')
    testMatrix = np.hstack((norm_mat_linear, norm_mat_dispersed))



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



