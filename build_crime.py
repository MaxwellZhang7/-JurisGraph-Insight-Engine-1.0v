#!/usr/bin/env python3
# coding: utf-8

import os
import json
from py2neo import Graph,Node

class LawGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/crime.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))

    '''读取文件'''
    @property
    def read_nodes(self):
        # 共７类节点
        crime_bigs= [] # 一类罪名
        crime_smalls= [] #二类罪名
        gainians = []#概念
        tezhengs =[]#特征
        rendings = []#认定
        chufas = []#处罚
        fatiaos =[]#法条
        jieshis = []#解释
        bianhus = []#辩护
        ketis = []#客体
        keguans = []#客观
        zhutis =[]#主体
        zhuguans =[]#主观

        crime_infos = []#

        # 构建节点实体关系
        rels_crime_big = [] # 罪名从属
        rels_gainian = [] # 概念从属
        rels_tezheng = [] # 特征从属
        rels_rending = [] #认定
        rels_chufa = [] # 处罚标准
        rels_fatiao = [] # 刑法条文
        rels_jieshi = [] #司法解释
        rels_bianhu =[] # 辩护
        rels_zhuguan = [] # 主观要件
        rels_zhuti = [] #主体要件
        rels_keguan = [] # 客观要件
        rels_keti = [] #　客体要件

        count = 0
        for data in open(self.data_path,encoding='utf-8'):
            crime_dict = {}
            count += 1
            print(count)
            # 获取每一条json数据字典
            data_json = json.loads(data)
            # 读取name字段
            crime_small = data_json['crime_small']
            # 将name字段加入到新建的字典中
            crime_dict['crime_small'] = crime_small
            crime_smalls.append(crime_small)

            crime_dict['crime_big'] = ''
            crime_dict['gainian'] = ''
            crime_dict['tezheng'] = ''
            crime_dict['rending'] = ''
            crime_dict['chufa'] = ''
            crime_dict['fatiao'] = ''
            crime_dict['jieshi'] = ''
            crime_dict['bianhu'] = ''

            if 'crime_big' in data_json:
                crime_bigs.append(data_json['crime_big'])
                rels_crime_big.append([crime_small, data_json['crime_big']])


            if 'gainian' in data_json:
                gainians.append(data_json['gainian'][0])
                rels_gainian.append([crime_small, data_json['gainian'][0]])

            if 'tezheng' in data_json:  # 待处理
                tezhengs += data_json['tezheng']
                for tezheng in data_json['tezheng']:
                    rels_tezheng.append([crime_small, tezheng])

            if 'rending' in data_json: # 待处理
                rendings += data_json['rending']
                for rending in data_json['rending']:
                    rels_rending.append([crime_small, rending])

            if 'chufa' in data_json:
                chufas += data_json['chufa']
                for chufa in data_json['chufa']:
                    rels_chufa.append([crime_small, chufa])

            if 'fatiao' in data_json:
                fatiaos += data_json['fatiao']
                for fatiao in data_json['fatiao']:
                    rels_fatiao.append([crime_small, fatiao])

            if 'jieshi' in data_json:
                jieshis += data_json['jieshi']
                for jieshi in data_json['jieshi']:
                    rels_jieshi.append([crime_small, jieshi])

            if 'bianhu' in data_json:
                bianhus += data_json['bianhu']
                for bianhu in data_json['bianhu']:
                    rels_bianhu.append([crime_small, bianhu])
            crime_infos.append(crime_dict)
        return set(crime_bigs), set(crime_smalls), set(gainians), set(tezhengs), set(rendings), set(chufas), set(fatiaos), set(jieshis),set(bianhus) ,set(ketis),set(keguans), set(zhutis), set(zhuguans), crime_infos,\
               rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti
    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return
            
    '''创建知识图谱的节点'''
    # def create_crime_nodes(self, crime_infos):
    #     count = 0
    #     for crime_dict in crime_infos:
    #         node = Node("Crime", name=crime_dict['crime_small'], crime_big=crime_dict['crime_big'],
    #                     gainian=crime_dict['gainian'] ,tezheng=crime_dict['tezheng'],
    #                     rending=crime_dict['rending'],chufa=crime_dict['chufa'],
    #                     fatiao=crime_dict['fatiao']
    #                     ,jieshi=crime_dict['jieshi'] , bianhu=crime_dict['bianhu'])
    #         self.g.create(node)
    #         count += 1
    #         print(count)
    #     return


    def create_crime_nodes(self):

        node = Node("Crime", name="刑法罪名")   
        self.g.create(node)
        return


    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        crime_bigs, crime_smalls, gainians, tezhengs, rendings, chufas, fatiaos,jieshis,bianhu, ketis,keguans,zhutis,zhuguans, crime_infos,\
               rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti = self.read_nodes
        self.create_crime_nodes()

        self.create_node('crime_bigs', crime_bigs)
        print(len(crime_bigs))
        self.create_node('crime_smalls', crime_smalls)
        print(len(crime_smalls))
        self.create_node('gainians', gainians)
        print(len(gainians))
        self.create_node('tezhengs', tezhengs)
        print(len(tezhengs))
        self.create_node('rendings', rendings)
        print(len(rendings))
        self.create_node('chufas', chufas)
        print(len(chufas))
        self.create_node('fatiaos', fatiaos)
        print(len(fatiaos))
        self.create_node('jieshis', jieshis)
        print(len(jieshis))
        self.create_node('bianhu', bianhu)
        print(len(jieshis))
        self.create_node('ketis', ketis)
        print(len(ketis))
        self.create_node('keguans', keguans)
        print(len(keguans))
        self.create_node('zhutis', zhutis)
        print(len(zhutis))
        self.create_node('zhuguans', zhuguans)
        print(len(zhuguans))
        
        info = crime_bigs, crime_smalls, gainians, tezhengs, rendings, chufas, fatiaos,jieshis,bianhu, ketis,keguans,zhutis,zhuguans, crime_infos,\
               rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti 
        return info


    '''创建实体关系边'''
    def create_graphrels(self,info):
        crime_bigs, crime_smalls, gainians, tezhengs, rendings, chufas, fatiaos,jieshis,bianhu, ketis,keguans,zhutis,zhuguans, crime_infos,\
               rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti = info 
        self.create_relationship('crime_smalls', 'crime_bigs', rels_crime_big, 'crime_bigs', '一级罪名')
        self.create_relationship('crime_smalls', 'gainians', rels_gainian, 'gainians', '概念')
        self.create_relationship('crime_smalls', 'tezhengs', rels_tezheng, 'tezhengs', '特征')
        self.create_relationship('crime_smalls', 'rendings', rels_rending, 'rendings', '认定')
        self.create_relationship('crime_smalls', 'chufas', rels_chufa, 'chufas', '处罚')
        self.create_relationship('crime_smalls', 'fatiaos', rels_fatiao, 'fatiaos', '法条')
        self.create_relationship('crime_smalls', 'jieshis', rels_jieshi, 'jieshis', '解释')
        self.create_relationship('crime_smalls', 'bianhu', rels_bianhu, 'bianhu', '辩护')
        self.create_relationship('crime_smalls', 'zhuguans', rels_zhuguan, 'zhuguans', '主观')
        self.create_relationship('crime_smalls', 'zhuti', rels_zhuti, 'zhuti', '主体')
        self.create_relationship('crime_smalls', 'keguan', rels_keguan, 'keguan', '客观')
        self.create_relationship('crime_smalls', 'keti', rels_keti, 'keti', '客体')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self,info):
        crime_bigs, crime_smalls, gainians, tezhengs, rendings, chufas, fatiaos,jieshis,bianhu, ketis,keguans,zhutis,zhuguans, crime_infos,\
               rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti = info
        f_crime_bigs = open('./dict/crime/crime_bigs.txt', 'w+',encoding="utf-8")
        f_crime_smalls = open('./dict/crime/crime_smalls.txt', 'w+',encoding="utf-8")
        f_gainians = open('./dict/crime/gainians.txt', 'w+',encoding="utf-8")
        f_tezhengs = open('./dict/crime/tezhengs.txt', 'w+',encoding="utf-8")
        f_rendings = open('./dict/crime/rendings.txt', 'w+',encoding="utf-8")
        f_chufas = open('./dict/crime/chufas.txt', 'w+',encoding="utf-8")
        f_fatiaos = open('./dict/crime/fatiaos.txt', 'w+',encoding="utf-8")

        f_jieshis = open('./dict/crime/jieshis.txt', 'w+',encoding="utf-8")
        f_bianhu = open('./dict/crime/bianhu.txt', 'w+',encoding="utf-8")
        f_ketis = open('./dict/crime/ketis.txt', 'w+',encoding="utf-8")
        f_keguans = open('./dict/crime/keguans.txt', 'w+',encoding="utf-8")
        f_zhutis = open('./dict/crime/zhutis.txt', 'w+',encoding="utf-8")
        f_zhuguans = open('./dict/crime/zhuguans.txt', 'w+',encoding="utf-8")
        f_fatiaos = open('./dict/crime/fatiaos.txt', 'w+',encoding="utf-8")

        f_crime_bigs.write('\n'.join(list(crime_bigs)))
        f_crime_smalls.write('\n'.join(list(crime_smalls)))
        f_gainians.write('\n'.join(list(gainians)))
        f_tezhengs.write('\n'.join(list(tezhengs)))
        f_rendings.write('\n'.join(list(rendings)))
        f_chufas.write('\n'.join(list(chufas)))
        f_fatiaos.write('\n'.join(list(fatiaos)))
        f_jieshis.write('\n'.join(list(jieshis)))
        f_bianhu.write('\n'.join(list(bianhu)))
        f_ketis.write('\n'.join(list(ketis)))
        f_keguans.write('\n'.join(list(keguans)))
        f_zhutis.write('\n'.join(list(zhutis)))
        f_zhuguans.write('\n'.join(list(zhuguans)))


        f_crime_bigs.close()
        f_crime_smalls.close()
        f_gainians.close()
        f_tezhengs.close()
        f_rendings.close()
        f_chufas.close()
        f_fatiaos.close()
        f_jieshis.close()
        f_bianhu.close()
        f_ketis.close()
        f_keguans.close()
        f_zhutis.close()
        f_zhuguans.close()

        return



if __name__ == '__main__':

    handler = LawGraph()
    print("step1:导入图谱节点中")
    info = handler.create_graphnodes()
    print("step2:导入图谱边中")   
    handler.create_graphrels(info)
    handler.export_data(info)
