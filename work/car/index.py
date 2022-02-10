# -*- coding: utf-8 -*-
import os.path

import tqdm

img_fix_list = ['jpg', 'png']

# 自己的 APPID AK SK
APP_ID = '25573115'
API_KEY = 'gokX1BWRwfC2vyAenEtEXSsK'
SECRET_KEY = 'eXY20R34Iy6ZKMXWUMvfitKqA2ymhF6o'
from aip import AipOcr


# 读取图片
def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
		return fp.read()


# 创建客户端对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 建立连接的超时时间，单位为毫秒
client.setConnectionTimeoutInMillis(5000)
# 通过打开的连接传输数据的超时时间，单位为毫秒
client.setSocketTimeoutInMillis(5000)


def print_car_info():
	path_info = os.listdir('./')
	file_list = [item for item in path_info if os.path.isfile(item) and item.split('.')[-1] in img_fix_list]

	for item in tqdm.tqdm(file_list):
		image = get_file_content(item)
		res = client.licensePlate(image)
		print(res)

print_car_info()





