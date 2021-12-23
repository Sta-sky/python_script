import json


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


"""
	使用须知：
		下载 chrome 驱动：
			1、下载chrome浏览器
			2、查看chrome版本
				地址栏输入：chrome://version
					eg:
						Google Chrome	96.0.4664.110 (正式版本) （64 位） (cohort: Stable)
			3、下载对应版本的驱动：
				下载地址: http://chromedriver.storage.googleapis.com/index.html
				 如果没有对应版本 则下载最接近的版本
			4、下载后解压  将 chromedriver.exe 放到 python目录下
				例如：D:\software\Python39
				
				
	注意：zip包中的chromedriver.exe 版本为 96.0 如果你的chrome版本是这个  可以直接放到 python目录下 使用
"""


class Questions():
	def __init__(self):
		self.url = 'https://exam.kaoshixing.com/exam/enter_exam/210024/507501'
		self.brower = webdriver.Chrome()
		self.brower.set_window_size(1200, 800)
		self.href_list = []
	
	def login(self):
		self.brower.get(self.url)
		WebDriverWait(self.brower, 10).until(ec.presence_of_element_located((By.ID, "username")))
		self.brower.find_element(By.ID, 'username').send_keys('NFDW36')
		self.brower.find_element(By.ID, 'userTypePwd').send_keys('Nfdw@123')
		time.sleep(1)
		self.brower.find_element(By.ID, 'loginBtn').click()
		
	
	def get_item_click(self):
		WebDriverWait(self.brower, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "startExam")))
		self.brower.find_element(By.CLASS_NAME, "startExam").click()
		WebDriverWait(self.brower, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "box-list")))
		self.href_list = self.brower.find_elements(By.CLASS_NAME, "iconBox")


	def get_and_write(self):
		count = 0
		total = len(self.href_list)
		point = 71
		for item in self.href_list[point:]:
			count += 1
			point += 1
			item.click()
			time.sleep(2)
			value = self.brower.execute_script('return localStorage.getItem("questionNumber");')
			info_dic = json.loads(value)
			with open('info_dic.json', 'r', encoding='utf-8') as fp:
				json_dic = fp.readlines()
			with open('info_dic.json', 'a+', encoding='utf-8') as fp:
				for value in info_dic.values():
					mid_data = str(value) + '\n'
					if mid_data not in json_dic:
						fp.write(mid_data)
						print("\033[2;031m 文件写入完成 \033[m")

			print(f"\033[4;034m总共 {total}道题 当前第 {count} 个 本地存储长度{len(info_dic)} \033[m")
			
	def run(self):
		try:
			self.login()
			self.get_item_click()
			time.sleep(2)
			self.get_and_write()
			time.sleep(1)
			self.brower.close()
		except Exception as e:
			print(e)
if __name__ == '__main__':
	question = Questions()
	question.run()


		

