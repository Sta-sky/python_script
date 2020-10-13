import os
import time
import urllib.request
from lxml import etree
import requests


base_url = 'https://www.kuaidaili.com/free/inha/{}/'
page_num = 0
count_page = 100
ele_num = 15
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
		print(url, 'current url')
		res = urllib.request.urlopen(url)
		html_data = res.read().decode('utf-8')
		# print(html_data)
		element_boj = etree.HTML(html_data)
		for i in range(ele_num):
			param_ele = i + 1
			ip = element_boj.xpath(f'/html/body/div/div[4]/div[2]/div/div[2]/table/tbody/tr[{param_ele}]/td[1]/text()')
			port = element_boj.xpath(f'/html/body/div/div[4]/div[2]/div/div[2]/table/tbody/tr[{param_ele}]/td[2]/text()')
			count += 1
			print(count, '30行')
			print(f'当前为第{count}个ip, ip地址为{ip}，端口为{port}')
			data = str(count) + '_' + ip[0] + '_' + port[0] + '_' + '\n'
			with open(file_path, 'a+') as fp:
				fp.write(data)

# get_ip_pool()

avilabale_ip_file = os.path.realpath('./available_ip.txt')
if not os.path.exists(avilabale_ip_file):
	with open(avilabale_ip_file, 'w') as fp:
		pass

def test_ip():
	print(file_path)
	with open(file_path, 'r') as fp:
		data_list = fp.readlines()
		for data in data_list:
			data_ip_list = data.split('_')
			ip_data = data_ip_list[1]
			port_data = data_ip_list[2]
			count = data_ip_list[0]
			server = ip_data + ':' + port_data
			time.sleep(1)
			test_urls = 'https://list.tmall.com/search_product.htm?s=2340&q=%E6%88%90%E6%9E%9C&type=p&style=&cat=all&vmarket='
			try:
				res = requests.get(url=test_urls, proxies={'http': server}, timeout=2)
				print(res.status_code)
				print(res)
				print(f'第{count}个ip{ip_data}链接测试成功')
				avilabale_data =str(count) + '_' + ip_data + '_' + port_data + '\n'
				with open(avilabale_ip_file, 'a+') as fp:
					fp.write(avilabale_data)
					print(f'第{count}个ip，port{ip_data, port_data}写入完成')
				continue
			except Exception as e:
				print(f'第{count}个ip{ip_data}链接测试失败')
test_ip()
