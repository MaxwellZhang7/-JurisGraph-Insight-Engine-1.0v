#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    # {'实体类别1' : [对应句子中的实体],'实体类别2' : [对应句子中的实体]}
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    # res_classify : {'args' : {medical_dict},'question_types':[这个问题类别的列表]}
    # medical_dict : {'问题涉及的实体内容':'实体类别','问题涉及的实体内容':'实体类别',...}
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        quirey = ['defination','belong','xingqi','tuijian','rending','fataio','tezheng']
        # entity_dict : {'实体类别1' : [对应句子中的实体],'实体类别2' : [对应句子中的实体]}
        question_types = res_classify['question_types']# 句子对应的问题类型的列表
        sqls = []
        # 对于每一种问题的类型，每个问题类型中的每个实体类别都会创建一次查询
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type in quirey :
                sql = self.sql_transfer(question_type, entity_dict.get('crime_smalls'))

            elif question_type == "drug_anjian" or question_type == "theft_anjian":
                sql = self.sql_transfer(question_type, entity_dict.get('id'))
            # sql = self.sql_transfer(question_type, entity_dict.get('crime_smalls'))
        
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        # [{'question_type' : 'disease_desc','sql':[这个问题类型对应的查询语句]},{...},{...}]
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        quirey = ['defination','belong','xingqi','tuijian','rending','fataio','tezheng']
        # 查询语句
        sql = []
        # 查询罪名的定义
        if question_type in quirey:
            sql = ["MATCH (n:crime_smalls) -[r]->(m)  where n.name = '{0}' RETURN n, r, m".format(i) for i in entities]

        # 查询疾病的定义
        elif question_type == "drug_anjian" :
            sql = ["MATCH (n:Nh) -[r]->(m)  where n.id = '{0}' RETURN n, r, m".format(i) for i in entities]
        elif question_type == "theft_anjian":
            sql = ["MATCH (n:NHCS) -[r]->(m)  where n.id = '{0}' RETURN n, r, m".format(i) for i in entities]

      
        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
