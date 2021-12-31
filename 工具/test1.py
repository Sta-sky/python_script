import time

from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.baidu.com/s?wd={}&rsv_spt=1&rsv_iqid=0x937adbe3000351e7&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=5&rsv_sug1=4&rsv_sug7=101&rsv_sug2=0&rsv_btype=i&inputT=674&rsv_sug4=1087"
browser = webdriver.Chrome()

browser.get(url.format("test"))
tool_class_list = [ "c-icon", "icons_2hrV4"]

tool_node = None
for tool_class in tool_class_list:
	try:
		tool_node = browser.find_element(By.CLASS_NAME, tool_class)
	except Exception as e:
		continue
	

print(tool_node)
if tool_node:
	time.sleep(3)
	tool_node.click()
	print('===')

	

browser.find_element(By.ID, 'timeRlt').click()



