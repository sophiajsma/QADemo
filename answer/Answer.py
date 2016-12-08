# coding=utf-8


class Answer(object):
    def __init__(self, str_answer):
        self._str_answer = str_answer   # 答案字符串
        self._score = 0.0                          # 分数

    @property
    def str_answer(self):
        return self._str_answer

    @str_answer.setter
    def str_answer(self, value):
        self._str_answer = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value