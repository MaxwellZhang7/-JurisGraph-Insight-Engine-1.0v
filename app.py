# app.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
# from your_qa_system import SimpleQASystem # 测试样例
# from crime_qa import SimpleQASystem #百科问答对
from chatbot_graph import SimpleQASystem    #知识图谱筛选
import datetime
import json
#long running



app = Flask(__name__, static_folder='static')
qa_system = SimpleQASystem()
graph_data= []


@app.route('/')
def index():

    return render_template('index5.html', conversation_history=[],graph_data=[])

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    starttime = datetime.datetime.now()
    # (result,graph_data) = qa_system.answer_question(question)
    (result,graph_data) = qa_system.answer_question(question)
    # result = "东莞市第三市区人民检察院指控，2014年10月下旬的一天中午，被告人张守东接到李某的电话称要购买毒品（冰毒），双方约好在李某位于东莞市**镇**路*号**公寓**房的暂住处进行交易后，张守东到**市**镇**路*号**公寓**房，以每包100元人民币的价格贩卖给李某7小包毒品（冰毒，每包约1克，共7克）。"
    result="2016年11月10日12时许，朱某甲因其苹果手机充电出现故障，即找租住在其家三楼的租户借用充电线，在拿充电线时，顺手将苹果手机窃走"
#     graph_data=[{'source': '朱某甲', 'target': '苹果手机', 'relationship': '盗窃'},
# {'data': {'id': '朱某甲'}},
# {'data': {'id': '苹果手机'}},
# {'source': '卓某某', 'target': '苹果手机', 'relationship': '所属'},
# {'data': {'id': '卓某某'}}
# ]
    
    endtime = datetime.datetime.now()
    print (endtime - starttime)
    conversation_history = request.form.getlist('conversation_history')
    conversation_history.append({'question': question, 'answer': result})

    return jsonify({'question': question, 'answer': result, 'conversation_history': conversation_history,"graph_data":graph_data})

if __name__ == '__main__':
    app.run(debug=True)
