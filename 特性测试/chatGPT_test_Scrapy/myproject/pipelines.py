# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import json


class MyPipeline:
	def __init__(self):
		self.file = open('data.json', 'w+', encoding='utf-8')
	
	def process_item(self, item, spider):
		print("这是开始存储数据了")
		json.dump(item, self.file)
		self.file.write("\n")
		return item
	
	def open_spider(self, spider):
		print("这是爬虫启动了")
	
	def close_spider(self, spider):
		self.file.close()
