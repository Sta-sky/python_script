import os
import random
import re

firstParamStr = \
"""\033[1;34m
请选择要解密还是加密\n
	1.M) 输入 M 为 手动加密、解密 \n
	2.R) 输入 R 为 自动加密、解密 \n
请输入:

\033[m"""

secondParamStr = \
"""\033[1;34m
请选择要解密还是加密\n
	1.D) 输入 D 为解密 \n
	2.E) 输入 E 为加密 \n
请输入:
\033[m"""



class CaesarCrypt:
	def __init__(self):
		self.inputFirstItem = None
		self.inputSecondItem = None
		self.numInfo = None
		self.strInfo = None
		self.handleCryptedTxt = None
		self.autoTextFile = None
		self.insertFilePath = None
		self.content_list = []
		self.firstSelectList = ['m', 'M', 'r', 'R']
		self.secondSelect_list = ['e', 'E', 'd', 'D']
	
	def selectItem(self):
		inputItem = input(firstParamStr).strip()
		while not inputItem or inputItem not in self.firstSelectList:
			print('\033[31m 请输入正确的选项\033[m')
			inputItem = input(firstParamStr)
		self.inputFirstItem = inputItem
		inputItem = input(secondParamStr).strip()
		if inputItem == 'm' or inputItem == 'M':
			while not inputItem or inputItem not in self.secondSelect_list:
				print('请输入正确的选项')
				inputItem = input(secondParamStr)
			self.inputSecondItem = inputItem
		else:
			self.inputSecondItem = inputItem
			if self.inputSecondItem == 'd' or self.inputSecondItem == 'd':
				with open('./info.txt', 'r') as fp:
					textList = fp.readlines()
				self.autoTextFile = [item.strip().replace('\n', '') for item in textList]
	
	def firstinputParam(self):
		""" 获取输入信息 """
		paramStr = '1.M 请输入字符串，或.txt后缀文本路径\n 请输入： '
		paramNum = '2.R 请输入位移量 : '
		self.strInfo = self.getParam(paramStr)
		self.parseFilePath()
		self.numInfo = int(self.getParam(paramNum, True))
		
	def secondinputParam(self):
		paramStr = '1.请输入字符串，或.txt后缀文本路径\n 请输入 ：'
		self.strInfo = self.getParam(paramStr)
		self.parseFilePath()
	
	def parseFilePath(self):
		if self.strInfo.split('.')[-1] == 'txt':
			while not os.path.exists(self.strInfo):
				print('\033[31m 文件路径不正确 请重新输入\033[m')
				self.insertFilePath = self.getParam('请输入文件路径:')
			else:
				self.insertFilePath = self.strInfo
			with open(self.strInfo, 'r') as fp:
				dataList = fp.readlines()
			self.strInfo = ''.join(dataList).strip().replace('\n', ' ')
	
	def getParam(self, paramTip, isNum=False):
		""" 循环获取正确输入信息 """
		input_info = input(paramTip)
		if isNum:
			while not input_info.strip() or not self.judgeIsNum(input_info):
				print('\nA number must be entered and cannot be null')
				input_info = input(paramTip)
		else:
			while not input_info.strip():
				print('\nThe request not found')
				input_info = input(paramTip)
		return input_info.strip().replace('\n', ' ')
	
	def judgeIsNum(self, param):
		""" 判断是否为数字类型 """
		try:
			int(param)
			return True
		except Exception as e:
			return False
	
	def autoDeCrypt(self):
		""" 自动解密 """
		for num in range(26):
			str_list = list(self.strInfo)
			item = 0
			while item <len(self.strInfo):
				if not str_list[item].isalpha():
					str_list[item] = str_list[item]
				else:
					a = "A" if str_list[item].isupper() else "a"
					str_list[item] = chr((ord(str_list[item]) - ord(a) - num) % 26 + ord(a))
				item = item + 1
			result = ''.join(str_list)
			beforeTen = result.split(' ')[:10]
			flag = False
			for item in beforeTen:
				if item in self.autoTextFile or item.lower() in self.autoTextFile:
					flag = True
			if flag:
				print(f'解密结果为：{result}')
				userConfirm = input('请确认解密是否正确')
				if userConfirm == 'yes' or userConfirm == 'YES' or userConfirm == 'Y':
					self.handleCryptedTxt = result
					return True
		self.handleCryptedTxt = ''
		return False
	
	def autoEncrypt(self):
		str_list = list(self.strInfo)
		item = 0
		genrateNum = random.randint(1, 26)
		while item <len(self.strInfo):
			if not str_list[item].isalpha():
				str_list[item] = str_list[item]
			else:
				a = "A" if str_list[item].isupper() else "a"
				str_list[item] = chr((ord(str_list[item]) - ord(a) + genrateNum) % 26 + ord(a))
			item = item + 1
		result = ''.join(str_list)
		self.handleCryptedTxt = result.upper()
	
	def decrypt(self):
		""" 解密 """
		str_list = list(self.strInfo)
		item = 0
		while item <len(self.strInfo):
			if not str_list[item].isalpha():
				str_list[item] = str_list[item]
			else:
				a = "A" if str_list[item].isupper() else "a"
				str_list[item] = chr((ord(str_list[item]) - ord(a) - self.numInfo) % 26 + ord(a))
			item = item + 1
		result = ''.join(str_list)
		self.handleCryptedTxt = result.upper()
	
	def encrypt(self):
		""" 加密 """
		str_list = list(self.strInfo)
		item = 0
		while item <len(self.strInfo):
			if not str_list[item].isalpha():
				str_list[item] = str_list[item]
			else:
				a = "A" if str_list[item].isupper() else "a"
				str_list[item] = chr((ord(str_list[item]) - ord(a) + self.numInfo) % 26 + ord(a))
			item = item + 1
		result = ''.join(str_list)
		self.handleCryptedTxt = result.upper()
	
	def fileWrite(self):
		""" 文件写入 """
		totalWordNum = len(self.content_list)
		withoutRepetWord = len(set(self.content_list))
		length_list = list(map(lambda item: len(item), self.content_list))
		length_list.sort()
		max_word = length_list[-1]
		mix_word = length_list[0]
		R_dir = os.path.realpath('R')
		M_dir = os.path.realpath('M')
		if not os.path.exists(R_dir) :
			os.mkdir(R_dir)
		if not os.path.exists(M_dir):
			os.mkdir(M_dir)
		fileDict = {
			'TOTAL_NUMBER.txt': f'Total number of the words: {totalWordNum}',
			'UNIQUE_WORDS.txt': f'Number of unique words: {withoutRepetWord}' ,
			'MINIMUM.txt': f'Minimum word length: {max_word}',
			'MAXIMUM.txt': f'Maximum word length: {mix_word}',
			'MOST_COMMON_LETTER.txt': self.sumFrequency()
		}
		if self.inputFirstItem == 'm' or self.inputFirstItem == 'M':
			filePath = os.path.realpath('M')
		else:
			filePath = os.path.realpath('R')
		createFile(fileDict, filePath)
	
	def handleFileTxt(self):
		""" 处理文件标点 可在下列 clear_list 添加任意标点 """
		clear_list = "[,.?]"
		if self.inputSecondItem == 'd' or self.inputSecondItem == 'D':
			content = re.sub(clear_list, '', self.handleCryptedTxt)
		else:
			content = re.sub(clear_list, '', self.strInfo)
		self.content_list = [item for item in content.split(' ') if item]
	
	def sumFrequency(self):
		""" 计算单词出现次数 """
		dic = {}
		self.content_list = [item.upper() for item in self.content_list ]
		set_content = list(set(self.content_list))
		for item in set_content:
			count = 0
			for j in self.content_list:
				if item == j or item.lower() == j :
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
		mostWord = ''
		print("\033[6;31m 频率统计结果如下：\033[m")
		for item in new_list:
			itemStr = f'{item[0]}: {item[1]}\n'
			print(f"\033[6;36m {itemStr} \033[m")
			mostWord += itemStr
		return mostWord
			
	def run(self):
		""" 入口 """
		self.selectItem()
		if self.inputFirstItem == 'm' or self.inputFirstItem == 'M':
			self.firstinputParam()
			if self.inputSecondItem == 'd' or self.inputSecondItem == 'E':
				self.decrypt()
			else:
				self.encrypt()
		else:
			self.secondinputParam()
			if self.inputSecondItem == 'd' or self.inputSecondItem == 'E':
				self.autoDeCrypt()
			else:
				self.autoEncrypt()
		if not self.handleCryptedTxt:
			return '输出失败'
		self.handleFileTxt()
		self.fileWrite()
		return self.handleCryptedTxt


def createFile(fileDict, filePath):
	for key, val in fileDict.items():
		path = f'{filePath}/{key}'
		with open(path, 'a+', encoding='utf-8') as fp:
			fp.write('*' * 200 + '\n')
			fp.write(str(val) + '\n')

if __name__ == '__main__':
	result = CaesarCrypt().run()
	print(f"\033[32m 输入信息为：\n {result} \033[m")

