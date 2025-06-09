from LAC import LAC

def lac_username(sentences: str) -> list:
    # 装载LAC模型
    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            user_name_list.append(lac_result[0][index])
    return user_name_list


if __name__ == '__main__':
	print(lac_username("请写出张智星的犯罪记录"))