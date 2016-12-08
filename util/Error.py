# coding=utf-8

import os

'''
    该文件定义一些错误处理程序
'''

# 控制台打印错误原因并直接退出
def error_exit(str_reason):
    print str_reason.decode('utf8')
    os._exit(1)

# 控制台打印错误原因并忽略
def error_ignore(str_reason):
    print str_reason.decode('utf8')
