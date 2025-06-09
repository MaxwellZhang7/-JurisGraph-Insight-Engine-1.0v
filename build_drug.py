#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node
import uuid
from faker import Faker   # 1
import random

class LawGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/zong_test.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))

    '''读取文件'''


    @property
    def read_nodes(self):
        # 共７类节点
        def get_label(lis,label):
            l1 = []

            for l in lis:

                if l["label"] ==label:

                    l1.append(l["text"])
            return l1
        def get_triple(lis,label,entity_list1):
            l1 = []
            for l in lis:

                if l["label"] ==label:
                    if l["em2Text"] in entity_list1:
                        l["em2Text"] = entity_list1[l["em2Text"]][-18:]
                    if l["em1Text"] in entity_list1:
                        l["em1Text"] = entity_list1[l["em1Text"]][-18:]                    
                            
                    l1.append([l["em1Text"],l["em2Text"]])
            return l1

        fake = Faker(locale='zh_CN')
        # 实体汇总
        number = []# 案号
        jianchayuan = [] #检察院

        NT =[]# 案发时间
        Ns = []# 案发地
        Nh = [] # 犯罪嫌疑人 同案也是这个标（是否要区分不同）
        ID = [] # 身份证号
        NDR = [] # 毒品名称
        NW = []# 毒品重量
        money = [] # 毒品金额

        drug_infos = []#案例信息
        # 构建节点实体关系
        rels_sell_drugs_to = [] #卖给谁
        rels_traffic_in = [] # 卖什么毒品
        rels_provide_shelter_for = [] # 提供场所吸毒
        rels_possess = [] #拥有属于
        rels_human_id = []
        rels_an_Suspects = []

        with open(self.data_path,encoding ="utf-8") as f:
            datas = list(f)
            count = 0
            for data in datas:
                drug_dict = {}
                count += 1
                print(count)
                # 获取每一条json数据字典
                data_json = json.loads(data)
                # 读取name字段
                entity_list = data_json['entityMentions']
                relations_list = data_json["relationMentions"]
                # 将name字段加入到新建的疾病字典中
                drug_dict['number'] = uuid.uuid1().hex
                drug_dict['district'] = fake.city_name()+fake.district()
                drug_dict['jianchayuan'] = drug_dict['district']+ "检察院"
                drug_dict['NT']=""
                drug_dict['Ns']=""
                drug_dict['Nh']=[]
                drug_dict['ID']=""
                drug_dict['NDR']=""
                drug_dict['NW']=""
                drug_dict['money']=""
                human_dict ={}
                list1 = get_label(entity_list,"Nh")
                if list1!=[]:
                    idl = []
                    list1 = list(set(list1))
                    for l in list1:
                        ssn  =fake.ssn(min_age=18, max_age=90)
                        idl.append(ssn)
                        list1[list1.index(l)] = l + ssn
                        human_dict[l] = l + ssn
                        Nh.append(ssn)
                        drug_dict['Nh'].append(l + ssn)
                        rels_human_id.append([l + ssn,ssn])


                list1 = get_label(entity_list,"NT")
                if list1!=[]:
                    NT += list1
                    drug_dict['NT'] =list1

                list1 = get_label(entity_list,"Ns")
                if list1!=[]:
                    Ns.append(list1[0])
                    drug_dict['Ns'] =list1[0]

                list1 = get_label(entity_list,"NDR")
                if list1!=[]:
                    NDR.append(list1[0]) 
                    drug_dict['NDR'] =list1[0]


                list1 = get_label(entity_list,"NW")
                if list1!=[]:
                    NW += list1      
                    drug_dict['NW']+=list1[0]


                mon  =random.randint(100,1000)
                money.append(mon)  
                drug_dict['money'] =mon     
                
