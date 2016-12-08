# coding=utf-8

from answer import Evidence
from question import Question

'''
    与谷歌搜索建立链接
'''

class GoogleDataSource(object):
    def __init__(self):
        pass

    '''
        给定问题，返回支持的证据（段落）

        @param question: Question类型
        return: a list of Evidence
    '''
    def get_evidence(self, question):
        return [Evidence.Evidence()]