#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, render_template
from neo4j import GraphDatabase
from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))

        self.num_limit = 20


    def delete(self,text):

        punctuation_string = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
        for i in punctuation_string:
            text = text.replace(i, '')
        return text
   
    def search_main(self, sqls):
        final_answers = []
        graph_data = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            selected_data = []

            if question_type=="defination":       
                for d in answers:
                    if d["r"]["name"]=="概念" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="belong":       
                for d in answers:
                    if d["r"]["name"]=="一级罪名" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="xingqi":       
                for d in answers:
                    if d["r"]["name"]=="处罚" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="fatiao":       
                for d in answers:
                    if d["r"]["name"]=="法条" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="jieshi":       
                for d in answers:
                    if d["r"]["name"]=="解释" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="tuijian":       
                for d in answers:
                    if d["r"]["name"]=="辩护" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="tezheng":       
                for d in answers:
                    if d["r"]["name"]=="特征" and  d not in selected_data:
                        selected_data.append(d)
            elif question_type=="rending":       
                for d in answers:
                    if d["r"]["name"]=="认定" and  d not in selected_data:
                        selected_data.append(d) 
            elif question_type=="drug_anjian":       
                for d in answers:
                    
                    selected_data.append(d)  
            elif question_type=="theft_anjian":       
                for d in answers:
                    
                    selected_data.append(d)  
            # elif question_type=="defination":       
            #     for d in answers:
            #         if d["r"]["name"]=="主观" and  d not in selected_data:
            #             selected_data.append(d)
            # elif question_type=="defination":       
            #     for d in answers:
            #         if d["r"]["name"]=="客观" and  d not in selected_data:
            #             selected_data.append(d)
          
                    # elif d["r"]["name"]=="解释" and  d not in selected_data:
                    #     selected_data.append(d)
                    # elif d["r"]["name"]=="辩护" and  d not in selected_data:
                    #     selected_data.append(d)
                    # elif d["r"]["name"]=="主观" and  d not in selected_data:
                    #     selected_data.append(d)
            elif question_type=="other":
                selected_data = answers

            # unique_data = []
            # for d in selected_data:
            #     if d not in unique_data:
            #         unique_data.append(d)

            
            for rel in selected_data:
                source_name = str(self.delete(rel["n"]["name"]))
                target_name = str(self.delete(rel["m"]["name"]))
                relationship_name = rel["r"][1]
                graph_data.append({"data": {"source": source_name, "target": target_name, "relationship": relationship_name}})
                graph_data.append({"data": {"id": source_name}})
                graph_data.append({"data": {"id": target_name}})

            final_answer = self.answer_prettify(question_type, selected_data)
            if final_answer:
                final_answers.append(final_answer)
        # print(graph_data)
        return final_answers,graph_data

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'belong':
            desc = [i["m"]["name"] for i in answers]  
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的一级罪名为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'defination':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的定义为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'xingqi':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的刑期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'tuijian':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的庭审辩护词为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'rending':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的认定为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'fataio':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的相关法条为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'tezheng':
            desc = [i["m"]["name"] for i in answers]
            subject = answers[0]["n"]["name"]
            final_answer = '{0}的特征为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'drug_anjian':

            final_answer = '详情请见右侧图谱'
        elif question_type == 'theft_anjian':

            final_answer = '详情请见右侧图谱'
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    st = "的符合法规和释放 豆腐干豆腐干的dfgfd..,,/'"
    print(searcher.delete(st))
