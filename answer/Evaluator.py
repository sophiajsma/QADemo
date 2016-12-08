# coding=utf-8

import Answer
import Evidence
from question import Question
from util import Tool
import re
import math

'''
    打分器
    给evidence和answer根据问题打分
    可以实现多种打分函数，甚至混合加权
'''

class Evaluator(object):
    def __init__(self):
        self._evidences_idf = {}  # 逆文档频率，针对一个evidence列表

    @property
    def evidences_idf(self):
        return self._evidences_idf

    @evidences_idf.setter
    def evidences_idf(self, dic):
        self._evidences_idf = dic

    '''
        根据问题给证据打分

        @param evidence: Evidence类型，被打分的证据
        @param question: Quesiton类型
        return: 打分后的evidence
    '''
    def evalue_evidence(self, evidence, question):
        # now all weights are 1
        return self.evalue_evidence_idf(evidence, question) + self.evalue_evidence_bigram(evidence, question) + self.evalue_evidence_skipgram(evidence, question)

    '''
        证据打分函数1： 根据词频
        在 title 中出现，计 2/idf 分
        在 snippet 中出现，计 1/idf 分
    '''
    def evalue_evidence_idf(self, evidence, question):
        score = 0.0
        key_title = Tool.eliminate_stop_words(evidence.lst_title_word)
        key_snippt = Tool.eliminate_stop_words(evidence.lst_snippt_word)
        for word in question.lst_keywords:
            if word in key_title:
                score += 2/self.evidences_idf[word]
            if word in key_snippt:
                score += 1/self.evidences_idf[word]
        return score

    '''
        在evidence中用question的所有bigram正则匹配
        匹配一个2分
    '''
    def evalue_evidence_bigram(self, evidence, question):
        length = len(question.lst_question)
        # collect patterns
        patterns = []
        for i in range(length-1):
            pattern = question.lst_question[i] + question.lst_question[i+1]
            patterns.append(pattern)
        # to match
        text = evidence.str_title + evidence.str_snippt
        score = 0.0
        for pattern in patterns:
            num = len(re.findall(pattern, text))
            score += num*2
        return score

    '''
        在evidence中用question所有skipbigram正则匹配
        匹配一个2分
    '''
    def evalue_evidence_skipgram(self, evidence, question):
        length = len(question.lst_question)
        # collect patterns
        patterns = []
        for i in range(length-2):
            pattern = question.lst_question[i] + '.' + question.lst_question[i+2]
            patterns.append(pattern)
        # to match
        text = evidence.str_title + evidence.str_snippt
        score = 0.0
        for pattern in patterns:
            num = len(re.findall(pattern, text))
            score += num*2
        return score

    '''
        根据问题和证据给答案打分

        @param answers: a list Answer类型，被打分的答案集
        @param evidence: Evidence类型
        @param question: Question类型
        return: 打分后的answer
    '''
    def evalue_answers(self, answers, evidence, question):
        # all weights are 1
        self.evalue_answers_frequency(answers, evidence, question)
        self.evalue_answers_distance(answers, evidence, question)
        self.evalue_answers_alignment(answers, evidence, question)
        self.evalue_answers_more_alignment(answers, evidence, question)
        self.evalue_answers_rewind_alignment(answers, evidence, question)
        self.evalue_answers_hot_candidate(answers, evidence, question)
        return answers

    '''
        根据词频打分
        title中出现算2分
        snippet中出现算1分
    '''
    def evalue_answers_frequency(self, answers, evidence, question):
        tf = Tool.get_tf(evidence, question.get_pos())
        for answer in answers:
            if answer not in tf:
                print '词频答案打分，未找到答案词。。。'
                continue
            else:
                answer.score += tf[answer]
        return

    '''
        根据 candidate answer 和 question term 的词距打分
        score = 原分值 * （1/词距）
    '''
    def evalue_answers_distance(self, answers, evidence, question):
        # question key words
        question_keywords = question.lst_keywords
        # evidence words
        evidence_words = evidence.lst_title_word + evidence.lst_snippt_word

        for answer in answers:
            distance = 0.0
            # calculate the distribution of answer
            answer_offsets = []
            for i in range(len(evidence_words)):
                if evidence_words[i] == answer.str_answer:
                    answer_offsets.append(i)
            for question_keyword in question_keywords:
                # calculate the distribution of question
                question_offsets = []
                for i in range(len(evidence_words)):
                    if evidence_words[i] == question_keyword:
                        question_offsets.append(i)
                # calculate distance
                for answer_offset in answer_offsets:
                    for question_offset in question_offsets:
                        distance += abs(answer_offset - question_offset)

            answer.score += answer.score / distance

    '''
        文本对齐评分
        将每一个候选答案放到问题的每一个位置，再在每个词之间插入.{0,5}做模糊匹配，在证据中查找是否有匹配的文本
        算得平均匹配长度
        score = 问题长度 / 平均匹配长度
    '''
    def evalue_answers_alignment(self, answers, evidence, question):
        # question words
        question_words = question.lst_question
        # evidence string
        evidence_text = evidence.str_title + evidence.str_snippt
        # for every answer
        for answer in answers:
            # position i to substitute
            for i in range(question_words):
                textual_alignment = ""
                for j in range(question_words):
                    if i == j:
                        textual_alignment += answer.str_answer
                    else:
                        textual_alignment += question_words[j]

                # if alignment equals the question itself, continue to the next alignment
                if textual_alignment == question.str_question:
                    continue

                # generate  pattern
                alignment_term, _ = Tool.parse_sentence_separate(textual_alignment)
                pattern = ""
                alignment_length = len(alignment_term)
                for t in range(alignment_length):
                    pattern += alignment_term[t]
                    if t < alignment_length-1:
                        pattern += ".{0,5}"

                match = re.findall(pattern, evidence_text)
                count = len(match)
                length = sum(list(map(len, match)))
                if count > 0:
                    average_length = length / count
                    question_length = len(question_words)
                    answer.score += question_length / average_length

    '''
        宽松文本对齐评分
        忽略问题中长度为1的词
        其余和文本对齐评分无异
    '''
    def evalue_answers_more_alignment(self, answers, evidence, question):
        # question words
        question_words = []
        for word in question_words:
            if len(word) > 1:
                question_words.append(word)
        # evidence string
        evidence_text = evidence.str_title + evidence.str_snippt
        # for every answer
        for answer in answers:
            # position i to substitute
            for i in range(len(question_words)):
                textual_alignment = ""
                for j in range(len(question_words)):
                    if i == j:
                        textual_alignment += answer.str_answer
                    else:
                        textual_alignment += question_words[j]

                # if alignment equals the question itself, continue to the next alignment
                if textual_alignment == question.str_question:
                    continue

                # generate  pattern
                alignment_term, _ = Tool.parse_sentence_separate(textual_alignment)
                pattern = ""
                alignment_length = len(alignment_term)
                for t in range(alignment_length):
                    pattern += alignment_term[t]
                    if t < alignment_length-1:
                        pattern += ".{0,5}"

                match = re.findall(pattern, evidence_text)
                count = len(match)
                length = sum(list(map(len, match)))
                if count > 0:
                    average_length = length / count
                    question_length = len(question_words)
                    answer.score += question_length / average_length

    '''
        回带文本对齐评分
        答案到问题中替换词，然后回到google搜索得证据
    '''
    def evalue_answers_rewind_alignment(self, answers, evidence, question):
        pass

    '''
        热词评分【热词长度要大于1】
        先找出问题中词频最高得词
        然后找出离这个词最近得候选答案
        候选答案分值翻倍
    '''
    def evalue_answers_hot_candidate(self, answers, evidence, question):
        best_candidate_answer = None
        min_distance = 9999999

        evidence_words = evidence.lst_title + evidence.lst_snippt
        hot = question.get_hot()

        # find hot word's position
        hot_offsets = []
        for i in range(len(evidence_words)):
            if evidence_words[i] == hot:
                hot_offsets.append(i)
        # for every answer
        for answer in answers:
            # find answer's position
            answer_offsets = []
            for i in range(len(evidence_words)):
                if answer.str_answer == evidence_words[i]:
                    answer_offsets.append(i)
            # calculate the min distance of hot word and the answer
            for answer_offset in answer_offsets:
                for hot_offset in hot_offsets:
                    distance = abs(answer_offset - hot_offset)
                    if min_distance > distance:
                        min_distance = distance
                        best_candidate_answer = answer

        if best_candidate_answer and min_distance > 0:
            best_candidate_answer.score += best_candidate_answer.score


    '''
        对答案列表排序，评分最高即最可能的答案放在最前面
        @param: a list of Answer
        return: a list of sorted Answer
    '''
    def rank_answers(self, answers):
        return answers