# -*- coding: UTF-8 -*-
import sys
import fasttext
import jieba
import random
import math

sys.path.append('..')

from model.source import DbSource

# resources/content/source_origin.txt 打好标签的最原始数据（从db读入的）
# resources/content/source.txt 已分词完毕的数据

# resources/content/source_origin_verify.txt 打好标签的最原始!!验证集!!数据（从db读入的）
# resources/content/source_verify.txt 用于验证训练完毕的模型的!!验证集!!数据

# 写入训练的原始数据（待分词）
def filterKeyword(line):

    text = (line.title + line.content).strip()
    text = text.replace("\n", "").replace("\r", "")

    words = ['macan', '玛卡', 'mancn', 'macans', 'macangts', 'macanturbo', '迈凯', 'cayman', '718', 'boxster', '盒子',
             'Panamera', '卡宴', '卡曼', '博克斯特', '曼卡', 'glc', 'mancan', '987.2', '911']
    if (len(text) > 0):
        text = text.lower()

        # for word in words:
        #     text = text.replace(word, "苹果")

        return text

    return ''

def writeTrainTxt():
    db = DbSource()
    id = 0
    out = open("../resources/content/source_origin.txt", 'w')

    train_num = 0
    sell_success = 0
    buy_success = 0
    default_success = 0

    while(True):
        lines = db.getDetermineForeachList(id, 9)
        if (len(lines) > 0) :
            for line in lines:
                id = line.id
                text = filterKeyword(line)
                if (len(text) > 0):
                    if (line.intention == 2):
                        # 普通帖子
                        out.write(text+" __label__default\n")

                        train_num+=1
                        default_success+=1
                    elif (line.intention == 5):
                        # 购买意向帖子
                        out.write(text + " __label__buy\n")

                        train_num += 1
                        buy_success+=1
                    elif (line.intention == 9):
                        # 出售意向帖子
                        out.write(text + " __label__sell\n")

                        train_num += 1
                        sell_success+=1
        else:
            break
    out.close()

    # 训练
    print ("total:%d" % train_num)
    print ("sell:%d" % sell_success)
    print ("buy:%d" % buy_success)
    print ("default:%d" % default_success)

def writeVerifyTxt():
    db = DbSource()
    id = 0
    out = open("../resources/content/source_origin_verify.txt", 'w')

    new_success = 0

    while (True):
        lines = db.getDetermineForeachList(id, 0)
        if (len(lines) > 0):
            for line in lines:
                id = line.id
                text = filterKeyword(line)
                if (len(text) > 0):

                    out.write(text + " __label__default\n")
                    new_success += 1
        else:
            break
    out.close()

    # 验证
    print ("total:%d" % new_success)


# 训练模型
def trainModel():
    # 写入训练原始数据
    writeTrainTxt()

    lines = _get_line("../resources/content/source_origin.txt")

    source_file = "../resources/content/source.txt"
    out = open(source_file, 'w')
    for li in lines:
        out.write(li)

    classifier = fasttext.supervised(source_file, '../resources/model/source_online', label_prefix='__label__', epoch=100)
    result = classifier.test(source_file)
    print ("\n")
    print ('P@1:', result.precision)
    print ('R@1:', result.recall)
    print ('Number of examples:', result.nexamples)

# 验证集
def verifyModel():
    # 写入训练原始数据
    writeVerifyTxt()

    lines = _get_line("../resources/content/source_origin_verify.txt")

    source_file = "../resources/content/source_verify.txt"
    out = open(source_file, 'w')
    for li in lines:
        out.write(li)

    classifier = fasttext.load_model('../resources/model/source_online.bin', label_prefix='__label__')


    result = classifier.test(source_file)
    print ("\n")
    print ('P@1:', result.precision)
    print ('R@1:', result.recall)
    print ('Number of examples:', result.nexamples)

def _get_line(file):
    fr = open(file)
    need = []
    tag = " __label__"
    for line in fr.readlines():
        line = line.strip()
        if(len(line) >0 ):
            struct = line.split(tag)
            if(len(struct) == 2):
                content = " ".join(jieba.lcut(struct[0]))
                need.append(content+tag+struct[1]+"\n")
    random.shuffle(need)
    return need

# 分类新入帖子
def scanBelong():
    db = DbSource()

    id = 0

    num = 0
    sell_success = 0
    buy_success = 0
    default_success = 0

    while (True):
        list = trainModel = db.getWaitDetermineForeachList(id, 0, 0)
        if (len(list) > 0):
            for one in list:
                id = one.id
                num += 1
                print ("each:%s" % (id))
                text = filterKeyword(one)
                if(len(text) == 0):
                    db.suspectedDel(id)
                    continue

                action = _get_action(text)
                if (action == 'sell'):
                    sell_success += 1
                    db.suspectedSell(id)
                    print ("sell:%s" % (id))

                elif (action == 'buy'):
                    buy_success += 1
                    db.suspectedBuy(id)
                    print ("buy:%s" % (id))

                elif (action == 'default'):
                    default_success += 1
                    db.suspectedDefault(id)
                    print ("default:%s" % (id))
        else:
            break

    print ("total:%s" % num)
    print ("sell:%d" % sell_success)
    print ("buy:%d" % buy_success)
    print ("default:%d" % default_success)

def _get_action(input):
    classifier = fasttext.load_model('../resources/model/source_online.bin', label_prefix='__label__')
    words = " ".join(jieba.lcut(input))
    texts = [words]
    lables = classifier.predict(texts)
    #print (lables)
    return lables[0][0]