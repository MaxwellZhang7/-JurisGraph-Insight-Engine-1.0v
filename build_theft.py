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
        self.data_path = os.path.join(cur_dir, 'data/pro.json')
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
        def judgerelation(dic):
            if 'from_id' in dic and 'type' in dic:
                return True
            else:
                return False
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
        NS = []# 案发地
        NHCS  = [] # 犯罪嫌疑人 同案也是这个标（是否要区分不同）
        NHVI   = [] # 受害人
        NHMZ =[]
        ID = [] # 身份证号
        NASI = [] # 被盗物品

        NCGV = [] # 钱

        drug_infos = []#案例信息
        # 构建节点实体关系
        rels_theft = [] #卖给谁
        rels_possess = [] # 卖什么毒品
        rels_traffic = [] # 提供场所吸毒
        rels_accomplice = [] #拥有属于

        rels_human_id = []

        rels_an_Suspects = []
        with open(self.data_path,encoding ="utf-8") as load_f:
            data = json.load(load_f)
            count =1
            for dic in data:
                flag = False
                relations_list =[]
                entity_list = []
                entity ={}
                relation= []
                for j in dic["annotations"][0]["result"]:
                    if judgerelation(j):
                        if len(j["labels"])>0:
                            print(j["from_id"],j["to_id"],j["labels"][0])
                            relation.append((j["from_id"],j["to_id"],j["labels"][0]))
                        else:
                            continue
                    else:
                        entity[j["id"]] = j["value"]["text"]
                        entity_list.append({"text":j["value"]["text"],"label":j["value"]["labels"][0]})
                if len(relation)==0:
                    continue
                for k in relation:
                    relations_list.append({"em1Text":entity[k[0]],"label":k[2],"em2Text":entity[k[1]]})
                
                drug_dict = {}
                count += 1
                # 将name字段加入到新建的疾病字典中
                drug_dict['number'] = uuid.uuid1().hex
                drug_dict['district'] = fake.city_name()+fake.district()
                drug_dict['jianchayuan'] = drug_dict['district']+ "检察院"
                drug_dict['NT']=""
                drug_dict['NS']=""
                drug_dict['NHCS']=[]
                drug_dict['NHVI']=[]
                
                drug_dict['ID']=""
                drug_dict['NASI']=""
                drug_dict['NCGV']=""
                human_dict ={}

                list1 = get_label(entity_list,"NHCS")
                if list1!=[]:
                    idl = []
                    list1 = list(set(list1))
                    for l in list1:
                        ssn  =fake.ssn(min_age=18, max_age=90)
                        idl.append(ssn)
                        list1[list1.index(l)] = l + ssn
                        human_dict[l] = l + ssn
                        NHCS.append(ssn)
                        drug_dict['NHCS'].append(l + ssn)
                        rels_human_id.append([l + ssn,ssn])

                list1 = get_label(entity_list,"NHVI")
                if list1!=[]:
                    idl = []
                    list1 = list(set(list1))
                    for l in list1:
                        ssn  =fake.ssn(min_age=18, max_age=90)
                        idl.append(ssn)
                        list1[list1.index(l)] = l + ssn
                        human_dict[l] = l + ssn
                        NHVI.append(ssn)
                        drug_dict['NHVI'].append(l + ssn)
                        rels_human_id.append([l + ssn,ssn])
                list1 = get_label(entity_list,"买赃物的人")
                if list1!=[]:
                    idl = []
                    list1 = list(set(list1))
                    for l in list1:
                        ssn  =fake.ssn(min_age=18, max_age=90)
                        idl.append(ssn)
                        list1[list1.index(l)] = l + ssn
                        human_dict[l] = l + ssn
                        NHCS.append(ssn)
                        drug_dict['NHCS'].append(l + ssn)
                        rels_human_id.append([l + ssn,ssn])

                list1 = get_label(entity_list,"NT")
                if list1!=[]:
                    NT += list1
                    drug_dict['NT'] =list1

                list1 = get_label(entity_list,"NS")
                if list1!=[]:
                    NS.append(list1[0])
                    drug_dict['NS'] =list1[0]

                list1 = get_label(entity_list,"NASI")
                if list1!=[]:
                    NASI.append(list1[0]) 
                    drug_dict['NASI'] =list1[0]

                list1 = get_label(entity_list,"NCGV")
                if list1!=[]:
                    NCGV += list1      
                    drug_dict['NCGV']+=list1[0]

                # mon  =random.randint(100,1000)
                # money.append(mon)  
                # drug_dict['money'] =mon     
                
