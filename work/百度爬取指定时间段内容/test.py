import base64
import re
from urllib import parse


url_1 = 'https://www.baidu.com/s?wd=test&rsv_spt=1&rsv_iqid=0x937adbe3000351e7&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=5&rsv_sug1=4&rsv_sug7=101&rsv_sug2=0&rsv_btype=i&inputT=674&rsv_sug4=1087'
url_2 = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd=test&rsv_spt=1&oq=test&rsv_pq=f6c7fa7700068dd6&rsv_t=c8aaxJcRYOsjQrD%2FM0TZc7%2FTm1p6okr8hFAlnrSoeAd8yfS1dzcGnBNyJct5btt7qlcd&rqlang=cn&rsv_enter=1&rsv_dl=tb&gpc=stf%3D1577808000%2C1640966400%7Cstftype%3D2&tfflag=1'
url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd=test&rsv_spt=1&oq=test&rsv_pq=f6c7fa7700068dd6&rsv_t=63551Ytlk%2F5XzYKfU7QpKBSYPJEnaXJR0OLwJSm7%2BcZc%2Bmtop%2Fe6MgxxXqaLaQzlNf%2Fc&rqlang=cn&rsv_enter=1&rsv_dl=tb&gpc=stf%3D1262275200%2C1640880000%7Cstftype%3D2&tfflag=1"

import time
# print(parse.parse_qs(parse.urlsplit(url).query))


# "1262275200,1640880000"
# time_tuple = time.localtime(1262275200)
# print(time_tuple)
# format_time = time.strftime("%Y-%m-%d %H-%M_%S", time_tuple)
# print(format_time)

# html_text = '<span class="hint_PIwZX c_font_2AD7M">百度为您找到相关结果约58,100,000个</span>'
#
#
#
# data = re.search('约(.*?)个', html_text)
# print(data.group(1).replace(',', ''))

#
with open('./search_key.txt', 'r', encoding='utf-8')as fp:
	search_data = fp.read()
search_key_list = search_data.split("、")


with open('./city.txt', 'r', encoding='utf-8')as fp:
	city_data = fp.readlines()


with open('./rotation_image.png', 'rb') as fp:
	data = base64.b64encode(fp.read())
	print(data)
distance_api = int(data)
print(distance_api)


# every = len(search_key_list) * len(city_data)
# ress  = '%.10f' % (1 / every)
# res = float(ress)
# print(res)
# print(type(res))
# import tqdm
# with tqdm.tqdm(total=every) as bar:
# 	for item in range(every):
# 		time.sleep(0.1)
# 		bar.update(res)