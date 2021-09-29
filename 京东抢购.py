import requests
import urllib3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Spider:
	def __init__(self):
		
		self.base_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=100026667904&callback=jQuery321594&_=1632799712356'
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		data = self.return_requests_data(self.base_url)
		print(data.content)
	
	
	def login_jd(self):
		username = '13981'
		'//*[@id="loginname"]'
		
	
	def return_requests_data(self, param_url):
		"""
			requests 请求工具，最大请求数20次
			param_url : 需要请求的单个地址，
		"""
		retry_times = 20
		retry_count = 0
		for i in range(retry_times):
			retry_count += 1
			try:
				if retry_count > 1:
					print(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
					headers = {
						'Cookie': 'wlfstk_smdl=7q7nqrgfqeowf3mbegnqbdjp4nkx7ocf; __jda=122270672.16327984902471486592763.1632798490.1632798490.1632798490.1; __jdb=122270672.5.16327984902471486592763|1.1632798490; __jdc=122270672; __jdv=122270672|direct|-|none|-|1632798490247; __jdu=16327984902471486592763; TrackID=1YLEJhL536-c_G4LdsfwQcMjyLw4uRvvMRtgzu7s-EG6hTT2QsRqQfT8KLe0tQvrai9jRgTV48bqgSMvx8k_P4JzwiEoXwSFVD5srwOyAUfdXPnLW_gH-wNIRMVtEjacV; thor=18BE94A4F8C582B38FAF0E2E4F0C6B429152310AC4A1331B5E25CAF9F39670D244C464F57C5FA03D0E8D19F5A088FD5BF6D889D60017506B45FCCFF1D905ED3F0793C979171BE97F74EE537A684250E642064A51A0BBD3F3E4F244C97EF1779B48F0D2C0C85979777B73D20DEE5E3D8BBD699BDCF10CCED901F11204F17885AA3DBC89DE808D2584377AD7936064B7309F028EB2F2F9740DC7598A3A25CF885B; pinId=5CADqdUu64pPqdJYBa7QOrV9-x-f3wj7; pin=jd_57ae8b978ed5c; unick=jd_57ae8b978ed5c; ceshi3.com=103; _tp=5Uwu%2BC8%2BptKyLDGPiVnpgiPExVyDHqGw3dDDOAy8bx4%3D; _pst=jd_57ae8b978ed5c; areaId=22; ipLoc-djd=22-1930-49324-0; 3AB9D23F7A4B3C9B=S34BCKFDV2KG4I7F6IGNA4P6QVHPDSQIKJBVNCCPHBM5G2MRMJDDHCJDTD24MNOXGWPVE5HXBMOVGW2YPOFAWPVJLE',
						'Host':'home.jd.com',
						'Sec-Fetch-Dest': 'script',
						'Sec-Fetch-Mode': 'no-cors',
						'Sec-Fetch-Site': 'same-site',
						'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
						'Connection': 'keep-alive',
						'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
						'Referer':'https://home.jd.com/'
					}
					
				http_res = requests.get(param_url, headers=headers, stream=True, verify=False, timeout=10)
				print(http_res.text)
				return http_res
			except Exception as e:
				if retry_count >= retry_times:
					raise Exception(f'{param_url},请求失败，原因{e}')
				else:
					continue


Spider()