# 关系          
                
                list1 = get_triple(relations_list,"theft",human_dict)

                if list1!=[]:
                    for re in list1:
                        rels_theft.append(re)

                rels_an_Suspects.append([drug_dict['number'],drug_dict['NHCS'][0][-18:]])

                list1 = get_triple(relations_list,"traffic",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_traffic.append(re)

                list1 = get_triple(relations_list,"possess",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_possess.append(re)

                list1 = get_triple(relations_list,"accomplice",human_dict)
                if list1!=[]:
                    for re in list1:
                        rels_accomplice.append(re)

                drug_infos.append(drug_dict)
            return set(NT), set(NS), set(NHCS), set(NHVI),set(ID), set(NASI), set(NCGV), drug_infos,\
                rels_theft, rels_traffic, rels_accomplice, rels_possess, rels_an_Suspects
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
            node = Node("Anjian", name=drug_dict['number'],jianchayuan = drug_dict['jianchayuan'],district = drug_dict['district'],money = drug_dict['NCGV'],time= drug_dict['NT'])
            self.g.create(node)
            count += 1
            print(count)
        return
    def create_du_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            node = Node("NASI", name=drug_dict['NASI'],money = drug_dict['NCGV'])
            self.g.create(node)
            count += 1
            print(count)
        return
    def create_human_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            for hu in drug_dict['NHCS']:
                node = Node("NHCS", name=hu[:-18],id= hu[-18:])
                self.g.create(node)
                count += 1
                print(count)
        return
    def create_humanvi_nodes(self, drug_infos):
        count = 0
        for drug_dict in drug_infos:
            for hu in drug_dict['NHVI']:
                node = Node("NHVI", name=hu[:-18],id= hu[-18:])
                self.g.create(node)
                count += 1
                print(count)
        return
    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        NT, NS, NHCS, NHVI,ID, NASI, NCGV, drug_infos,\
                rels_theft, rels_traffic, rels_accomplice, rels_possess, rels_an_Suspects = self.read_nodes
        self.create_anjian_nodes(drug_infos)
        self.create_human_nodes(drug_infos)
        self.create_humanvi_nodes(drug_infos)
        self.create_du_nodes(drug_infos)

        self.create_node('NT', NT)
        print(len(NT))
        self.create_node('NS', NS)
        print(len(NS))

        nodes = NT, NS, NHCS, NHVI,ID, NASI, NCGV, drug_infos,\
                rels_theft, rels_traffic, rels_accomplice, rels_possess, rels_an_Suspects
        return nodes


    '''创建实体关系边'''
    def create_graphrels(self,nodes):
        NT, NS, NHCS, NHVI,ID, NASI, NCGV, drug_infos,\
                rels_theft, rels_traffic, rels_accomplice, rels_possess, rels_an_Suspects = nodes  
        self.create_relationship('NHCS', 'NASI', rels_theft, 'theft', '盗窃',hu=10)
        self.create_relationship('NHCS', 'NHCS', rels_accomplice, 'accomplice', '共犯',hu =11)
        self.create_relationship('NHCS', 'NHCS', rels_traffic, 'traffic', '交易',hu=11)
        self.create_relationship('NHVI', 'NASI', rels_possess, 'possess', '所属',hu =10)

        self.create_relationship('Anjian', 'NHCS', rels_an_Suspects, 'Anjian', '归属案件',hu=000 )

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
            if hu==000:
                query = "match(p:%s),(q:%s) where p.name='%s'and q.id='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            elif hu==10:
                query = "match(p:%s),(q:%s) where p.id='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
            elif hu==00:
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            elif hu==11:
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