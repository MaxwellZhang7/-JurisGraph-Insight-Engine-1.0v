from flask import Flask, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j数据库连接配置
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123"  # 请将此处的 your_password 替换为你的数据库密码

# 创建Neo4j数据库连接
driver = GraphDatabase.driver(uri, auth=(username, password))

# 定义查询知识图谱的Cypher语句
query = """
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 25
"""

# 定义获取知识图谱数据的函数
def get_knowledge_graph_data():
	with driver.session() as session:
		data = []
		result = session.run(query).data()
		for rel in result:
			source_name = rel["r"][0]["name"]
			target_name = rel["r"][-1]["name"]
			relationship_name = rel["r"][1]
			data.append({"data": {"source": source_name, "target": target_name, "relationship": relationship_name}})
			data.append({"data": {"id": source_name}})
			data.append({"data": {"id": target_name}})

		unique_data = []
		for d in data:
			if d not in unique_data:
				unique_data.append(d)
		print(unique_data)
		return unique_data

# 定义路由和视图函数
@app.route('/')
def index():
	graph_data = get_knowledge_graph_data()
	return render_template('index4.html', graph_data=graph_data) # 表示测试用例

if __name__ == '__main__':
	app.run(debug=True)