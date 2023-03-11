import scrapy
import json


class MySpider(scrapy.Spider):
	name = 'myspider'
	start_urls = ['https://www.baidu.com']
	print("这是抓取数据了")
	
	def parse(self, response):
		print("这是开始  解析  数据了")
		for link in response.xpath('//a/@href'):
			yield {
				'url': link.get()
			}
