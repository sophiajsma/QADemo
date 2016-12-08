# coding=utf-8

import math
import jieba.posseg as pseg

'''
    该文件定义一些工具函数
    比较杂
'''

################################################
#                                                                                                                   #
#                                    初始化一些工具                                                          #
#                                                                                                                   #
################################################
# 从文件中读取列表
def read_list(path):
    with open(path) as f:
        return [line.decode('utf8').strip() for line in f]

# 停用词表
stop_words = read_list('./datas/stop_words')



################################################
#                                                                                                                   #
#                                    分隔线                                                                      #
#                                                                                                                   #
################################################

# 消除问句最后的问号（如果有的话）
def eliminate_question_mark(str):
    return str.decode('utf8').strip().replace("?","").replace("？".decode('utf8'),"")

# 消除列表中的停用词
# @param lst: list类型
# return: 除去停用词之后的列表
def eliminate_stop_words(lst):
    ret_lst = []
    for word in lst:
        if word not in stop_words:
            ret_lst.append(word)
    return ret_lst

# 分词和标注，用的是结巴分词
# 返回的是 (word词, tag词性)元组的列表
def parse_sentence(str):
    return pseg.cut(str)

# 分词，分别返回word列表和tag列表
def parse_sentence_separate(str):
    items = pseg.cut(str)
    words = [item[0] for item in items]
    tags = [item[1] for item in items]
    return words, tags

# 计算证据集合所有词的逆文档频率
# @param evidences: a  list of Evidence
# return : a dict {word: idf}
def get_idf(evidences):
    idf = {}
    for evidence in evidences:
        # set word list
        words_title = parse_sentence(evidence.str_title)
        words_snippt = parse_sentence(evidence.str_snippt)
        evidence.lst_title = words_title
        evidence.lst_snippt = words_snippt
        evidence.lst_title_word = [item[0] for item in words_title]
        evidence.lst_title_tag = [item[1] for item in words_title]
        evidence.lst_snippt_word = [item[0] for item in words_snippt]
        evidence.lst_snippt_tag = [item[1] for item in words_snippt]

         # count how many evidences does a word appear in
        words = evidence.lst_title_word + evidence.lst_snippt_word
        s = set(words)
        for word in s:
            if word not in idf:
                idf[word] = 1.0
            else:
                idf[word] += 1

        num_evidences = len(evidences)
        for k,v in idf.items():
            idf[k] = math.log(num_evidences/v, 10)

    return idf

# 计算词频，在可能的目标词中出现的次数（加权，title中算2次）
# @param evidence: Evidence类型
# @param pos: 问题对应的可能的答案词性【前缀】
# return: a dict {word : count}
def get_tf(evidence, pos):
    tf = {}
    title_names = []
    snippt_names = []
    # title
    for word in evidence.lst_title:
        if word[1].startwith(pos):
            title_names.append(word[0])
    # snippt
    for word in evidence.lst_snippt:
        if word[1].startwith(pos):
            snippt_names.append(word[0])
    # count
    for name in title_names:
        if name not in tf:
            tf[name] = 2
        else:
            tf[name] += 2
    for name in snippt_names:
        if name not in tf:
            tf[name] = 1
        else:
            tf[name] += 1

    return tf



def main():
    print eliminate_stop_words(['?', 'asd', ')'])
    str = '北京大学的地址在北京的什么地方？'
    print eliminate_question_mark(str)
    words = pseg.cut(str)
    for word, flag in words:
        print word, ' ', flag

if __name__ == '__main__':
    main()