# -*- coding: UTF-8 -*-
import math
import numpy as np
from sklearn import preprocessing

def getModelByGroup(group, type, trainModel, ids, groupNum, testPercentage):
    group = int(group)
    feature = trainModel['feature']
    classificate = trainModel['classificate']

    length = len(feature)

    # 每个组总容量
    capacityNum = int(math.ceil(length/groupNum))

    if group+1 > groupNum:
        group = groupNum-1

    # 每个组数据集
    if group == groupNum-1 :
        start = group*capacityNum
        needFeature = feature[start:]
        needClassificate = classificate[start:]
        needIds = ids[start:]
    else:
        start = group * capacityNum
        end = (group+1) * capacityNum
        needFeature = feature[start:end]
        needClassificate = classificate[start:end]
        needIds = ids[start:end]

    # 训练、测试数据集划分
    testEnd = int(math.ceil(capacityNum * testPercentage))
    # 训练数据
    if type == 'dispersed':
        resultFeature = needFeature[testEnd:]
        resultClassificate = needClassificate[testEnd:]
        resultIds = needIds[testEnd:]
    else:
        resultFeature = needFeature[:testEnd]
        resultClassificate = needClassificate[:testEnd]
        resultIds = needIds[:testEnd]

    return resultFeature, resultClassificate, resultIds

# z-score归一化
def z_score_norm(data_set):
    return preprocessing.MinMaxScaler().fit_transform(data_set)

def coverFloat(master):
    master_float = []
    for i in master:
        i = float(i)
        master_float.append(i)
    return master_float

def similarSort(master, origin):
    #转化

    master = coverFloat(master)

    list = origin
    list.append(master)
    list = np.array(list)
    list = z_score_norm(list)

    #归一化取出
    total = list.shape[0]
    master = list[total-1]
    list = np.delete(list, total-1, 0)

    #列表长度
    list_size = list.shape[0]

    diff_mat = np.tile(master, (list_size, 1)) - list
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sorted_distIndicies = distances.argsort()

    # result_list = []
    # for i in range(list_size):
    #     result_list.append(origin[sorted_distIndicies[i]])

    return sorted_distIndicies.tolist()

def get_conf():
    # 分组个数
    groupNum = 6
    # 每个组测试集占比
    testPercentage = 0.2

    # 模型id
    modelId = "017adc861c20b360bddb4dce92d9608a"

    isAdd = True
    #isAdd = False

    return modelId, groupNum, testPercentage, isAdd