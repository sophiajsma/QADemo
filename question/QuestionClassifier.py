# coding=utf-8

# 问题的类别，分为7类：人名、地名、机构名、数字、时间、定义、对象、未知
question_type = ['PERSON', 'LOCATION', 'ORGANIZATION', 'NUMBER', 'TIME', 'DEFINITION', 'OBJECT', 'UNKNOWN']

'''
    问题分类器
'''
class QuestionClassifier(object):
    def __init__(self):
        pass

    '''
        问句分类

        @param question: Question类型
        return: Question 类型
    '''
    def classify(self, question):
        question.str_type = 'PERSON'
        return question




def main():
    pass

if __name__ == '__main__':
    main()
