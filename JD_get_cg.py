"""

selenium 爬取网站信息

爬取成果的衣服信息

"""
from time import sleep

from selenium import webdriver
import redis

class Jdspider(object):
    def __init__(self):
        self.url = 'https://www.jd.com'
        self.browser = webdriver.Firefox()
        self.r = redis.Redis(host='localhost',db=3,port='6379')

    # 获取页面
    def get_html(self):
        self.browser.get(self.url)
        #找到输入搜索关键字的 xpath节点
        input_node = self.browser.find_element_by_xpath('//*[@id="key"]')

        input_node.send_keys('演员成果')
        # 找到点击按钮节点  点击
        button_node = self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
        button_node.click()
        sleep(1)
    #解析页面
    def parse_html(self):
    # 获取页面 的内容
        # 滚动鼠标滑轮 拉进页面度条
        self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        #给商品预留加载时间

        #抓数据
        li_list = self.browser.find_elements_by_xpath('//*[@class="gl-item"]/div')
        dic = {}
        print(len(li_list))
        count = 100
        for li in li_list:
            count +=1
            title = dic['title'] = li.find_element_by_xpath('.//div[@class="p-name p-name-type-2"]/a/em').text
            price = dic['price'] = li.find_element_by_xpath('.//div[@class="p-price"]').text
            comment = dic['comment'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text
            shop = dic['shop"'] = li.find_element_by_xpath('.//div[@class="p-shop"]').text
            print(dic)
            print('*' * 50)
            key = 'CG'+str(count)
            print(key)
            self.r.lpush(key,title,price,shop,comment)
            self.r.save()

    def run(self):
        self.get_html()
        self.parse_html()




if __name__ == '__main__':
    jdspider = Jdspider()
    jdspider.run()






