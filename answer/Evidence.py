# coding=utf-8

import Answer

class Evidence(object):
    def __init__(self):
        self._str_title = ""                 # 标题字符串
        self._str_snippt = ""             # 段落字符串
        self._lst_title = []                  # 标题， 列表形式 (词，词性)
        self._lst_snippt = []              # 段落，列表形式  （词， 词性）
        self._lst_title_word = []        # 标题，列表形式 词
        self._lst_snippt_word = []    # 段落， 列表形式 词性
        self._lst_title_tag = []          # 标题，列表形式 词性
        self._lst_snippt_tag = []      # 段落，列表形式 词性
        self._score = 0                    # 评分

    @property
    def str_title(self):
        return self._str_title

    @str_title.setter
    def str_title(self, value):
        self._str_title = value

    @property
    def str_snippt(self):
        return self._str_snippt

    @str_snippt.setter
    def str_snippt(self, value):
        self._str_snippt = value

    @property
    def lst_title(self):
        return self._lst_title

    @lst_title.setter
    def lst_title(self, value):
        self._lst_title = value

    @property
    def lst_snippt(self):
        return self._lst_snippt

    @lst_snippt.setter
    def lst_snippt(self, value):
        self._lst_snippt = value

    @property
    def lst_title_word(self):
        return self._lst_title_word

    @lst_title_word.setter
    def lst_title_word(self, value):
        self._lst_title_word = value

    @property
    def lst_snippt_word(self):
        return self._lst_snippt_word

    @lst_snippt_word.setter
    def lst_snippt_word(self, value):
        self._lst_snippt_word = value

    @property
    def lst_title_tag(self):
        return self._lst_title_tag

    @lst_title_tag.setter
    def lst_title_tag(self, value):
        self._lst_title_tag = value

    @property
    def lst_snippt_tag(self):
        return self._lst_snippt_tag

    @lst_snippt_tag.setter
    def lst_snippt_tag(self, value):
        self._lst_snippt_tag = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value


    '''
        在支撑证据（段落）中根据pos提取答案

        @param pos: string, pos（词性）
        return: a list of Answer
    '''
    def extract_answers(self, pos):
        candidate_answers = []
        words = self.lst_title + self.lst_snippt
        for word in words:
            # 长度小于2的词直接忽略
            if len(word[0]) < 2:
                continue
            if word[1].startwith(pos):
                candidate_answers.add(Answer.Answer(word[0]))

        return candidate_answers