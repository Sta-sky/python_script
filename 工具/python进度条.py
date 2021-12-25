import time
from tqdm import tqdm

res = [item for item in range(100)]

# 方式一
bar = tqdm(total=len(res))
bar.set_description("进度为：")
for item in res:
	bar.update(1)
	time.sleep(0.1)
bar.close()


# 方式二
with tqdm(total=len(res)) as bar:
	bar.set_description('方式二：')
	for item in res:
		bar.update(1)
		time.sleep(0.1)
		
