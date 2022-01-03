import base64
import math
import random
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tqdm import tqdm



class getInfo:
	def __init__(self):
		# option = webdriver.ChromeOptions()
		# option.headless = True
		self.base_url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd={0}&rsv_spt=1&oq={0}&rsv_pq=f6c7fa7700068dd6&rsv_t=63551Ytlk%2F5XzYKfU7QpKBSYPJEnaXJR0OLwJSm7%2BcZc%2Bmtop%2Fe6MgxxXqaLaQzlNf%2Fc&rqlang=cn&rsv_enter=1&rsv_dl=tb&gpc=stf%3D1262275200%2C1640880000%7Cstftype%3D2&tfflag=1"
		self.url = None
		self.browser = webdriver.Chrome()
		self.city_list = []
		self.search_key_list = []
		self.history_list = []
		self.total = None

	def read_text(self):
		with open('./search_key.txt', 'r', encoding='utf-8')as fp:
			search_data = fp.read()
		self.search_key_list = search_data.split("、")
		
		with open('./city.txt', 'r', encoding='utf-8')as fp:
			city_data = fp.readlines()
		self.city_list = [item.replace('\n', '') for item in city_data]
		
		with open('./history.txt', 'r', encoding='utf-8')as fp:
			self.history_list = fp.readlines()
			
		self.total = len(self.search_key_list) * len(self.city_list)
	
	def loop_get_info(self):
		count = 0
		try:
			with tqdm(total=self.total) as bar:
				for city in self.city_list:
					for key in self.search_key_list:
						key_word = f'{city} {key}'
						time.sleep(1)
						count += 1
						if not self.key_word_get_info(key_word, bar):
							with open('./error.txt', 'a+', encoding='utf-8') as errFp:
								errFp.write(f'{key_word}\n')
								print(f'\033[3;33m获取{key_word}失败， 已写入错误文件中！\033[m')
						print(f'\033[3;35m获取{key_word}完成， 当前第:{count}个\033[m')
		except Exception as e:
			print(e, ']]')
			
	
	def key_word_get_info(self, key_word, bar):
		if f'{key_word}\n' not in self.history_list:
			count = 0
			while True:
				if not self.get_url_info(key_word):
					if count > 10:
						return False
				else:
					break
			speed = float('%.10f' % (1 / self.total))
			print(speed, type(speed))
			bar.update(speed)
		else:
			print(f'{key_word}: 数据已经存在')
			return True
			

	def get_url_info(self, key_word):
		try:
			self.url = self.base_url.format(key_word)
			self.browser.get(self.url)
			time.sleep(2)
			if '百度安全验证' in str(self.browser.page_source):
				while True:
					time.sleep(random.uniform(3, 5))
					try:
						rotation_image_src = self.browser.find_element(By.XPATH,
							'//FaceImg[@class="vcode-spin-FaceImg"]').get_attribute('src')
						rotation_image = requests.get(rotation_image_src).content
						with open('./rotation_image.png', 'wb')as f:
							f.write(rotation_image)
					except Exception as error:
						print(error)
						self.browser.refresh()
						time.sleep(4)
						continue
					try:
						distance_api = int(self.base64_api())
					except Exception as error:
						print(error)
						continue
					print('distance api:', distance_api)
					if distance_api > 0:
						distance = abs(220 * distance_api / 360)
					elif distance_api < 0:
						distance = abs(abs(220 * (360 + distance_api) / 360))
					else:
						continue
					print('current distance:', distance)
					partHead = math.ceil(distance * 0.8)
					partTail = distance - partHead
					slider_element = self.browser.find_element(By.XPATH, '//div[@class="vcode-spin-button"]/p')
					ActionChains(self.browser).click_and_hold(on_element=slider_element).perform()
					ActionChains(self.browser).move_by_offset(xoffset=partHead, yoffset=0).perform()
					tracks = self.get_track(partTail)
					for s in tracks:
						ActionChains(self.browser).move_by_offset(xoffset=s, yoffset=0).perform()
					time.sleep(0.3)
					ActionChains(self.browser).release().perform()
					time.sleep(random.uniform(3, 5))
					if str(self.browser.page_source).find("百度安全验证") >= 0:
						continue
					else:
						return True
			
			# data_node = self.browser.find_element(By.CLASS_NAME, '//*[@id="tsn_inner"]/div[2]/span')
			time.sleep(2)
			data_node = self.browser.find_element(By.CLASS_NAME, "hint_PIwZX")
			print('===================')
			html_text = data_node.get_attribute("outerHTML")
			group_data = re.search('约(.*?)个', html_text)
			data = group_data.group(1).replace(',', '')
			with open('data.txt', 'a+', encoding='utf-8') as fp:
				info = f'{key_word}:               {data}\n'
				fp.write(info)
			with open('./history.txt', 'a+', 'utf-8') as hisFp:
				hisFp.write(f'{key_word}')
			self.history_list.append(f'{key_word}\n')
			print('当前爬取完成')
			return True
		except Exception as e:
			print(f'获取{key_word} 信息出错了, {e}')
			return False
	
	def get_track(self, distance):
		'''
		根据偏移量distance获取移动轨迹
		返回:
			移动轨迹
		'''
		track = []  # 移动轨迹
		current = 0  # 当前位移
		mid = distance * 2 / 3  # 减速阈值
		t = 0.2  # 计算间隔
		v = 0  # 初速度
		
		while current < distance:
			if current < mid:
				a = random.randint(30, 40)  # 加速度为正
			else:
				a = -random.randint(40, 80)  # 加速度为负
			
			v0 = v  # 初速度v0
			
			v = v0 + a * t  # 当前速度v = v0 + at
			# 移动距离x = v0t + 1/2 * a * t^2
			move = v0 * t + 1 / 2 * a * t * t
			current += move  # 当前位移
			track.append(round(move))  # 加入轨迹
		rest = sum(track) - distance
		while rest > 0:
			if rest > 3:
				max = 3
			else:
				max = rest
			move = -random.randint(1, max)
			track.append(round(move))
			rest += move
			if rest <= 2:
				move = -rest
				track.append(round(move))
				break
		return track
	
	def run(self):
			self.read_text()
			self.loop_get_info()
	
	def base64_api(self):
		with open('./rotation_image.png', 'rb') as fp:
			return base64.b64encode(fp.read())


if __name__ == '__main__':
	get_info = getInfo()
	get_info.run()
