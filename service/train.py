# -*- coding: UTF-8 -*-
import math
def getModelByGroup(group, type, trainModel, groupNum, testPercentage):
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
    else:
        start = group * capacityNum
        end = (group+1) * capacityNum
        needFeature = feature[start:end]
        needClassificate = classificate[start:end]

    # 训练、测试数据集划分
    testEnd = int(math.ceil(capacityNum * testPercentage))
    # 训练数据
    if type == 'dispersed':
        resultFeature = needFeature[testEnd:]
        resultClassificate = needClassificate[testEnd:]
    else:
        resultFeature = needFeature[:testEnd]
        resultClassificate = needClassificate[:testEnd]

    return resultFeature, resultClassificate