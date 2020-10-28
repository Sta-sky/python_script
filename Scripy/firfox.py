import os
import random
import re
import time

import redis
import requests
import scrapy
import scrapy_redis
from Crypto.Cipher import AES
from spider_web.byte_change_str import change_str
from lxml import etree
from bs4 import BeautifulSoup


class WebSpider(scrapy.Spider):
    name = 'web'
    allowed_domains = ['http://127.0.0.1']
    start_urls =[]
    start_page = 0
    end_page = 2
    primery_url_list = []
    url = 'https://ggcc01.com/archives/category/jingpin/page/{}'
    for num in range(start_page, end_page):
        start_urls.append(url.format(num))

    def __init__(self):
        super(WebSpider, self).__init__()
        self.redis_clent = redis.Redis(host='127.0.0.1', db=2)
        self.ts_list_size = 3000
        self.file_save_base_path = 'c\\nihao'
        self.new_save_path = 'c\\nihao'
        self.set_name = 'ts_str'
        self.save_redis_npath_txt = ''

    def parse(self, response):
        pass

    def get_redis_link(self):
        char_link = self.redis_clent.spop(self.set_name)
        yield scrapy.Request(
            change_str(char_link), callback=self.get_m3u8_save_video)

    def get_m3u8_save_video(self, response):
        """
        匹配出m3u8地址， 跟影片名
        :param response:
        :return:
        """
        if not response:
            print('子页面请求失败')
            return
        else:
            page_data = response.text
            m3u8_re = '(.*)\.m3u8'
            src_path = re.findall(m3u8_re, page_data)
            # print('文件中匹配出的没有过滤的m3u8地址列表', src_path)
            if not src_path:
                print('匹配出的m3u8列表为空')
            m3u8_file_res_url = src_path[2].split(': ')[1].split('"')[1]
            ele = etree.HTML(page_data)
            try:
                file_name = ele.xpath('//title/text()')[0]
            except Exception:
                file_name = random.randint(1, 100)
                print(f'没有匹配出name，当前的name为随机数 ： {file_name}')
            save_file_path = self.file_save_base_path.format(file_name)
            new_save_path = self.new_save_path.format(file_name)
            if os.path.exists(save_file_path) or os.path.exists(new_save_path):
                print(f'-------文件已经存在-------,name{file_name}')
                return
            print(f'文件不存在，保存路径为：{new_save_path}')

            # 从页面上匹配的m3u8地址没有https：前缀，这种情况是在有需要key解密的ts，
            judge_http = m3u8_file_res_url.split('/')
            if 'https:' not in judge_http and 'http:' not in judge_http:
                m3u8_file_res_url = 'https:' + m3u8_file_res_url
            # print('页面中返回处理后最终的m3u8_url:', m3u8_file_res_url)

            base_url_key_ts = m3u8_file_res_url.replace('index', '')
            # 通过页面中取得的m3u8地址，拼接出携带域名为止的url，用于后面拼接真正的m3u8 url
            domain_base_url = m3u8_file_res_url.split('com')[0] + 'com'

            # 用页面中的m3u8地址 获取文件，看是否有两个m3u8 url
            false_m3u_url = m3u8_file_res_url + '.m3u8'
            data = {
                'domain_base_url': domain_base_url,
                'base_url_key_ts': base_url_key_ts,
                'new_save_path': new_save_path,
                'file_name': file_name
            }
            yield scrapy.Request(
                false_m3u_url, callback=self.get_one_m3u8, cb_kwargs=data)

    def get_one_m3u8(
        self, response, domain_base_url, base_url_key_ts, new_save_path,
            file_name):

        false_m3u8_file = response.text
        key_val = self.match_key(false_m3u8_file)
        if key_val:
            key_base_url = domain_base_url + key_val
        else:
            key_base_url = key_val
        m3u8_re = '(.*)\.m3u8'
        true_link = re.findall(m3u8_re, false_m3u8_file)
        # print('匹配出的m3u8链接列表为：', true_link)

        # 如果是两个m3u8 url，则拼接真实的m3u8 url，获取ts文件，
        # 如果不是，则说明只有一个m3u8 url，继续使用上面的false_m3u_url获取的数据匹配ts文件
        ts_url_data = ''
        ts_base_url = ''
        if not true_link:
            ts_url_data = false_m3u8_file
            ts_base_url = base_url_key_ts
        else:
            # 判断匹配出的真实链接是否携带https/http 头
            if 'https:' in true_link[0].split('/') or 'http:' not in \
                    true_link[0].split('/'):
                true_m3u8_url = domain_base_url + true_link[0] + '.m3u8'
            else:
                true_m3u8_url = true_link[0]
            # print('真实的m3u8链接：', true_m3u8_url)
            data = {
                'domain_base_url': domain_base_url,
                'new_save_path': new_save_path,
                'file_name': file_name,
            }
            yield scrapy.Request(
                true_m3u8_url, callback=self.get_tow_m3u8, cb_kwargs=data)
        # 匹配出ts url的后缀
        ts_re = '(.*)\.ts'
        ts_list = re.findall(ts_re, ts_url_data)
        self.handle_ts_key_save_info(
            ts_list, ts_base_url, key_base_url, new_save_path, file_name)

    def get_tow_m3u8(
            self, response, domain_base_url, new_save_path,file_name):
        key_base_url = ''
        if not response:
            print('m3u8请求失败')
            return
        else:
            ts_url_data = response.text
            true_key_val = self.match_key(ts_url_data)
            if true_key_val:
                key_base_url = domain_base_url + true_key_val
            # print(f'加密了，第二次请求m3u8匹配的key，拼接的key_url{key_base_url}')
            ts_base_url = domain_base_url

        # 匹配出ts url的后缀
        ts_re = '(.*)\.ts'
        ts_list = re.findall(ts_re, ts_url_data)
        self.handle_ts_key_save_info(
            ts_list, ts_base_url, key_base_url, new_save_path, file_name)

    def handle_ts_key_save_info(
        self, ts_lists, ts_base_url, key_url_base, new_save_path, file_name):
        """ 函数功能，返回解密key，ts地址"""
        ts_url_list = []
        for ts in ts_lists:
            res_ts_url = ts_base_url + str(ts) + '.ts'
            ts_url_list.append(res_ts_url)
        if key_url_base:
            key_url = key_url_base + '.key'
            # print(f'文件需要解密，密钥url为{key_url}')
            key_banery = self.return_requests_data(key_url)
            key_value = key_banery.content
        else:
            # print('文件不需要解密')
            key_value = None
        ts_length = len(ts_url_list)
        if ts_length > self.ts_list_size:
            print(f'文件ts数量为{ts_length}个,大于{self.ts_list_size}个ts')
            return
        index_path_key = new_save_path + '_' + key_value
        with open(self.save_redis_npath_txt, 'a+', encoding='utf8') as fp:
            fp.write(new_save_path + '\n')
        self.redis_clent.sadd(file_name, index_path_key)
        self.redis_clent.hset(name=new_save_path, key=index_path_key,
                              value=ts_url_list)

    def match_key(self, request_data_file):
        key_re = '(.*)\.key'
        key_list = re.findall(key_re, request_data_file)
        # print(f'文件中匹配出的key_list:{key_list}')
        try:
            key_val = key_list[0].split('"')[1]
            return key_val
        except Exception as e:
            return None

    def return_requests_data(self, param_url):
        retry_times = 20
        retry_count = 0
        for i in range(retry_times):
            retry_count += 1
            try:
                if retry_count > 1:
                    print(
                        f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
                http_res = requests.get(url=param_url, verify=False,
                                        timeout=5)
                return http_res
            except Exception as e:
                if retry_count >= retry_times:
                    print(f'{param_url},请求失败，原因{e}')
                    return False
                else:
                    continue



