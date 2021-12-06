"""
1、模拟登录，获取一级url
2、获取二级url列表
3、发送请求，获取页面内容，
4、param_page解析页面
5、存储数据
"""
import os
import time
import random

import requests
import xlwt

import urllib3
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

base_url = 'https://www.tmall.com/'
KEY_WORD = input('请输入你要抓取的商品')
# KEY_WORD = '显示器'


class spider_tmall():

	def __init__(self):
		# xml文件保存路径
		self.file_save_path = 'C:\\Users\\Administrator\\Desktop\\Python\\xml_download\\Spider_xml\\{}'
		self.file_path = os.path.realpath('./available_ip.txt')  # 可用的ip池
		# 无界面
		# options = Options()
		# options.add_argument('--headless')
		# 为火狐浏览器设置代理ip
		# 1、创建代理池
		self.proxy_http_pool = []
		proxy_dic = self.random_host_port()
		print(proxy_dic)
		# 2、 设置代理ip
		self.profile = self.update_firfox_proxy(proxy_dic)
		self.browser = webdriver.Firefox(self.profile)
		# 设置浏览器窗口大小
		self.browser.set_window_size(1200, 800)
		# 设置js加载等待时间
		self.wait = WebDriverWait(self.browser, 5)

		self.headers = {
			'User-Agent': UserAgent().random
		}
		# 取消告警
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


	def random_host_port(self):
		with open(self.file_path, 'r') as fp:
			data = fp.readlines()
			for i in data:
				ip_data = i.split('_')[1]
				port_data = i.split('_')[2].replace('\n', '')
				proxy_http_key = f'{ip_data}:{port_data}'
				self.proxy_http_pool.append(proxy_http_key)
		random_proxy = random.sample(self.proxy_http_pool, 1)
		host = random_proxy[0].split(':')[0]
		port = random_proxy[0].split(':')[1]
		proxy = {
			'host': host,
			'port': int(port)
		}
		return proxy

	def update_firfox_proxy(self, proxy_dict):
		profile = webdriver.FirefoxProfile()
		profile.set_preference('network.proxy.type', 1)
		profile.set_preference('network.proxy.http', proxy_dict['host'])
		profile.set_preference('network.proxy.http_port', proxy_dict['port'])
		# 为https设置的
		# profile.set_preference('network.proxy.ssl_transfer', proxy['host'])
		# profile.set_preference('network.proxy.ssl_port', proxy['port'])
		profile.update_preferences()
		return profile


	def login(self):
		"""
		模拟登录，get一级url
		:return:
		"""
		self.browser.get(base_url)
		self.browser.find_element_by_xpath('//*[@id="login-info"]/a[1]').click()
		# 浏览器中的节点xpath表达式没有问题，但是就是定位不到具体元素，是因为有自定义的元素，
		#  需要为浏览器对象指定出自定义的元素，就会找到并填入值，
		# TODO 切入iframe之后一定要切出来，且要预留睡眠等待时间，
		self.browser.switch_to.frame(self.browser.find_element_by_xpath('//iframe[@id="J_loginIframe"]'))
		self.browser.find_element_by_xpath("//*[@id='fm-login-id']").send_keys('18419360851')
		self.browser.find_element_by_xpath("//*[@id='fm-login-password']").send_keys('10793300d')
		self.browser.find_element_by_xpath('//button[@class="fm-button fm-submit password-login"]').click()
		self.browser.switch_to.default_content()
		wait_time = 5
		time.sleep(wait_time)
		self.browser.find_element_by_xpath('//*[@id="mq"]').send_keys(KEY_WORD)
		self.browser.find_element_by_xpath('//button[@type="submit"]').click()
		currnt_url = self.browser.current_url
		return currnt_url

	def get_sub_url(self, task_url):
		sub_url_list = []
		pre_url = task_url.split('?')[0]
		after_url = task_url.split('?')[1]
		key_num = 0
		for count in range(80):
			key_num += 60
			sub_url = pre_url + '?' + 's=' + str(key_num) + '&' + after_url
			sub_url_list.append(sub_url)
		return sub_url_list


	def get_sub_sub_url(self, sub_url_list_params):
		link_list = []
		total_num = 0
		page_count = 2
		for url in sub_url_list_params[page_count:5]:
			print(url)
			page_count += 1
			time.sleep(5)
			try:
				self.browser.get(url)
				for count in range(60):
					count += 1
					time.sleep(0.5)
					total_num += 1
					data = self.browser.find_element_by_xpath(f'/html/body/div[1]/div/div[3]/div/div[7]/div[{count}]/div/div[1]/a')
					href = data.get_attribute('href')
					link_list.append(href)
					print(f'当前第{total_num}链接已加入：{href}')
			except Exception as e:
				print(e)
				continue
		return link_list

	def get_link_info(self, links_list):
		"""
		获取想要的信息
		:param links_list:
		:return: data， field
		"""
		data = []
		num_count = 0
		field = ['序号', '商品名', '价格', '销量', '运费']
		# links_list = ['https://detail.tmall.com/item.htm?id=624096625292&skuId=4419391317503&areaId=510100&user_id=3899867883&cat_id=2&is_b=1&rn=35a7af0e4f2b1d512658711a0aee3a44',
		# 			 'https://detail.tmall.com/item.htm?id=613333353044&skuId=4611686631760740948&areaId=510100&user_id=2255956124&cat_id=2&is_b=1&rn=35a7af0e4f2b1d512658711a0aee3a44']
		for link in links_list:
			try:
				print('开始get link')
				self.browser.get(link)
				print('开始等待')
				times = 0
				for i in range(5):
					times += 1
					time.sleep(1)
					print(f'等待时间{times}')
				print('等待结束')
				name = self.browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[1]/div/div[1]/h1').text
				print('商品名' ,name)
				price = self.browser.find_element_by_css_selector('.tm-price').text
				print('价格' ,price)
				try:
					selery = self.browser.find_element_by_class_name('tm-count').text
				except Exception as e:
					selery = '默认值'
				print('销量' ,selery)
				try:
					freight = self.browser.find_element_by_xpath('//div[@id="J_PostageToggleCont"]/p/span').text
				except Exception as e:
					freight = '默认值：0'
				print('运费', freight)
				try:
					src_element = self.browser.find_element_by_xpath('//*[@id="J_ImgBooth"]')
					src = src_element.get_attribute('src')
				except Exception as e:
					print(f'图片src获取失败，原因为{e}')
					src = None
				print('图片', src)
				num_count += 1
				if src is not None:
					self.picture_save(src, num_count)
				else:
					print('第{num_count} 图片获取失败')
				sub_data = [num_count, name, price, selery, freight]
				data.append(sub_data)
				print(f'===========第{num_count}个抓取完成===========')
			except Exception as e:
				print(e)
				continue
		print(data, '\n', field)
		return data, field


	def save_xml(self, data, fields):
		"""
		保存xml表格
		:param data:
		:param fields:
		:return:
		"""
		print('进来了')
		work = xlwt.Workbook(encoding='utf-8')
		sheet = work.add_sheet(str(KEY_WORD))
		for num in range(len(fields)):
			sheet.write(0, num, fields[num])

		for row in range(1, len(data) + 1):
			for col in range(len(fields)):
				lists_res = data[row - 1][col]
				print(lists_res)
				sheet.write(row, col, lists_res)
		file_name = str(KEY_WORD) + '.xml'
		file_path = self.file_save_path.format(file_name)
		if os.path.exists(file_path):
			os.remove(file_path)
		work.save(file_path)
		print('保存成功')


	def picture_save(self, src, count):
		print(f'当前的请求src为{src}')
		data = requests.get(url=src, verify=False).content
		picture_base_path = self.file_save_path.format(KEY_WORD)
		if not os.path.exists(picture_base_path):
			os.makedirs(picture_base_path)
		picture_file_path = picture_base_path + '\\' + str(count) + '.jpg'
		try:
			with open(picture_file_path, 'wb') as fp:
				fp.write(data)
			print(f'第{count}个图片{src}保存完成')
		except Exception as e:
			print(f'第{count}个图片保存失败，原因为{e}')


if __name__ == '__main__':
	tmall = spider_tmall()
	current_url = tmall.login()
	sub_url = tmall.get_sub_url(current_url)
	link_list = tmall.get_sub_sub_url(sub_url)
	data_info, fileds_res = tmall.get_link_info(link_list)
	tmall.save_xml(data_info, fileds_res)
