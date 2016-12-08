# coding=utf-8

from optparse import OptionParser

from question import Question
from question import QuestionClassifier
from database import FileDataSource
from database import BaiduDataSource
from database import GoogleDataSource
from answer import Answer
from answer import Evidence
from answer import Evaluator
from util import Tool
from util import Error

'''
    问答系统框架
    其中定义了：
        ① 问题分类器  用于对问题分类
        ② 三个数据源  文件、baidu、 google， 接受处理过后的问题按要求搜索数据库返回支撑证据
        ③ 一个打分器  对证据和答案打分
'''
class QuestionAnsweringSystem(object):
    def __init__(self, useWeb):
        # for question parsing
        self._question_classifier = QuestionClassifier.QuestionClassifier()

        # for database
        self._file_source = FileDataSource.FileDataSource()
        self._baidu_source = BaiduDataSource.BaiduDataSource()
        self._google_source = GoogleDataSource.GoogleDataSource()
        self._useWeb = useWeb

        # for answer extraction and ranking
        self._evaluator = Evaluator.Evaluator()

    @property
    def useWeb(self):
        return self._useWeb

    @property
    def question_classifier(self):
        return self._question_classifier

    @property
    def evaluator(self):
        return self._evaluator

    @property
    def file_source(self):
        return self._file_source

    @property
    def baidu_source(self):
        return self._baidu_source

    @property
    def google_source(self):
        return self._google_source

    '''
        回答一个问题

        @param question: Question类型
        return : string 一个答案
    '''
    def answer_question(self, question):
        # 问句分类
        question = self.question_classifier.classify(question)
        # 提取关键词
        question = question.extract_keywords()

        # 问句类型未知，直接当作错误
        if question.str_type == 'UNKNOWN':
            Error.error_ignore('未知类型，拒绝回答！！')
            return 'no answer'  # empty answer

        # 从数据源获得支撑证据
        evidences = self.file_source.get_evidence(question)
        if self.useWeb:
            evidences += self.baidu_source.get_evidence(question)
            evidences += self.google_source.get_evidence(question)

        # empty list
        if not evidences:
            Error.error_ignore('搜索不到证据！！')
            return 'no answer'

        # evidences 装入 question
        question.evidences = evidences
        # 计算证据集合所有词的逆文档频率（idf），之后打分用
        self.evaluator.evidences_idf = Tool.get_idf(evidences)

        # 所有候选答案集合
        all_candidate_answers = []
        # 对每个evidence打分、提取答案以及对答案打分
        for evidence in evidences:
            # 对evidence打分
            evidence = self.evaluator.evalue_evidence(evidence, question)
            # 提取答案
            candidate_answers = evidence.extract_answers(question.get_pos())
            # 对答案打分
            candidate_answers = self.evaluator.evalue_answers(candidate_answers, evidence, question)
            # 合并候选答案
            all_candidate_answers += candidate_answers

        # empty list
        if not all_candidate_answers:
            Error.error_ignore('没有候选答案！！')
            return 'no answer'

        ranked_answers = self.evaluator.rank_answers(all_candidate_answers)

        return ranked_answers[0].str_answer

    '''
        回答一列表的问题

        @param questions:  a list of Question
        return: a list of string
    '''
    def answer_questions(self, questions):
        return [self.answer_question(question) for question in questions]



def main():
    # define cmd line parameter
    parser = OptionParser()
    parser.add_option("-w", "--web",
                      action="store_true",
                      dest="web",
                      default=False,
                      help="Seach answer from both file and web"
                      )
    parser.add_option("-f", "--file",
                      action="store",
                      type="string",
                      dest="filepath",
                      help="path of input file, the file should contain questions only")
    (options, args) = parser.parse_args()

    # whether open field or not
    if options.web:
        question_answering_system = QuestionAnsweringSystem(True)
    else:
        question_answering_system = QuestionAnsweringSystem(False)

    # read questions from file or from cmd line
    if options.filepath is None:
        while True:
            print 'please type in you question (in Chinese), "exit" or "quit" to exit this program:'
            str_question = raw_input().lower()
            if str_question == 'exit' or str_question == 'quit':
                break
            question =Question.Question(Tool.eliminate_question_mark(str_question))
            answer = question_answering_system.answer_question(question)
            print answer
    else:
        with open(options.filepath, 'r') as f:
            questions = [Question.Question(Tool.eliminate_question_mark(str_question)) for str_question in f]
            answers = question_answering_system.answer_questions(questions)
        with open('./test/answers', 'w') as f:
            for answer in answers:
                f.write(answer+'\n')


if __name__ == '__main__':
    main()
