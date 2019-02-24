# -*- coding: UTF-8 -*-
'''
Created on Sep 16, 2010
kNN: k Nearest Neighbors

Input:      in_x: vector to compare to existing dataset (1xN)
            dataSet: size m data set of known vectors (NxM)
            labels: data set labels (1xM vector)
            k: number of neighbors to use for comparison (should be an odd number)

Output:     the most popular class label

@author: pbharrin
'''
import numpy as np
import operator
from sklearn import preprocessing

# knn
def classify(in_x, data_set, labels, k):
    data_set_size = data_set.shape[0]
    diff_mat = np.tile(in_x, (data_set_size,1)) - data_set
    sq_diff_mat = diff_mat**2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5
    sorted_distIndicies = distances.argsort()
    class_count={}
    for i in range(k):
        voteIlabel = labels[sorted_distIndicies[i]]
        class_count[voteIlabel] = class_count.get(voteIlabel,0) + 1
    sortedclass_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedclass_count[0][0]

# read from file

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

def file2matrixstr(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        list_from_line = line.split(' ')
        class_label_vector.append(list_from_line)
    return np.array(class_label_vector)

def file2array(filename):
    fr = open(filename)
    class_label_vector = []

    for line in fr.readlines():
        line = line.strip()
        class_label_vector.append(line)

    return class_label_vector

# min-max
def min_max_norm(data_set):
    min_vals = data_set.min(0)
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals
    norm_data_set = np.zeros(np.shape(data_set))
    m = dataSet.shape[0]
    norm_data_set = data_set - np.tile(min_vals, (m,1))
    norm_data_set = norm_data_set/np.tile(ranges, (m,1))   #element wise divide
    return norm_data_set

# z-score
def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

# one-hot
def one_hot_norm(data_set):
    enc = preprocessing.OneHotEncoder()
    enc.fit(data_set)
    return enc.transform(data_set).toarray()

def dating_class_test():
    ho_ratio = 0.1      #verify 10%

    dating_data_mat_linear = file2matrixnumber("input/macan2014_linear.txt", 5)
    norm_mat_linear = z_score_norm(dating_data_mat_linear)


    dating_data_mat_dispersed = file2matrixstr('input/macan2014_dispersed.txt')
    norm_mat_dispersed = one_hot_norm(dating_data_mat_dispersed)


    dating_labels = file2array('input/macan2014_cat.txt')
    dating_data_mat = np.hstack((norm_mat_linear, norm_mat_dispersed))


    m = dating_data_mat.shape[0]
    num_test_vecs = int(m*ho_ratio)
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classify(dating_data_mat[i,:],dating_data_mat[num_test_vecs:m,:],dating_labels[num_test_vecs:m],5)
        print "the classifier came back with: %s, the real answer is: %s" % (classifier_result, dating_labels[i])
        if (classifier_result != dating_labels[i]): error_count += 1.0
    print "the total error rate is: %f" % (error_count/float(num_test_vecs))
    print error_count


dating_class_test()