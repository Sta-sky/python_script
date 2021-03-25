"""
百度图片的抓取
"""
from time import sleep
from urllib import parse
import os
import requests
from selenium import webdriver


class BaiduImgSpider(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/index?tn=baiduimage&word={}'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.browser = webdriver.Firefox()
        self.i = 1
        self.word = input('请输入下载图片关键字：')
        # 下载地址
        self.diretory = 'D:\\spider_load\\images\\{}\\'.format(self.word)
        # 判断是否有文件夹 没有直接创建；
        if not os.path.exists(self.diretory):
            os.makedirs(self.diretory)

    def get_html(self, one_url):
        self.browser.get(url=one_url)
        input_node = self.browser.find_element_by_xpath('//*[@id="kw"]')
        input_node.send_keys(self.word)
        for i in range(0, 20):
            count = 19 - i
            if count == 0:
                print('开始下载')
            else:
                print('图片加载中--->>%d后开始下载  请等待···' % count)
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(1)
        img_link = self.browser.find_elements_by_xpath('//li[@class="imgitem"]')
        self.parmse(img_link)

    def parmse(self, img_link):
        #     获取页面的链接地址
        length = len(img_link)
        try:
            for link in img_link:
                # xpath  获取自定义属性  需要先获取到属性节点 根据姐点的get_attribute()方法才能获取。
                links = link.find_element_by_xpath('.//div[@class="imgbox"]//img').get_attribute('data-imgurl')
                print(links)
                print(links[-4:])
                z_img = requests.get(url=links, headers=self.headers).content
                filename = self.diretory + str(self.i) + '_' + links[-4:]
                with open(filename, 'wb') as f:
                    f.write(z_img)
                print(filename + '下载成功!! 已经下载了:%.2f ' % ((self.i / length) * 100) + '%')
                self.i += 1
                print()
                sleep(0.1)
        except Exception as e:
            print('百度爸爸发现了，终止爬取！')

    def run(self):
        word = self.word
        parmse = parse.quote(word)
        one_url = self.url.format(parmse)
        self.get_html(one_url)


if __name__ == '__main__':
    img = BaiduImgSpider()
    img.run()
