#!/usr/bin/env python3
# coding: utf-8

import os
import ahocorasick

# from LAC import LAC
class QuestionClassifier:
    # 初始化函数
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.crime_smalls = os.path.join(cur_dir, 'dict/crime/crime_smalls.txt')
        self.crime_bigs = os.path.join(cur_dir, 'dict/crime/crime_bigs.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')

        # 加载特征词
        self.crime_smalls_wds= [i.strip() for i in open(self.crime_smalls,encoding= "utf-8") if i.strip()]
        self.crime_bigs_wds= [i.strip() for i in open(self.crime_bigs,encoding= "utf-8") if i.strip()]

        self.region_words = set(self.crime_smalls_wds + self.crime_bigs_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding= "utf-8") if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.defination_qwds = ['定义', '解释', '现象', '概念', '表现',"什么","意思","含义"]
        # self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.belong_qwds = ['属于什么罪名', '属于', '什么罪']
        self.xingqi_qwds = ['审判',"判刑","刑期","判多少年","进监狱"]
        self.tuijian_qwds = ["辩护"]
        self.rending_qwds = ["如何区分","比较异同","比较","认定","区别"]# 认定
        self.fatiao_qwds = ["法条","法律条文"]
        self.jieshi_qwds = ["司法解释","解释"]
        self.tezheng_qwds = ["特征","特点"]
        self.drug_anjian_qwds = ["毒品","贩毒","涉毒"]
        self.theft_anjian_qwds = ["盗窃","偷"]
        
        print('model init finished ......')

        return
    def judge_person(sentences: str) -> list:
        flag =0
        for i in sentences:
            if i in ["0","1","2","3","4","5","6","7","8","9"]:
                flag +=1
            else:
                flag =0
            if flag ==18:
                break
        return flag ==18

    '''分类主函数'''
    # 分类函数入口
    def judge_id(self,question):
        result =[]
        for char in question:
            if char.isdigit():

                result.append(char)
            else:
                if len(result) != 18:
                    result=[]
                else:
                    break
        return ''.join(result)

    def classify(self, question):
        data = {}
        medical_dict = self.check_treeentity(question)


        if self.judge_id(question):
            medical_dict[self.judge_id(question)] = ['id']
            question_type = "anjian"
        if not medical_dict:# 如果字典是空的就返回空字典
            return {}
        data['args'] = medical_dict# 构建一个字典参数是{'args' : {medical_dict},'question_types':[这个问题类别的列表]}  
        
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 判断是否为定义的问题
        if self.check_words(self.defination_qwds, question) and ('crime_smalls' in types):
            question_type = 'defination'
            question_types.append(question_type)

        elif self.check_words(self.belong_qwds, question) and ('crime_smalls' in types):
            question_type = 'belong'
            question_types.append(question_type)

        elif self.check_words(self.xingqi_qwds, question) and ('crime_smalls' in types):
            question_type = 'xingqi'
            question_types.append(question_type)

        elif self.check_words(self.tuijian_qwds, question) and ('crime_smalls' in types):
            question_type = 'tuijian'
            question_types.append(question_type)

        elif self.check_words(self.rending_qwds, question) and ('crime_smalls' in types):
            question_type = 'rending'
            question_types.append(question_type)
        elif self.check_words(self.tezheng_qwds, question) and ('crime_smalls' in types):
            question_type = 'tezheng'
            question_types.append(question_type)
        elif self.check_words(self.fatiao_qwds, question) and ('crime_smalls' in types):
            question_type = 'fatiao'
            question_types.append(question_type)
        elif self.check_words(self.jieshi_qwds, question) and ('crime_smalls' in types):
            question_type = 'jieshi'
            question_types.append(question_type)
        elif self.check_words(self.drug_anjian_qwds, question) and self.judge_id(question):
            question_type = 'drug_anjian'
            question_types.append(question_type)
        elif self.check_words(self.theft_anjian_qwds, question) and self.judge_id(question):
            question_type = 'theft_anjian'
            question_types.append(question_type)
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


# ['drug_anjian','theft_anjian']


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            # {'心理病':['disease','symptom'],'实体2':['类别1','类别2'],...,'所有的实体':['实体类别','实体类别']}
            wd_dict[wd] = []
            if wd in self.crime_smalls_wds:
                wd_dict[wd].append('crime_smalls')
            if wd in self.crime_bigs_wds:
                wd_dict[wd].append('crime_bigs')
            # if wd in self.name_wds:
            #     wd_dict[wd].append('name')

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_treeentity(self, question):
        region_wds = []
        # 遍历那个ac树找到这个句子中拥有的所有实体 index (index,'实体')
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            # i[1][1]就是这个对应的实体，将这个对应的实体加入到这个列表中去
            region_wds.append(wd)
        stop_wds = []
        # 除去冗余的实体内容，最后返回final_wds为输入问句中所有需要的实体
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        # 通过上面的字典构建问句中实体的字典{'实体内容':'实体类别','实体内容':'实体类别',...}
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
        # 构建一个字典参数是{'args' : {medical_dict},'question_types':[这个问题类别的列表]}
        # medical_dict : {'问题涉及的实体内容':'实体类别','问题涉及的实体内容':'实体类别',...}
