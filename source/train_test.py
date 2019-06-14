# -*- coding: UTF-8 -*-
import fasttext
import jieba
import random
import math
import os, sys

# 先分词

group = 1
billard = 0.2

def get_line(file):
    fr = open(file)
    need = []
    tag = " __label__"
    for line in fr.readlines():
        line = line.strip()
        if(len(line) >0 ):
            struct = line.split(tag)

            content = " ".join(jieba.lcut(struct[0]))
            need.append(content+tag+struct[1]+"\n")
    random.shuffle(need)
    return need

def write_word():
    lines = get_line("../resources/content/source_origin.txt")
    total = len(lines)
    end = int(total*billard)

    train_lines = lines[end:]
    test_lines = lines[0:end]
    write_line("test", test_lines)
    write_line("train", train_lines)

    print ("write done")

def write_line(type, lines):
    file_name = "source_{:s}.txt".format(type)

    out = open(file_name, 'w')
    for li in lines:
        out.write(li)
    out.close()

def train(n):
    # epoch 训练次数
    classifier = fasttext.supervised("source_train.txt", 'source', label_prefix='__label__', epoch = 50)

    result = classifier.test("source_test.txt")
    print ("group num is %s, and rate is:%f\n" % (n, result.precision))

    return result.precision

def logic():
    rate_t = 0
    fornum = 100

    for s in range(fornum):
        write_word()
        rate = train(s)
        rate_t += rate

    print ("avg rate is:%f" % (rate_t / fornum))

logic()









