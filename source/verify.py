# -*- coding: UTF-8 -*-
import fasttext
import jieba
import random

# 载入模型
classifier = fasttext.load_model('../resources/model/source_online.bin', label_prefix='__label__')



# 出售
# input = '19款帕纳梅拉本人经常长途出差。因心宽体胖不太适合。喜欢的私信吧自己开确实操控很好。指哪打哪山东老乡有木有音响确实不错'
#input = '想出 Macan s 请教一下大概的价格。谢谢各位老师,14年11月。65000km。选bose，19寸，行李架，木纹饰板。北京。不知道要出的话大概多少钱合适。感谢。'
#input = '11年Boxster转让爱车转让一直4s店保养很爱惜白车身蓝色贴膜'
#input = '已售，删帖出个人卡曼2.7  13年10月4万无事故，原车漆，保养记录全，关注，私信'

# 求购
#input = '坐标广东省内或周边求购Macan看配置和车况给价要个人车合理价的'
#input = '全国收macan二手求macan，火山灰?红内，懂行，事故泡水车勿扰'
#input = '个人求2014 16款不是4S店保养的不要，诚心出的直接私聊联系方式谈！江西赣州附近地区联系。'
#input = '广佛地区有出18S的轮毂轮胎吗如题想收一套，有改装鸟巢要出的朋友联系我'

#普通
#input = 'Macan什么时候换代？换代后是用新Q5的底盘吗应该还有汽油版吧？'
#input = '山东，济南！！价格求指教小弟想请教一下山东济南20t的macan能优惠多少，比如说是选配完63w，能优惠多少钱！！请懂得大神指教一下，老婆着急买，自己也不太懂，请大神指教一下'

input = '19年一月新提牧马人沙哈拉2.0出，带无钥匙和远程启动。'

# 测试文本
words = " ".join(jieba.lcut(input))
texts = [words]
lables=classifier.predict(texts)
print(lables)

labels = classifier.predict_proba(texts, k=3)
print (labels)



