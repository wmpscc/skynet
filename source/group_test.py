# -*- coding: UTF-8 -*-
import fasttext
import jieba
import random

def get_word(file):
    fr = open(file)
    need = []
    tag = " __label__"
    for line in fr.readlines():
        line = line.strip()
        if len(line):
            struct = line.split(tag)
            need.append(struct)
    return need


default_words = get_word('source_test.txt')

classifier = fasttext.load_model('source.bin', label_prefix='__label__')
total = 0
success_num = 0
error_num = 0

default_error_num = 0
default_juj_num = 0
for line in default_words:

    total += 1
    lables = classifier.predict([line[0]])
    tag = line[1]
    if (lables[0][0] == tag):
        success_num += 1
        # print ("success, the real answer is: %s" % (
        #     lables[0][0]))
    else:
        error_num += 1
        if lables[0][0] == 'default':
            default_error_num+=1
        if tag == 'default':
            default_juj_num+=1

        print ("line id is %s,the classifier came back with: %s, the real answer is: %s" % (total,lables[0][0], tag))

print ("\n")
print ("本来是其他判断成default :%d" % (default_error_num))
print ("本来是default判断成其他 :%d" % (default_juj_num))
print ("error num is :%d" % (error_num))
print ("total num is :%d" % (total))
print ("\n")
print ("success rate is:%f" % (success_num / total))



