import os
import time

import redis
import scrapy
from Crypto.Cipher import AES

from spider_web.byte_change_str import change_str


class DownTsSpider(scrapy.Spider):

    name = 'down_ts'
    allowed_domains = ['www.nihao.com']
    start_urls = []
    redis_clent = redis.Redis(host='127.0.0.1', db=2)
    while True:
        reds_data = redis_clent.spop('my-video-name')
        print(f'当前集合中总共有{redis_clent.scard("my-video-name")}个文件待下载')
        if not reds_data:
            print('数据取完了，退出')
            break
        print('集合中的数据', change_str(reds_data))
        new_save_path = change_str(reds_data).split('_')[0]
        file_name = new_save_path.split('\\')[-1]
        key = change_str(reds_data).split('_')[1]
        print('集合解析出来的数据', new_save_path, key)
        # 获取下载ts

        hash_data ={}
        if redis_clent.exists(new_save_path):
            hash_data = change_str(redis_clent.hgetall(new_save_path))
            for path, ts in hash_data.items():
                start_urls = [ts_url for ts_url in ts.split("|") if ts_url]
                print('reques中的url', start_urls)
                print(f'字典中的{path}')
                print(f'字典中的{ts.split("|")}')
                print(f'hashdata的结果{hash_data}')
                print(f'当前文件的保存路径{new_save_path}')
                print(f'当前文件的key为{key}')
                print(f'文件中的ts数量为{len(start_urls)}')
                print('=====================================================')
        else:
            print('redis的hash中么有这个文件路径')
        time.sleep(0)
        ts_length = len(start_urls)

    def __init__(self):
        super(DownTsSpider, self).__init__()
        self.num = len(self.start_urls)
        self.path = self.new_save_path
        print(f'start_url中的url数量为{self.path}')
        print(f'当前self中文件的保存；路径为{self.num}')


    def parse(self, response):
        """功能函数2:解密,保存"""
        # decrypt方法的参数需要为16的倍数，如果不是，需要在后面补二进制"0"
        current_count = len(self.start_urls)
        sprytor = None
        # 获取当前页请求的url
        current_url = response.request.url
        print(f"当前下载：{self.file_name[0:15]}")
        progrees = float('%.2f' % (current_count / self.ts_length)) * 100
        print('ts数量{}，当前下载第{}个，已经下载{}%,'.format(
            self.ts_length, current_count, progrees))
        # key为None时不需要解密，
        if self.key:
            sprytor = AES.new(self.key, AES.MODE_CBC, IV=self.key)
        try:
            ts_data = response.content
            # 密文长度不为16的倍数，则添加b"0"直到长度为16的倍数
            while len(ts_data) % 16 != 0:
                ts_data += b"0"
            # 此种情况下，没有使用key加密，可以直接写入文件，
            # 判断是否加密，可直接下载一个ts文件，如果正常播放，表示没有加密
            if not self.key or self.key == '':
                with open(self.new_save_path, "ab") as file:
                    file.write(ts_data)
            # print(f'{ts_name}已下载写入')
            else:
                with open(self.new_save_path, "ab") as file:
                    file.write(sprytor.decrypt(ts_data))
        # print(f'{ts_name}已下载写入')
        except Exception as e:
            print(f'保存ts文件失败，原因为{e}')
            return False


if __name__ == '__main__':
    fs = DownTsSpider()
