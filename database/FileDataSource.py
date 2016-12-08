# coding=utf-8

from answer import Evidence
from question import Question

'''
    与本地的数据库建立链接
    数据文件是老师给的6G文件
'''

class FileDataSource(object):
    def __init__(self):
        pass

    '''
        给定问题，返回支持的证据（段落）

        @param question: Question类型
        return: a list of Evidence
    '''
    def get_evidence(self, question):
        return [Evidence.Evidence()]