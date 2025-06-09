import json
def judgerelation(dic):
	if 'from_id' in dic and 'type' in dic:
		return True
	else:
		return False

def text2list(filename):
	temple =[]
	re2id={}
	
	# f = open(, "r", encoding='utf8')
	with open(filename+"/project-9-at-2024-01-02-19-38-90ba018f.json", 'r',encoding='utf-8') as load_f:
		data = json.load(load_f)
		for dic in data:
			flag = False
			triple_list =[]
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
			if len(relation)==0:
				continue
			for k in relation:
				triple_list.append([entity[k[0]],k[2],entity[k[1]]])
			
			dic2 = {}
			# dic = json.loads(line)
			dic2["text"]=dic["data"]["text"]
			# for relation in dic["relationMentions"]:
			# 	if relation["label"] not in re2id.values():
			# 		re2id[str(len(re2id))] = relation["label"]
			# 	triple_list.append([relation["em1Text"],relation["label"],relation["em2Text"]])
			dic2["triple_list"] = triple_list
			temple.append(dic2)
	json_file_path = '/zhuan/train.json'
	json_file = open(filename+json_file_path, mode='w+')
	json.dump(temple, json_file, ensure_ascii = False,indent=4)

text2list("data")