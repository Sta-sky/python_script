import os
import re

class CaesarCrypt:
	def __init__(self):
		self.inputItem = None
		self.numInfo = None
		self.strInfo = None
		self.handleCryptedTxt = None
		self.content_list = []
	
	def selectItem(self):
		paramStr = \
"""
请选择要解密还是加密\n
	1) 输入 E 为加密 \n
	2) 输入 D 为解密 \n
请输入:
"""
		inputItem = input(paramStr).strip()
		select_list = ['e', 'E', 'd', 'D']
		while not inputItem or inputItem not in select_list:
			print('请输入正确的选项')
			inputItem = input(paramStr)
		return inputItem
	
	def inputParam(self):
		paramStr = '1.M 请输入字符串 Enter here: '
		paramNum = '2.R 请输入字符串 Enter here: '
		self.strInfo = self.getParam(paramStr)
		self.numInfo = int(self.getParam(paramNum, True))
	
	def getParam(self, paramTip, isNum=False):
		input_info = input(paramTip)
		if isNum:
			while not input_info.strip() or not self.judgeIsNum(input_info):
				print('\nA number must be entered and cannot be null')
				input_info = input(paramTip)
		else:
			while not input_info.strip():
				print('\nThe request not found')
				input_info = input(paramTip)
		return input_info
	
	def judgeIsNum(self, param):
		try:
			int(param)
			return True
		except Exception as e:
			return False
	
	def deOrEnCrypt(self):
		str_list = list(self.strInfo)
		item = 0
		while item <len(self.strInfo):
			if not str_list[item].isalpha():
				str_list[item] = str_list[item]
			else:
				a = "A" if str_list[item].isupper() else "a"
				if self.inputItem == 'e' or self.inputItem == 'E':
					str_list[item] = chr((ord(str_list[item]) - ord(a) + self.numInfo) % 26 + ord(a))
				else:
					str_list[item] = chr((ord(str_list[item]) - ord(a) - self.numInfo) % 26 + ord(a))
			item = item + 1
		result = ''.join(str_list)
		self.handleCryptedTxt = result.upper()
	
	
	def fileWrite(self):
		totalWordNum = len(self.content_list)
		withoutRepetWord = len(set(self.content_list))
		length_list = list(map(lambda item: len(item), self.content_list))
		length_list.sort()
		max_word = length_list[-1]
		mix_word = length_list[0]
		write_info = \
f"""
{'*' * 100}
总字数         ：{totalWordNum},
不重复单词字数  ：{withoutRepetWord}
最大词长       ：{max_word}
最小词长       ：{mix_word}
"""
		map(lambda item: len(item), self.content_list)
		if self.inputItem == 'd' or self.inputItem == 'D':
			fileName = 'decryptInfo.txt'
		else:
			fileName = 'encryptInfo.txt'
		file_path = os.path.realpath(fileName)
		if not os.path.exists(os.path.realpath(fileName)):
			with open(file_path, 'w', encoding='utf-8'):
				pass
		with open(fileName , 'a', encoding='utf-8') as fp:
			fp.write(write_info)
			result_list = self.sumFrequency()
			for item in result_list:
				itemStr = f'{item[0]}: {item[1]}\n'
				fp.write(itemStr)
			
	def handleFileTxt(self):
		clear_list = "[,.?]"
		if self.inputItem == 'd' or self.inputItem == 'D':
			content = re.sub(clear_list, '', self.handleCryptedTxt)
		else:
			content = re.sub(clear_list, '', self.strInfo)
		self.content_list = [item for item in content.split(' ') if item]
	
	def sumFrequency(self):
		dic = {}
		set_content = list(set(self.content_list))
		for item in set_content:
			count = 0
			for j in self.content_list:
				if item == j:
					count += 1
			dic[item] = count
		result = sorted(dic.items(), key=lambda item: item[1], reverse=True)
		if len(self.content_list) > 5:
			index_list = []
			for index, item in enumerate(result):
				count = 0
				for j in result:
					if item[1] == j[1]:
						count += 1
						if count > 1:
							index_list.append(index)
			new_index = list(set(index_list))
			new_list = []
			for index, item in enumerate(result):
				if index not in new_index:
					new_list.append(item)
		else:
			new_list = result
		return new_list
		
	def run(self):
		self.inputItem = self.selectItem()
		self.inputParam()
		self.deOrEnCrypt()
		self.handleFileTxt()
		self.fileWrite()
		return self.handleCryptedTxt

if __name__ == '__main__':
	result = CaesarCrypt().run()
	print(f"输入信息为：\n {result}")