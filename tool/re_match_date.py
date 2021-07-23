import re
from datetime import datetime


def re_date_parse(content):
	""" 匹配字符串中的各种日期格式
		
		content: 字符串
		return：返回所有匹配的日期列表
	"""
	pattern = re.compile(r'\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日')  # 定义匹配模式
	pattern_data = re.findall(pattern, content)
	list_form = ['%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%d', '%Y年%m月%d日']
	date = []
	for pattern_item in pattern_data:
		for item in list_form:
			result = date_format(pattern_item, item)
			if result:
				date.append(result.strftime("%Y-%m-%d"))
	return date

def date_format(item, format_item):
	try:
		date = datetime.strptime(item, format_item)
		return date
	except Exception as e:
		return False
