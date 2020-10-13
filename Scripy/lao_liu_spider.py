import os
import random
import re
import time

import requests
from Crypto.Cipher import AES
from selenium import webdriver
import urllib3
from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options


class Spider_Video():
	def __init__(self):
		self.url = 'https://ggcc01.com/page/{}'
		self.tow_url = 'https://ggcc01.com/archives/{}.html'

		self.file_path = 'C:\\Users\\Administrator\\Desktop\\Python\\opencv\\scripy\\available_ip.txt'
		self.proxy_http_pool = []
		proxy_dic = self.random_host_port()
		print(proxy_dic)
		self.profile = self.update_firfox_proxy(proxy_dic)

		options = Options()
		options.add_argument('--headless')
		self.browser = webdriver.Firefox(options=options)

		# 0 -- 30 查缺补漏
		self.start_page = 150
		# 最大page为4
		self.end_page = 180
		# 消除警告
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

		# 从此处可以用切片的方式选择从所有视频列表中第几个开始抓取，video.get_m3u8_url(lists_id[:3], names_list[:3]) 从第三个开始
		self.video_num = 12

		self.name = None
		# 文件存储路径
		self.file_save_base_path = 'G:\\MAT\\video\\kele\\{}.mp4'
		self.file_save_path = None
		# 控制文件大小，大于700个数量的ts，就不去下载
		self.ts_list_size = 1500

		self.host = None
		self.referer = 'https://www.kele15.com/video/video_play.html?video_id={}'
		self.agent = UserAgent(verify_ssl=False).random
		self.headers = {
			'User-Agent': self.agent,
			'Origin': 'https://www.kele15.com',
			'Referer': self.referer,
			'Connection': 'close'
		}

	def update_firfox_proxy(self, proxy_dict):
		profile = webdriver.FirefoxProfile()
		profile.set_preference('network.proxy.type', 1)
		profile.set_preference('network.proxy.http', proxy_dict['host'])
		profile.set_preference('network.proxy.http_port', proxy_dict['port'])
		# 为https设置的
		# profile.set_preference('network.proxy.ssl', proxy['host'])
		# profile.set_preference('network.proxy.ssl_port', proxy['port'])
		profile.update_preferences()
		return profile

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

	def get_video_id(self):
		id_list = []
		name_list = []
		id_count = 0
		try:
			for num in range(self.start_page, self.end_page):
				num += 1
				url = self.url.format(num)
				self.browser.get(url=url)
				for ele_num in range(9):
					ele_num += 1
					id_count += 1
					href_ele = self.browser.find_element_by_xpath(f'/html/body/div[6]/div/div[2]/div/div[{ele_num}]/a')
					href = href_ele.get_attribute('href')
					id_num = href.split('/')[4].split('.')[0]
					video_name = href_ele.get_attribute('title')
					if '小可爱' in video_name or '大秀' in video_name or '直播' in video:
						print('又是小可爱直播，等待下载下一个')
						continue
					name_list.append(video_name)
					print(f'当前的为第{id_count}个视频，id为：{id_num}, 影片名称{video_name}')
					id_list.append(id_num)
			print(f'所有id获取完毕')
			return id_list, name_list
		except Exception as e:
			print(f'id列表获取失败，失败原因为{e}')
		finally:
			return id_list, name_list

	def get_m3u8_save_video(self, id_lists, video_name_list):
		try:
			if self.video_num > (self.end_page - self.start_page) * 9:
				print(f'第{self.end_page + 1}页全部下载结束')
			else:
				length = len(id_lists)
				time.sleep(5)
				while self.video_num < length:
					self.video_num += 1
					print(f'===============总共{length}个影片，正在下载第{self.video_num}个====================')
					id = id_lists[self.video_num - 1]
					self.name = video_name_list[self.video_num - 1]
					save_file_path = self.file_save_base_path.format(self.name)
					if os.path.exists(save_file_path):
						print(f'文件已经存在,name:{self.name},')
						print('------------等待下载下个视频-------------')
						continue
					self.file_save_path = save_file_path
					print(f'文件不存在，开始下载，保存路径为：{self.file_save_path}')
					tow_url = self.tow_url.format(id)
					print('当前所在的页面', tow_url)
					page_data = self.return_requests_data(tow_url)
					data = page_data.text
					page_data.close()
					key_val, ts_list_url = self.get_m3u8_key_ts_url(data)
					ts_length = len(ts_list_url)
					if ts_length > self.ts_list_size:
						print(f'文件ts数量为{ts_length}个，大于1500个ts，跳过，等待下载下一个')
						continue
					self.decrypt_save_ts(key_val, ts_list_url)
				else:
					print('所有文件下载完成')
		except Exception as e:
			print(f'获取数据失败，失败原因为{e}')

	def get_m3u8_key_ts_url(self, page_data):
		""" 函数功能， 通过视频播放页面地址，获取m3u8地址，
			根据m3u8地址，请求ts文件列表

			如果有两个ts文件，则有一个是真的能返回ts文件的地址，根据另一个拼接处真实ts地址
		"""
		# 匹配出m3u8的地址
		m3u8_re = '(.*)\.m3u8'
		src_path = re.findall(m3u8_re, page_data)
		print('文件中匹配出的没有过滤的m3u8地址列表', src_path)
		m3u8_file_res_url = src_path[1].split('url')[1].split(' ')[1].replace('"', '').replace("'", '').strip()

		# 从页面上匹配的m3u8地址没有https：前缀，这种情况是在有需要key解密的ts，
		judge_http = m3u8_file_res_url.split('/')
		if 'https:' not in judge_http:
			m3u8_file_res_url = 'https:' + m3u8_file_res_url
		base_url_key_ts = m3u8_file_res_url.replace('index', '')
		print('文件中的m3u8_url:', m3u8_file_res_url)
		# 通过页面中取得的m3u8地址，拼接出携带域名为止的url，用于后面拼接真正的m3u8 url
		domain_base_url = m3u8_file_res_url.split('com')[0] + 'com'

		# 用页面中的m3u8地址 获取文件，看是否有两个m3u8 url
		false_m3u_url = m3u8_file_res_url + '.m3u8'
		false_m3u8_file = self.return_requests_data(false_m3u_url).text
		key_val = self.match_key(false_m3u8_file)
		if key_val:
			key_base_url = domain_base_url + key_val
			print(f'加密了，第一次请求m3u8匹配的key，拼接的key_url{key_base_url}')
		else:
			key_base_url = key_val
		# false_m3u8_file = response_m3u8.text
		# response_m3u8.close()
		m3u8_re = '(.*)\.m3u8'
		true_link = re.findall(m3u8_re, false_m3u8_file)
		print('匹配出的m3u8链接列表为：', true_link)

		# 如果是两个m3u8 url，则拼接真实的m3u8 url，获取ts文件，
		# 如果不是，则说明只有一个m3u8 url，继续使用上面的false_m3u_url获取的数据匹配ts文件
		if true_link:
			true_m3u8_url = domain_base_url + true_link[0] + '.m3u8'
			print('真实的m3u8链接：', true_m3u8_url)
			ts_url_data = self.return_requests_data(true_m3u8_url).text
			true_key_val = self.match_key(ts_url_data)
			if true_key_val:
				key_base_url = domain_base_url + true_key_val
				print(f'加密了，第二次请求m3u8匹配的key，拼接的key_url{key_base_url}')
			ts_base_url = domain_base_url

		# 如果为两个m3u8跳转地址， 根据请求返回的m3u8地址，找规律，拼接出能返回ts文件的m3u8地址
		else:
			ts_url_data = false_m3u8_file
			ts_base_url = base_url_key_ts
		print('ts_base_url', ts_base_url)

		# 匹配出ts url的后缀
		ts_re = '(.*)\.ts'
		ts_list = re.findall(ts_re, ts_url_data)

		key_val, ts_list_url, = self.request_ts_key_url_list(ts_list, ts_base_url, key_base_url)
		return key_val, ts_list_url


	def match_key(self, request_data_file):
		key_re = '(.*)\.key'
		key_list = re.findall(key_re, request_data_file)
		print(f'文件中匹配出的key_list:{key_list}')
		try:
			key_val = key_list[0].split('"')[1]
			return key_val
		except Exception as e:
			return None

	def request_ts_key_url_list(self, ts_lists, ts_base_url, key_url_base):
		""" 函数功能，返回解密key，ts地址"""
		ts_url_list = []
		for ts in ts_lists:
			res_ts_url = ts_base_url + str(ts) + '.ts'
			# print(138, res_ts_url)
			ts_url_list.append(res_ts_url)

		# 判断key是在文件中，还是请求地址中包含着，大于则说明不在地址中，小于则说明在
		if key_url_base:
			key_url = key_url_base + '.key'
			print(f'文件需要解密，密钥url为{key_url}')
			key_banery = self.return_requests_data(key_url)
			key_banerys = key_banery.content
			key_banery.close()

		else:
			print('文件不需要解密')
			key_banerys = None
		print(f'是否需要解密返回的key：{key_banerys}，' + '\n' + '拼接完成的ts_url地址', ts_url_list)
		return key_banerys, ts_url_list


	def decrypt_save_ts(self, key, ts_urls):
		"""功能函数2:解密,保存"""

		# decrypt方法的参数需要为16的倍数，如果不是，需要在后面补二进制"0"
		total_size = len(ts_urls)
		print(f'ts个数{total_size}')
		# print(self.headers)
		down_num = 0

		for ts_url in ts_urls:
			down_num += 1
			progrees = float('%.2f' % (down_num / total_size)) * 100
			print('ts数量{}，当前下载第{}个，已经下载{}%,'.format(total_size, down_num, progrees))
			ts_name = ts_url.split("/")[-1]  # ts文件名
			# 解密，new有三个参数，
			# 第一个是秘钥（key）的二进制数据，
			# 第二个使用下面这个就好
			# 第三个IV在m3u8文件里URI后面会给出，如果没有，可以尝试把秘钥（key）赋值给IV
			sprytor = None

			# key为None时不需要解密，
			if key:
				sprytor = AES.new(key, AES.MODE_CBC, IV=key)
			# 获取ts文件二进制数据
			print(f"正在下载：{self.name} 影片的ts" + ts_name)
			time.sleep(0.5)
			ts_data = self.return_requests_data(ts_url).content
			# 密文长度不为16的倍数，则添加b"0"直到长度为16的倍数
			while len(ts_data) % 16 != 0:
				ts_data += b"0"
			# 此种情况下，没有使用key加密，可以直接写入文件，
			# 判断是否加密，可直接下载一个ts文件，如果正常播放，表示没有加密
			if key == None or key == '':
				with open(self.file_save_path, "ab") as file:
					file.write(ts_data)
					print(f'{ts_name}已下载写入')
			else:
				with open(self.file_save_path, "ab") as file:
					file.write(sprytor.decrypt(ts_data))
					print(f'{ts_name}已下载写入')
		print(f'视频下载完成，名称为：{self.name}')

	def return_requests_data(self, param_url):
		# self.headers['User-Agent'] = self.agent
		retry_times = 20
		retry_count = 0
		for i in range(retry_times):
			retry_count += 1
			try:
				if retry_count > 1:
					print(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
				http_res = requests.get(url=param_url, verify=False, timeout=10)
				return http_res
			except Exception as e:
				if retry_count >= retry_times:
					raise Exception(f'{param_url},请求失败，原因{e}')
				else:
					continue


if __name__ == '__main__':
	video = Spider_Video()
	lists_id, names_list = video.get_video_id()
	# lists_id, names_list = [3499], ['nihao']
	video.get_m3u8_save_video(lists_id, names_list)



