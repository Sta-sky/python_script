from selenium.webdriver.firefox.options import Options
from selenium import webdriver

class Daneispider(object):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.6e5b49c0DPOPIB&id=37564253018&skuId=4541955503054&user_id=931421195&cat_id=2&is_b=1&rn=b64d8311e6e1b58cd0d6ea8634210db0'
        self.url1 = 'http://tts.tmooc.cn/studentCenter/toMyttsPage'
        self.browser = webdriver.Firefox()

    def open_web(self):

        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//input[@id="fm-login-id"]').send_keys('18419360851')
        self.browser.find_element_by_xpath('//input[@id="fm-login-password"]').send_keys('52370851')
        self.browser.find_element_by_xpath('//button[@class="fm-button '
                                           'fm-submit password-login"]').click()



if __name__ == '__main__':
    d = Daneispider()
    d.open_web()

