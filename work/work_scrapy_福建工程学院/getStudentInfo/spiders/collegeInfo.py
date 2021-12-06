import random
import time

import scrapy

from getStudentInfo.items import GetstudentinfoItem

class CollegeinfoSpider(scrapy.Spider):
    name = 'collegeInfo'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    # allowed_domains = ['bbs.51testing.com']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    base_url = 'https://www.nbufe.edu.cn/sg/list_1.htm?typeid=1281&typeid2=1281&page={}'
    page = 1
    start_urls = [base_url.format(page)]

    def parse(self, response):  # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
        # node_list = response.xpath('//tbody[@id ="separatorline"]/following-sibling::tbody')
        lastPage = response.xpath("//*[contains(@class, 'pagination')]/a")[-2]
        totalPage = lastPage.xpath('text()').get('data')
        print(lastPage.xpath('text()'))
        node_list = response.xpath("//*[contains(@class, 'btxt2')]")
        print(len(node_list), '===')
        
        
        for node in node_list:
            time.sleep()
            item = GetstudentinfoItem()  # 类型是list
            yield item  # 返回item（列表），return会直接退出程序，这里是有yield

        if self.page < int(totalPage):

            self.page += 1
            print(self.page, '[[[[[[[[[[[[[[[[[')
            yield scrapy.Request(self.base_url + str(self.page), callback=self.parse)  # 返回请求，请求回调parse


