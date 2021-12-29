import matplotlib.pyplot as plot


def get_img():

	img_path = './4.jpg'
	# 使用python的matplotlib库读取图片
	user_img = plot.imread(img_path)
	print("没处理过的原图: ")
	plot.imshow(user_img)
	plot.show()
	print(user_img.shape)
	return user_img


def handle_img(origin_img):
	# 横竖每二十个像素点  拿出通道中的数据做显示， 跳过的数据为空，显示无色,
	handle_img = origin_img[::20, ::20]
	print("处理过的后的马赛克图片：")
	plot.imshow(handle_img)
	plot.show()
	print(handle_img.shape)
	
	# 从原图像中 可看出 头部坐标 截取头部 进行马赛克处理  垂直方向:水平方向
	origin_head_data = origin_img[50:350, 200:500]
	# 对头部进行马赛克处理
	origin_head_img = origin_head_data[::10, ::10]
	plot.imshow(origin_head_img)
	print(f'头部马赛克的行列：{origin_head_img.shape}')
	plot.show()
	
	shape_head = origin_head_img.shape
	row = shape_head[0]
	col = shape_head[1]
	origin_copy = origin_img.copy()

	for i in range(row):
		for j in range(col):
			# 截取行列的开始结束  行开始：50 列开始200 替换成头部 origin_head_img
			origin_copy[50 + i*10 : 60+i*10, 200+j*10 : 210+j*10] = origin_head_img[i, j]
	plot.imshow(origin_copy)
	plot.show()

if __name__ == '__main__':
	orgin_path = get_img()
	handle_img(orgin_path)
