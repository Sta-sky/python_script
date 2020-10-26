import os
import re
import time
import queue
import urllib3
import random
import requests
from lxml import etree
from log_util import Log
from Crypto.Cipher import AES
from threading import Thread, Lock

logger = Log('lao_liu_1').print_info()


class SpiderVideo(object):
	def __init__(self):
		super(SpiderVideo, self).__init__()
		self.url = 'https://ggcc01.com/archives/category/jingpin/page/{}'
		self.start_page = 50
		# 最大page为4
		self.end_page = 51
		# 消除警告
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		
		# 文件存储路径
		self.file_save_base_path = 'G:\\MAT\\video\\kele\\{}.mp4'
		self.new_save_path = 'H:\\ITM\\new_video\\{}.mp4'
		# 控制文件大小，大于700个数量的ts，就不去下载
		self.ts_list_size = 3000
		self.url_queue = queue.Queue(1000)
	
	def get_video_id(self):
		re_href_list = []
		href_count = 0
		try:
			for page in range(self.start_page, self.end_page):
				request_res = self.return_requests_data(self.url.format(page))
				if not request_res:
					logger.error('==主页面==地址，请求失败了， 开始请求下个页面')
					continue
				else:
					html_data = request_res.text
					element = etree.HTML(html_data)
					href_data = element.xpath('//a/@href')
					re_href_list, href_count = self.get_href_lilst(
						href_data, href_count, re_href_list)
				time.sleep(1)
			return re_href_list
		except Exception as e:
			logger.error(f'id列表获取失败，失败原因为{e}')
		finally:
			return re_href_list
	
	def get_href_lilst(self, href_data, href_count, href_list):
		totle = (self.end_page - self.start_page) * 12
		for href in href_data:
			if href.split('.')[-1] == 'html':
				if href in href_list:
					continue
				href_list.append(href)
				href_count += 1
				logger.info(f'总共{totle}个href，正在获取第{href_count}个，href为{href}')
		return href_list, href_count
	
	def get_m3u8_save_video(self, link, th_name):
		
		request_res = self.return_requests_data(link)
		if not request_res:
			raise Exception('子页面请求失败')
		else:
			page_data = request_res.text
			m3u8_re = '(.*)\.m3u8'
			src_path = re.findall(m3u8_re, page_data)
			# logger.info('文件中匹配出的没有过滤的m3u8地址列表', src_path)
			if not src_path:
				raise Exception('匹配出的m3u8列表为空')
			m3u8_file_res_url = src_path[2].split(': ')[1].split('"')[1]
			ele = etree.HTML(page_data)
			try:
				file_name = ele.xpath('//title/text()')[0]
			except Exception:
				file_name = random.randint(1, 100)
				logger.info(f'没有匹配出name，当前的name为随机数 ： {file_name}')
			save_file_path = self.file_save_base_path.format(file_name)
			new_save_path = self.new_save_path.format(file_name)
			if os.path.exists(save_file_path) or os.path.exists(new_save_path):
				raise Exception(f'-------文件已经存在-------,name{file_name}')
			logger.info(f'文件不存在，由线程{th_name}开始下载，保存路径为：{new_save_path}')
			request_res = self.handle_m3u8_ts_key(m3u8_file_res_url)
			if request_res:
				re_ts_list, re_ts_base_url, re_key_base_url = request_res
				key_val, ts_list_url = self.request_ts_key_url_list(
					re_ts_list, re_ts_base_url, re_key_base_url)
				ts_length = len(ts_list_url)
				if ts_length > self.ts_list_size:
					raise Exception(f'文件ts数量为{ts_length}个,大于{self.ts_list_size}个ts')
				return key_val, ts_list_url, new_save_path, file_name,
			else:
				raise Exception(request_res)
	
	def handle_m3u8_ts_key(self, m3u8_file_res_url):
		# 从页面上匹配的m3u8地址没有https：前缀，这种情况是在有需要key解密的ts，
		judge_http = m3u8_file_res_url.split('/')
		if 'https:' not in judge_http and 'http:' not in judge_http:
			m3u8_file_res_url = 'https:' + m3u8_file_res_url
		base_url_key_ts = m3u8_file_res_url.replace('index', '')
		# logger.info('文件中的m3u8_url:', m3u8_file_res_url)
		# 通过页面中取得的m3u8地址，拼接出携带域名为止的url，用于后面拼接真正的m3u8 url
		domain_base_url = m3u8_file_res_url.split('com')[0] + 'com'
		
		# 用页面中的m3u8地址 获取文件，看是否有两个m3u8 url
		false_m3u_url = m3u8_file_res_url + '.m3u8'
		false_m3u8_file = self.return_requests_data(false_m3u_url)
		if not false_m3u8_file:
			raise Exception('m3u8请求失败')
		else:
			false_m3u8_file = false_m3u8_file.text
			key_val = self.match_key(false_m3u8_file)
			if key_val:
				key_base_url = domain_base_url + key_val
			else:
				key_base_url = key_val
			m3u8_re = '(.*)\.m3u8'
			true_link = re.findall(m3u8_re, false_m3u8_file)
			# logger.info('匹配出的m3u8链接列表为：', true_link)
			
			# 如果是两个m3u8 url，则拼接真实的m3u8 url，获取ts文件，
			# 如果不是，则说明只有一个m3u8 url，继续使用上面的false_m3u_url获取的数据匹配ts文件
			if true_link:
				# 判断匹配出的真实链接是否携带https/http 头
				if 'https:' in true_link[0].split('/') or 'http:' not in true_link[0].split('/'):
					true_m3u8_url = domain_base_url + true_link[0] + '.m3u8'
				else:
					true_m3u8_url = true_link[0]
				# logger.info('真实的m3u8链接：', true_m3u8_url)
				request_res = self.return_requests_data(true_m3u8_url)
				if not request_res:
					raise Exception('m3u8请求失败')
				else:
					ts_url_data = request_res.text
					true_key_val = self.match_key(ts_url_data)
					if true_key_val:
						key_base_url = domain_base_url + true_key_val
					# logger.info(f'加密了，第二次请求m3u8匹配的key，拼接的key_url{key_base_url}')
					ts_base_url = domain_base_url
			# 如果为两个m3u8跳转地址， 根据请求返回的m3u8地址，找规律，拼接出能返回ts文件的m3u8地址
			else:
				ts_url_data = false_m3u8_file
				ts_base_url = base_url_key_ts
			# 匹配出ts url的后缀
			ts_re = '(.*)\.ts'
			ts_list = re.findall(ts_re, ts_url_data)
			return ts_list, ts_base_url, key_base_url
	
	def match_key(self, request_data_file):
		key_re = '(.*)\.key'
		key_list = re.findall(key_re, request_data_file)
		# logger.info(f'文件中匹配出的key_list:{key_list}')
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
			ts_url_list.append(res_ts_url)
		if key_url_base:
			key_url = key_url_base + '.key'
			# logger.info(f'文件需要解密，密钥url为{key_url}')
			key_banery = self.return_requests_data(key_url)
			key_banerys = key_banery.content
			key_banery.close()
		else:
			# logger.info('文件不需要解密')
			key_banerys = None
		return key_banerys, ts_url_list
	
	def decrypt_save_ts(self, key, ts_urls, new_save_path, file_name,
	                    down_th_name):
		"""功能函数2:解密,保存"""
		
		# decrypt方法的参数需要为16的倍数，如果不是，需要在后面补二进制"0"
		total_size = len(ts_urls)
		down_num = 0
		for ts_url in ts_urls:
			down_num += 1
			progrees = float('%.2f' % (down_num / total_size)) * 100
			logger.info('ts数量{}，当前下载第{}个，已经下载{}%,'.format(total_size, down_num,
			                                              progrees))
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
			logger.info(f"{down_th_name}=下载：{file_name[0:15]} 影片的ts" + ts_name)
			time.sleep(1)
			request_res = self.return_requests_data(ts_url)
			if not request_res:
				logger.info(f'ts请求超过20次，删除文件之后,再次将url加入列队，开始请求下一个ts：{ts_url}')
				os.remove(new_save_path)
				logger.info(f'删除成功，路径为{new_save_path}')
				return False
			else:
				try:
					ts_data = request_res.content
					# 密文长度不为16的倍数，则添加b"0"直到长度为16的倍数
					while len(ts_data) % 16 != 0:
						ts_data += b"0"
					# 此种情况下，没有使用key加密，可以直接写入文件，
					# 判断是否加密，可直接下载一个ts文件，如果正常播放，表示没有加密
					if not key or key == '':
						with open(new_save_path, "ab") as file:
							file.write(ts_data)
					# logger.info(f'{ts_name}已下载写入')
					else:
						with open(new_save_path, "ab") as file:
							file.write(sprytor.decrypt(ts_data))
				# logger.info(f'{ts_name}已下载写入')
				except Exception as e:
					logger.error(f'保存ts文件失败，原因为{e}')
					return False
		return True
	
	def return_requests_data(self, param_url):
		retry_times = 20
		retry_count = 0
		for i in range(retry_times):
			retry_count += 1
			try:
				if retry_count > 1:
					logger.info(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
				http_res = requests.get(url=param_url, verify=False, timeout=5)
				return http_res
			except Exception as e:
				if retry_count >= retry_times:
					logger.error(f'{param_url},请求失败，原因{e}')
					return False
				else:
					continue
	
	def product_queue(self):
		hrefs_list = self.get_video_id()
		for url in hrefs_list:
			self.url_queue.put(url)
		logger.info(f'获取的url队列总大小{self.url_queue.qsize()}')
		return self.url_queue


class MySpiderThread(Thread, SpiderVideo):
	def __init__(self, thread_name, uri_queue, totle_video):
		super().__init__()
		self.setName(thread_name)
		self.lock = Lock()
		self.name = self.getName()
		self.alive_status = self.is_alive()
		self.totle_video = totle_video + 1
		self.video = SpiderVideo()
		self.queue_url = uri_queue
	
	def run(self):
		while True:
			# 每个线程，先获取当前的队列中的总数
			current_queue_num = self.queue_url.qsize()
			# 通过传入的总的队列数，减去当前的队列数，为当前正在下载的第几个
			current_video_num = self.totle_video - current_queue_num
			if self.queue_url.empty():
				logger.info(f'队列为空，当前线程{self.name}下载完成，退出，当前队列中的个数为{current_queue_num}')
				break
			else:
				link = self.queue_url.get()
				self.totle_video -= 1
				logger.info(f'共{self.totle_video}个视频；由=={self.name}==开始下载第{current_video_num}个视频')
				try:
					request_res = self.video.get_m3u8_save_video(link, self.name)
				except Exception as e:
					logger.info(e)
					continue
				key, ts_urls, new_save_path, file_name = request_res
				down_video_res = self.video.decrypt_save_ts(
					key, ts_urls, new_save_path, file_name, self.name)
				if not down_video_res:
					self.queue_url.put(link)
					logger.info(f'保存ts阶段失败，再次加入队列{link}')
				else:
					continue


if __name__ == '__main__':
	"""
	多线程下载视频
	"""
	th_num = 30
	video = SpiderVideo()
	queue_url = video.product_queue()
	totle_video = queue_url.qsize()
	th_list = []
	for num in range(th_num):
		th_name = '___党的线程' + str(num) + '____'
		my_th = MySpiderThread(th_name, queue_url, totle_video)
		th_list.append(my_th)
	for j in th_list:
		j.start()
	for i in th_list:
		i.join()
		logger.info(f'线程{i.name}回收完成')

