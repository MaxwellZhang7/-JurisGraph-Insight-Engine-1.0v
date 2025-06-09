# QABasedOnLegalKnowledgeGraph
self-implement of law centered Medical graph from zero to full and sever as question answering base. 从无到有搭建一个以为中心的一定规模法律领域知识图谱，并以该知识图谱完成自动问答与分析服务。

# 项目介绍

知识图谱是目前自然语言处理的一个热门方向 。  
关于知识图谱概念性的介绍就不在此赘述。目前知识图谱在各个领域全面开花，如教育、医疗、司法、金融等。本项目立足法律领域，以法律援助网站为数据来源，以刑法罪名为核心，构建起一个包含多类规模知识实体，多类规模实体关系的知识图谱。
本项目将包括以下两部分的内容：
1) 基于刑法罪名数据的法律知识图谱构建
2) 基于法律知识图谱的大语言模型自动问答


# 项目运行方式
1、配置要求：要求配置neo4j数据库及相应的python依赖包。neo4j数据库用户名密码记住，并修改相应文件。  
2、知识图谱数据导入：python build_crime.py, python build_theft.py，python build_drug.py，导入的数据较多，估计需要几个小时。  
3、启动问答：python chat_graph.py

# 以下介绍详细方案
# 一、法律知识图谱构建
# 1.1 业务驱动的知识图谱构建框架


# 1.2 脚本目录
prepare_data/datasoider.py：网络资讯采集脚本  
prepare_data/datasoider.py：网络资讯采集脚本  
prepare_data/max_cut.py：基于词典的最大向前/向后切分脚本  
build_medicalgraph.py：知识图谱入库脚本    　　

# 1.3 法律领域知识图谱规模
1.3.1 neo4j图数据库存储规模


1.3.2 知识图谱实体类型


# 二、基于医疗知识图谱的自动问答
# 2.1 技术架构


# 2.2 脚本结构
question_classifier.py：问句类型分类脚本  
question_parser.py：问句解析脚本  
chatbot_graph.py：问答程序脚本  


# 总结
１、本项目完成了从无到有，以法律网站为数据来源，构建起以刑法罪名为中心的法律知识图谱。并基于此，搭建起了一个可以回答多类问题的自动问答系统。     
2、本项目以业务驱动，构建法律知识图谱，知识schema设计基于所采集的结构化数据生成(对网页结构化数据进行xpath解析)。    
3、本项目以neo4j作为存储，并基于传统规则的方式完成了知识问答，并最终以cypher查询语句作为问答搜索sql，支持了问答服务。  
4、本项目可以快速部署，本项目的数据，如侵犯相关单位权益，请联系我删除。本数据请勿商用，以免引起不必要的纠纷。在本项目中的部署上，可以遵循项目运行步骤，完成数据库搭建，并提供搜索服务。    


如果运行fail
可是尝试使用 neo4j stop 然后 neo4j.bat console

Elasticsearch 命令行直接执行