# 关系          
                
                list1 = get_triple(relations_list,"sell_drugs_to",human_dict)

                if list1!=[]:
                    for re in list1:
                        rels_sell_drugs_to.append(re)
                rels_an_Suspects.append([drug_dict['number'],drug_dict['Nh'][0][-18:]])

                list1 = get_triple(relations_list,"traffic_in",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_traffic_in.append(re)

                list1 = get_triple(relations_list,"provide_shelter_for",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_provide_shelter_for.append(re)

                list1 = get_triple(relations_list,"posess",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_possess.append(re)

                drug_infos.append(drug_dict)
            return set(NT), set(Ns), set(Nh), set(ID), set(NDR), set(NW), set(money), drug_infos,\
                rels_sell_drugs_to, rels_traffic_in, rels_provide_shelter_for, rels_possess, rels_an_Suspects
    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print("建节点",count, len(nodes))
        return
      
    '''创建知识图谱中心疾病的节点'''
    def create_anjian_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            node = Node("Anjian", name=drug_dict['number'],jianchayuan = drug_dict['jianchayuan'],district = drug_dict['district'],money = drug_dict['money'],time= drug_dict['NT'])
            self.g.create(node)
            count += 1
            print(count)
        return
    def create_du_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            node = Node("NDR", name=drug_dict['NDR'],weight = drug_dict['NW'],money = drug_dict['money'])
            self.g.create(node)
            count += 1
            print(count)
        return
    def create_human_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            for hu in drug_dict['Nh']:
                node = Node("Nh", name=hu[:-18],id= hu[-18:])
                self.g.create(node)
                count += 1
                print(count)
        return
    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        NT, Ns, Nh, ID, NDR, NW, money, drug_infos,\
                rels_sell_drugs_to, rels_traffic_in, rels_provide_shelter_for, rels_possess,rels_an_Suspects = self.read_nodes
        self.create_anjian_nodes(drug_infos)
        self.create_human_nodes(drug_infos)
        self.create_du_nodes(drug_infos)

        self.create_node('NT', NT)
        print(len(NT))
        self.create_node('Ns', Ns)
        print(len(Ns))

        nodes = NT, Ns, Nh, ID, NDR, NW, money, drug_infos,\
                rels_sell_drugs_to, rels_traffic_in, rels_provide_shelter_for, rels_possess,rels_an_Suspects
        return nodes


    '''创建实体关系边'''
    def create_graphrels(self,nodes):
        NT, Ns, Nh, ID, NDR, NW, money, drug_infos,\
                rels_sell_drugs_to, rels_traffic_in, rels_provide_shelter_for, rels_possess,rels_an_Suspects = nodes  
        self.create_relationship('Nh', 'Nh', rels_sell_drugs_to, 'sell_drugs_to', '交易',hu=3)
        self.create_relationship('Nh', 'NDR', rels_traffic_in, 'traffic_in', '走私',hu =2)
        self.create_relationship('Nh', 'Nh', rels_provide_shelter_for, 'provide_shelter_for', '容留他人吸毒',hu=3)
        self.create_relationship('Nh', 'NDR', rels_possess, 'possess', '非法持有毒品',hu =2)

        self.create_relationship('Anjian', 'Nh', rels_an_Suspects, 'Anjian', '归属案件',hu=1 )

# match(p:Nh),(q:Nh) where p.name='欧阳某仑370400199404112612'and q.name='黑仔450301196109284371' create (p)-[rel:sell_drugs_to{name:'交易毒品'}]->(q)
# match(p:Nh),(q:NDR) where p.name='甲基苯丙胺'and q.name='黑仔510683198710111662' create (p)-[rel:traffic_in{name:'贩卖毒品给'}]->(q)
    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name,hu):
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
            if hu==1:
                query = "match(p:%s),(q:%s) where p.name='%s'and q.id='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            elif hu==2:
                query = "match(p:%s),(q:%s) where p.id='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif hu==1:
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            elif hu==3:
                query = "match(p:%s),(q:%s) where p.id='%s'and q.id='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print("Error creating relationship:", e)
        return

    '''导出数据'''
    # def export_data(self):
    #     crime_bigs, crime_smalls, gainians, tezhengs, rendings, chufas, fatiaos,jieshis,bianhu, ketis,keguans,zhutis,zhuguans, crime_infos,\
    #            rels_crime_big, rels_gainian, rels_tezheng, rels_rending, rels_chufa, rels_fatiao, rels_jieshi, rels_bianhu, rels_zhuguan, rels_zhuti,rels_keguan, rels_keti = self.read_nodes
    #     f_crime_bigs = open('crime_bigs.txt', 'w+')
    #     f_crime_smalls = open('crime_smalls.txt', 'w+')
    #     f_gainians = open('gainians.txt', 'w+')
    #     f_tezhengs = open('tezhengs.txt', 'w+')
    #     f_rendings = open('rendings.txt', 'w+')
    #     f_chufas = open('chufas.txt', 'w+')
    #     f_fatiaos = open('fatiaos.txt', 'w+')

    #     f_jieshis = open('jieshis.txt', 'w+')
    #     f_bianhu = open('bianhu.txt', 'w+')
    #     f_ketis = open('ketis.txt', 'w+')
    #     f_keguans = open('keguans.txt', 'w+')
    #     f_zhutis = open('zhutis.txt', 'w+')
    #     f_zhuguans = open('zhuguans.txt', 'w+')
    #     f_fatiaos = open('fatiaos.txt', 'w+')

    #     f_drug.write('\n'.join(list(Drugs)))
    #     f_food.write('\n'.join(list(Foods)))
    #     f_check.write('\n'.join(list(Checks)))
    #     f_department.write('\n'.join(list(Departments)))
    #     f_producer.write('\n'.join(list(Producers)))
    #     f_symptom.write('\n'.join(list(Symptoms)))
    #     f_disease.write('\n'.join(list(Diseases)))

    #     f_drug.close()
    #     f_food.close()
    #     f_check.close()
    #     f_department.close()
    #     f_producer.close()
    #     f_symptom.close()
    #     f_disease.close()

    #     return



if __name__ == '__main__':

    handler = LawGraph()
    print("step1:导入图谱节点中")
    nodes = handler.create_graphnodes()
    print("step2:导入图谱边中")   
    handler.create_graphrels(nodes)
    # handler.export_data()