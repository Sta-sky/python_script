from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as mouseAction
import time
url = 'https://login.tmall.com/'
brower = webdriver.Chrome()
brower.set_window_size(1200, 800)
brower.get(url)

brower.switch_to.frame(brower.find_element(By.ID, 'J_loginIframe'))
user = brower.find_element(By.ID, 'fm-login-id').send_keys('13981980452')
passw = brower.find_element(By.ID, 'fm-login-password').send_keys('10793300d')

#  如果 10 秒内 login_button 按钮加载出来了 再点击
time.sleep(1)
brower.switch_to.frame(brower.find_element(By.ID, 'baxia-dialog-content'))
while True:
	time.sleep(2)
	slider = brower.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
	print(slider)
	distance = 260
	actions = webdriver.ActionChains(brower)
	print(']]]', actions)
	actions.click_and_hold(slider) # 点击并持续开始拖拽
	actions.pause(0.4) # 设置按下停顿时间 模拟人为操作
	# 横向移动 300 纵向0
	# +5 -10 是为了模拟人为操作  拖动超过了  然后再拖回来
	actions.move_by_offset(distance, 0)
	time.sleep(4)
	actions.pause(5)
	actions.release() # 松开鼠标
	actions.perform() # 结束动作
	try:
		# presence_of_element_located shu_div节点是否存在
		WebDriverWait(brower, 1).until(ec.presence_of_element_located((By.ID, 'nc_1_refresh1')))
		brower.find_element(By.ID, 'nc_1_refresh1').click()
	except Exception as e:
		break
	
brower.switch_to.default_content()
brower.find_element(By.CLASS_NAME, 'fm-button fm-submit password-login')
time.sleep(2)
brower.switch_to.default_content()
print('登录成功')
brower.quit()






