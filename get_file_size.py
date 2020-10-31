import os

import xlwt

file_path = 'H:\\ITM\\new-video'

def get_size_file(file_dir):
	data_list = []
	sub_file_name = None
	file_root_path = None
	dir_path = None
	for obj in os.walk(file_dir):
		file_root_path = obj[0]
		dir_path = obj[1]
		sub_file_name = obj[2]
	print(file_root_path)
	print(dir_path)
	print(sub_file_name)

	video_num = 0
	for file_name in sub_file_name:
		judge_file_path = file_root_path + '\\' + file_name
		kb_size = os.path.getsize(judge_file_path)
		print('name：', file_name)
		print('kb.size', kb_size)
		mb_size = float('%.2f' % ((kb_size / 1024) / 1024))
		print('mb_size', mb_size)
		video_num += 1
		sub_data = [video_num , mb_size, file_name]
		data_list.append(sub_data)
		print('===============================================')
	field = ['序号', '大小 (单位：MB)', '影片名']
	save_xml(data_list, field)


def save_xml(data, fields):
	"""
	保存xml表格
	:param data:
	:param fields:
	:return:
	"""
	print('进来了')
	file_save_path = 'G:\\MAT\\video\\{}'
	work = xlwt.Workbook(encoding='utf-8')
	sheet = work.add_sheet('video')
	for num in range(len(fields)):
		sheet.write(0, num, fields[num])

	for row in range(1, len(data) + 1):
		for col in range(len(fields)):
			lists_res = data[row - 1][col]
			print(lists_res)
			sheet.write(row, col, lists_res)
	file_name = 'video-new.xml'
	file_path = file_save_path.format(file_name)
	if os.path.exists(file_path):
		os.remove(file_path)
	work.save(file_path)
	print('保存成功')

if __name__ == '__main__':
	get_size_file(file_path)


