#coding=utf-8

# 问题的类别，分为7类：人名、地名、机构名、数字、时间、定义、对象、未知
question_type = ['PERSON', 'LOCATION', 'ORGANIZATION', 'NUMBER', 'TIME', 'DEFINITION', 'OBJECT', 'UNKNOWN']

'''
    问题
'''
class Question(object):
    def __init__(self, str):
        self._str_question = str              # 问题字符串
        self._str_type = 'UNKNOWN'      # 问题类型
        self._lst_question = []                # 分词后列表形式
        self._lst_keywords = []              # 关键词提取
        self._evidences = []                   # 对应证据列表

    @property
    def str_type(self):
        return self._str_type

    @str_type.setter
    def str_type(self, value):
        self._str_type = value

    @property
    def str_question(self):
        return self._str_question

    @property
    def lst_question(self):
        return self._lst_question

    @property
    def lst_keywords(self):
        return self._lst_keywords

    @property
    def evidences(self):
        return self._evidences

    @evidences.setter
    def evidences(self, value):
        self._evidences = value




    # 根据问题类型得出答案可能的pos类型【前缀】，注意【前缀】
    def get_pos(self):
        pos = "unknown"
        type = self.str_type
        if     type == 'PERSON':             pos = "nr"
        elif  type == 'LOCATION':          pos = "ns"
        elif  type == 'ORGANIZATION':  pos = "nt"
        elif  type == 'NUMBER':             pos = "m"
        elif  type == 'TIME':                   pos = "t"
        elif  type == 'DEFINITION':        pos = ""
        elif  type == 'OBJECT':               pos = ""

    # 提取关键词，存在self._lst_keywords中,顺便分词后词存在lst_question中
    def extract_keywords(self):
        return self

    # 对应evidences提取热词,长度大于1
    def get_hot(self):
        evidences_words = []
        for evidence in self.evidences:
            evidences_words += evidence.lst_title_word + evidence.lst_snippt_word
        tf = {}
        for word in evidences_words:
            if len(word) < 2:
                continue
            if word not in tf:
                tf[word] = 1
            else:
                tf[word] += 1
        # tf empty
        if not tf:
            return None

        sorted_tf = sorted(tf.items(), key=lambda item:item[1], reverse=True)
        return sorted_tf[0][0]


