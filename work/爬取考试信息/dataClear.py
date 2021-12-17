import json
import re

with open('info_dic.json', 'r', encoding='utf-8') as fp:
	res_list = fp.readlines()


count = 0
with open('questions_answer.txt', 'a+', encoding='utf-8') as fp:
	for item in res_list:
		count += 1
		item = re.sub('<.*?>','', item)
		info = item.replace("，", ',').replace('\'', '"').replace('\n', '')
		
		dict_info = json.loads(info)
		question = dict_info.get('question', '没有值')
		answer1 = dict_info.get('answer1', '没有值')
		answer2 = dict_info.get('answer2', '没有值')
		answer3 = dict_info.get('answer3', '没有值')
		answer4 = dict_info.get('answer4', '没有值')
		answer = dict_info.get('test_ans_right', '没有值')
		
		fp.write(f'{count}: {question} \n')
		fp.write(f'    A: {answer1}\n')
		fp.write(f'    A: {answer2}\n')
		fp.write(f'    A: {answer3}\n')
		fp.write(f'    A: {answer4}\n')
		fp.write(f'--- 正确答案： {answer} \n')
	
print('写入完成')


