#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier_law import *
from question_parser_law import *
from answer_search_law import *

from crime_qa import *

'''问答类'''
class SimpleQASystem:
    def __init__(self):
        # 构建一个字典参数是{'args' : {medical_dict},'question_types':[这个问题类别的列表]}
        # medical_dict : {'问题涉及的实体内容':'实体类别','问题涉及的实体内容':'实体类别',...}
        self.classifier = QuestionClassifier()

        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
         
        self.qa2 = None
        # self.qa2 = SimpleQASystem2()

    def answer_question(self, sent):

        answer = '您好，我是小正义法律智能助理，希望可以帮到您。'
        graph_data= []
        res_classify = self.classifier.classify(sent)
        # 当classifer返回的是空字典说明没有查询到任何的实体内容，查询失败了
        if not res_classify:
            return self.qa2.answer_question(sent),None

        # 说明传入的问题有实体在知识库中，将这个实体的字典传入parser_main中去
        res_sql = self.parser.parser_main(res_classify) # 这是检索的sql语句
        # [{'question_type' : 'disease_desc','sql':[这个问题类型对应的查询语句]},{...},{...}]
        
        final_answers,graph_data = self.searcher.search_main(res_sql)
        # print(graph_data)
        if not final_answers:
            return self.qa2.answer_question(question),None
        else:
            # return '\n'.join(final_answers)
            return (final_answers,graph_data)

if __name__ == '__main__':
    handler = SimpleQASystem()
    while 1:
        question = input('用户:')
        (answer,graph_data) = handler.answer_question(question)
        # print(graph_data)
        print('小正义:', answer)

