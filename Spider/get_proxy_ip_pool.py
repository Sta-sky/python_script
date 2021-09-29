import asyncio
import os
import time
import urllib.request
from lxml import etree
import requests
from threading import Thread
import queue


base_url = 'https://www.kuaidaili.com/free/inha/{}/'
page_num = 0
count_page = 30
ele_num = 15

# 爬取的所有代理ip保存地址
file_path = os.path.realpath('./ip_pool.txt')
if not os.path.exists(file_path):
	with open(file_path, 'w') as p:
		pass


def get_ip_pool():
	count = 0
	for num in range(count_page):
		num += 1
		time.sleep(2)
		url = base_url.format(str(num))
		res = urllib.request.urlopen(url)
		html_data = res.read().decode('utf-8')
		element_boj = etree.HTML(html_data)
		for i in range(ele_num):
			param_ele = i + 1
			ip = element_boj.xpath(f'/html/body/div/div[4]/div[2]/div/div[2]/table/tbody/tr[{param_ele}]/td[1]/text()')
			port = element_boj.xpath(f'/html/body/div/div[4]/div[2]/div/div[2]/table/tbody/tr[{param_ele}]/td[2]/text()')
			count += 1
			print(f'当前为第{count}个ip, ip地址为{ip}，端口为{port}')
			data = str(count) + '_' + ip[0] + '_' + port[0] + '_' + '\n'
			with open(file_path, 'a+') as fp:
				fp.write(data)


# get_ip_pool()

'-------------------------------------------------------------------------------------------------------------------'
# 可用的代理ip保存地址
avilabale_ip_file = os.path.realpath('./available_ip.txt')
if not os.path.exists(avilabale_ip_file):
	with open(avilabale_ip_file, 'w') as fp:
		pass


# async 异步测试ip
async def test(data):
	try:
		data_ip_list = data.split('_')
		ip_data = data_ip_list[1]
		port_data = data_ip_list[2]
		count = data_ip_list[0]
		server = ip_data + ':' + port_data
		test_urls = 'http://www.xbiquge.la'
		res = requests.get(url=test_urls, proxies={'http': server}, timeout=2)
		print(f'第{count}个ip{ip_data}链接测试成功')
		avilabale_data = str(count) + '_' + ip_data + '_' + port_data + '\n'
		with open(avilabale_ip_file, 'a+') as fp:
			fp.write(avilabale_data)
			print(f'第{count}个ip，port{ip_data, port_data}写入完成')
	except Exception as e:
		print(f'第{count}个ip{ip_data}链接测试失败')


async def test_ip():
	with open(file_path, 'r') as fp:
		data_list = fp.readlines()

		task_list = [
			test(data) for data in data_list
		]
		print(f"总共{len(task_list)}")
		response = await asyncio.wait(task_list)
		return response


task_obj = [test_ip()]
done, padding = asyncio.run(asyncio.wait(task_obj))
print(padding)
print(done)


'-------------------------------------------------------------------------------------------------------------------'


# 多线程测试ip
def test1(data):
	try:
		data_ip_list = data.split('_')
		ip_data = data_ip_list[1]
		port_data = data_ip_list[2]
		count = data_ip_list[0]
		server = ip_data + ':' + port_data
		test_urls = 'http://www.xbiquge.la'
		requests.get(url=test_urls, proxies={'http': server}, timeout=2)
		print(f'第{count}个ip{ip_data}链接测试成功')
		avilabale_data = str(count) + '_' + ip_data + '_' + port_data + '\n'
		with open(avilabale_ip_file, 'a+') as fp:
			fp.write(avilabale_data)
			print(f'第{count}个ip，port{ip_data, port_data}写入完成')
	except Exception as e:
		print(f'第{count}个ip{ip_data}链接测试失败')


class CustomThead(Thread):
	def __init__(self, queue_pool):
		self.queues = queue_pool
		super().__init__()

	def run(self):
		queue_total = self.queues
		while True:
			if queue_total.empty():
				print('队列为空，退出')
				break
			else:
				ip_data = queue_total.get()
				test1(ip_data)
		return None


def test_ip():
	with open(file_path, 'r') as fp:
		data_list = fp.readlines()
		queue_pool = queue.Queue()
		for data in data_list:
			queue_pool.put(data)
	print(f"总共{queue_pool.qsize()}")
	th_list = []
	for i in range(30):
		th_obj = CustomThead(queue_pool)
		th_list.append(th_obj)
	for i in th_list:
		i.start()
	for j in th_list:
		j.join()

test_ip()


