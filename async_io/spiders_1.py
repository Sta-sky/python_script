# -*- coding: utf8 -*-
import os
import re
import time
import queue
import random
import urllib3
import requests
from log_util import Log
from threading import Lock
from threading import Thread
from Crypto.Cipher import AES
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options

logger = Log('kele_3').print_info()


class Spider_Video():
    def __init__(self):
        self.url = "https://www.kele61.com/video/video_list.html?video_type={}&page_index={}"
        self.tow_url = 'https://www.kele15.com/video/video_play.html?video_id={}'
        self.file_path = 'C:\\Users\\Administrator\\Desktop\\Python\\opencv\\scripy\\available_ip.txt'

        # 控制下载页数
        self.start_page = 0
        # 最大page为4
        self.end_page = 2

        # 从此处可以用切片的方式选择从所有视频列表中第几个开始抓取，video.get_m3u8_url(lists_id[:3], names_list[:3]) 从第三个开始
        # 控制列表中的视频下载位置
        self.video_num = 0
        # 文件存储路径
        self.file_save_base_path = 'G:\\MAT\\video\\kele\\{}.mp4'
        self.new_save_path = 'H:\\ITM\\new_video\\{}.mp4'

        # 控制文件大小，大于700个数量的ts，就不去下载
        self.ts_list_size = 1500
        self.url_quueu = queue.Queue(1000)

        self.host = None
        self.referer = 'https://www.kele15.com/video/video_play.html?video_id={}'
        self.agent = UserAgent(verify_ssl=False).random
        self.headers = {
            'User-Agent': self.agent,
            'Origin': 'https://www.kele15.com',
            'Referer': self.referer,
            'Connection': 'close'
        }

    def open_browser(self):
        self.proxy_http_pool = []
        proxy_dic = self.random_host_port()
        self.profile = self.update_firfox_proxy(proxy_dic)
        # 无头浏览器
        options = Options()
        options.add_argument('--headless')
        # 消除警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        browser = webdriver.Firefox(options=options)
        return browser

    def update_firfox_proxy(self, proxy_dict):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', proxy_dict['host'])
        profile.set_preference('network.proxy.http_port', proxy_dict['port'])
        # 为https设置的
        # profile.set_preference('network.proxy.ssl', proxy['host'])
        # profile.set_preference('network.proxy.ssl_port', proxy['port'])
        profile.update_preferences()
        return profile

    def random_host_port(self):
        with open(self.file_path, 'r') as fp:
            data = fp.readlines()
            for i in data:
                ip_data = i.split('_')[1]
                port_data = i.split('_')[2].replace('\n', '')
                proxy_http_key = f'{ip_data}:{port_data}'
                self.proxy_http_pool.append(proxy_http_key)
        random_proxy = random.sample(self.proxy_http_pool, 1)
        host = random_proxy[0].split(':')[0]
        port = random_proxy[0].split(':')[1]
        proxy = {
            'host': host,
            'port': int(port)
        }
        return proxy

    def get_video_id(self):
        id_name_list = []
        id_count = 0
        type = 1
        browser = self.open_browser()
        try:
            for page in range(self.start_page, self.end_page):
                page += 1
                url = self.url.format(type, page)
                logger.info(url)
                browser.get(url=url)
                for ele_num in range(20):
                    lists = []
                    ele_num += 1
                    id_count += 1
                    href_ele = browser.find_element_by_xpath(
                        f'/html/body/div[12]/div/ul/li[{ele_num}]/a')
                    href = href_ele.get_attribute('href')
                    id_num = href.split('=')[1]
                    self.referer.format(id_num)
                    video_name = browser.find_element_by_xpath(
                        f'/html/body/div[12]/div/ul/li[{ele_num}]/a/h3/span[2]').text
                    lists.append(video_name)
                    logger.info(
                        f'当前的为第{id_count}个视频，id为：{id_num}, 影片名称：{video_name}')
                    lists.append(id_num)
                    id_name_list.append(lists)
            logger.info(f'所有id获取完毕')
            browser.close()
            return id_name_list
        except Exception as e:
            logger.info(f'id列表获取失败，失败原因为{e}')
        finally:
            browser.quit()
            return id_name_list

    def get_m3u8_save_video(self, id, video_name, th_name):
        save_file_path = self.file_save_base_path.format(video_name)
        new_save_path = self.new_save_path.format(video_name)
        if os.path.exists(save_file_path) or os.path.exists(new_save_path):
            raise Exception(f'-------文件已经存在-------,name{video_name}')
        logger.info(f'文件不存在，由线程{th_name}开始下载，保存路径为：{new_save_path}')
        tow_url = self.tow_url.format(id)
        request_res = self.return_requests_data(tow_url)
        if not request_res:
            raise Exception('二级面请求失败')
        else:
            page_data = request_res.text
            request_m3u8 = self.get_m3u8_key_ts_url(page_data)
            key_val, ts_list_url = request_m3u8
            ts_length = len(ts_list_url)
            if ts_length > self.ts_list_size:
                raise Exception(f'文件ts数量为{ts_length}个,大于{self.ts_list_size}个ts')
            return key_val, ts_list_url, new_save_path, video_name, th_name

    def get_m3u8_key_ts_url(self, page_data):
        """ 函数功能， 通过视频播放页面地址，获取m3u8地址，
            根据m3u8地址，请求ts文件列表
            如果有两个ts文件，则有一个是真的能返回ts文件的地址，根据另一个拼接处真实ts地址
        """
        # 匹配出m3u8的地址
        m3u8_re = '(.*)\.m3u8'
        src_path = re.findall(m3u8_re, page_data)
        # logger.info('文件中匹配出的没有过滤的m3u8地址列表', src_path)
        m3u8_file_res_url = src_path[0].split('=')[1].replace('"', '').strip()

        judge_http = m3u8_file_res_url.split('/')
        # logger.info(judge_http)
        if 'https:' not in judge_http:
            m3u8_file_res_url = 'https:' + m3u8_file_res_url
        replace_word = m3u8_file_res_url.split('/')[-1]
        # logger.info('替换的后缀的关键字关键字', replace_word)
        base_url_key_ts = m3u8_file_res_url.replace(replace_word, '')
        # logger.info('文件中的m3u8_url:', m3u8_file_res_url)
        # 通过页面中取得的m3u8地址，拼接出携带域名为止的url，用于后面拼接真正的m3u8 url
        domain_base_url = m3u8_file_res_url.split('com')[0] + 'com'

        # 用页面中的m3u8地址 获取文件，看是否有两个m3u8 url
        false_m3u_url = m3u8_file_res_url + '.m3u8'
        request_res = self.return_requests_data(false_m3u_url)
        if not request_res:
            raise Exception('一级m3u8地址请求失败')
        else:
            false_m3u8_file = request_res.text
            m3u8_re = '(.*)\.m3u8'
            true_link = re.findall(m3u8_re, false_m3u8_file)
            # logger.info('匹配出的m3u8链接列表为：', true_link)

            # 如果是两个m3u8 url，则拼接真实的m3u8 url，获取ts文件，
            if true_link:
                true_m3u8_url = domain_base_url + true_link[0] + '.m3u8'
                # logger.info('真实的m3u8链接：', true_m3u8_url)
                request_res = self.return_requests_data(true_m3u8_url)
                if not request_res:
                    raise Exception('二级m3u8地址请求失败')
                else:
                    ts_url_data = request_res.text
                    ts_key_base_url = domain_base_url

            # 如果不是，则说明只有一个m3u8 url，继续使用上面的false_m3u_url获取的数据匹配ts文件
            else:
                ts_url_data = false_m3u8_file
                ts_key_base_url = base_url_key_ts
            # logger.info('ts_base_url', ts_key_base_url)
            # 匹配出ts url的后缀
            ts_re = '(.*)\.ts'
            ts_list = re.findall(ts_re, ts_url_data)
            # logger.info('文件中匹配出的ts_list列表', ts_list)
            key_re = '(.*)\.key'
            key_list = re.findall(key_re, ts_url_data)
            # logger.info(f'文件中匹配出的key_list:{key_list}')
            key_val = False
            if key_list:
                # logger.info('需要解密')
                key_val = True
            key_val, ts_list_url, = self.request_ts_key_url_list(
                ts_list, ts_key_base_url, key_val)
            return key_val, ts_list_url


    def request_ts_key_url_list(self, ts_lists, key_ts_base_url, key_value):
        """ 函数功能，返回解密key，ts地址"""
        ts_url_list = []
        for ts in ts_lists:
            res_ts_url = key_ts_base_url + str(ts) + '.ts'
            # logger.info(138, res_ts_url)
            ts_url_list.append(res_ts_url)
        # 判断key是在文件中，还是请求地址中包含着，大于则说明不在地址中，小于则说明在
        if key_value:
            key_url = key_ts_base_url + 'key.key'
            # logger.info(f'需要解密,key_url为：{key_url}')
            key_banery = requests.get(url=key_url)
            key_banerys = key_banery.content
            key_banery.close()
        else:
            key_banerys = None
        # logger.info('不需要解密')
        return key_banerys, ts_url_list

    def decrypt_save_ts(self, key, ts_urls, new_save_path, file_name,
                        down_th_name):
        """功能函数2:解密,保存"""

        # decrypt方法的参数需要为16的倍数，如果不是，需要在后面补二进制"0"
        total_size = len(ts_urls)
        down_num = 0

        for ts_url in ts_urls:
            down_num += 1
            progrees = float('%.2f' % (down_num / total_size)) * 100
            logger.info('ts数量{}，当前下载第{}个，已经下载{}%,'.format(total_size, down_num,
                                                          progrees))
            ts_name = ts_url.split("/")[-1]  # ts文件名
            # 解密，new有三个参数，
            # 第一个是秘钥（key）的二进制数据，
            # 第二个使用下面这个就好
            # 第三个IV在m3u8文件里URI后面会给出，如果没有，可以尝试把秘钥（key）赋值给IV
            sprytor = None
            if key:
                sprytor = AES.new(key, AES.MODE_CBC, IV=key)
            # 获取ts文件二进制数据
            logger.info(f"正在由={down_th_name}=下载：{file_name[0:10]} 影片的ts" + ts_name)
            time.sleep(0.5)
            request_res = self.return_requests_data(ts_url)
            if not request_res:
                logger.info(f'ts请求超过20次，删除文件之后,再次将url加入列队，开始请求下一个ts：{ts_url}')
                os.remove(new_save_path)
                logger.info('删除成功')
                return False
            else:
                try:
                    ts_data = request_res.content
                    # 密文长度不为16的倍数，则添加b"0"直到长度为16的倍数
                    # ts_data = response_ts.content
                    # response_ts.close()
                    while len(ts_data) % 16 != 0:
                        ts_data += b"0"

                    # 此种情况下，没有使用key加密，可以直接写入文件，
                    # 判断是否加密，可直接下载一个ts文件，如果正常播放，表示没有加密
                    if key is None or key == '':
                        with open(new_save_path, "ab") as file:
                            file.write(ts_data)
                    # logger.info(f'{ts_name}已下载写入')
                    else:
                        with open(new_save_path, "ab") as file:
                            file.write(sprytor.decrypt(ts_data))
                # logger.info(f'{ts_name}已下载写入')
                except Exception as e:
                    logger.error(f'保存ts文件失败，原因为{e}')
                    return False
        return True

    def return_requests_data(self, param_url):
        self.headers['User-Agent'] = self.agent
        retry_times = 20
        retry_count = 0
        for i in range(retry_times):
            retry_count += 1
            try:
                if retry_count > 1:
                    logger.info(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
                http_res = requests.get(url=param_url, verify=False, headers=self.headers, timeout=5)
                http_res.close()
                return http_res
            except Exception as e:
                if retry_count >= retry_times:
                    logger.info(f'{param_url},请求失败，原因{e}')
                    return False
                else:
                    continue

    def pruduct_queue(self):
        name_id_lsit = self.get_video_id()
        for id_name in name_id_lsit:
            self.url_quueu.put(id_name)
        logger.info(f'队列中中共有{self.url_quueu.qsize()}个元素')
        return self.url_quueu


class MyKeleSpider(Thread):
    def __init__(self, user_th_name, url_queue, totle_video):
        super().__init__()
        self.setName(user_th_name)
        self.name = self.getName()
        self.status = self.is_alive()
        self.lock = Lock()
        self.totle_video = totle_video
        self.queue_url = url_queue

    def run(self):
        SpiderVideo = Spider_Video()
        # 每个线程，先获取当前的队列中的总数
        current_queue_num = self.queue_url.qsize()
        # 通过传入的总的队列数，减去当前的队列数，为当前正在下载的第几个
        current_video_num = self.totle_video - current_queue_num
        while True:
            if self.queue_url.empty():
                logger.info(f'队列为空，当前线程{self.name}下载完成，退出，当前队列中的个数为{current_queue_num}')
                break
            else:
                name_id = self.queue_url.get()
                self.totle_video -= 1
                logger.info(f'共{self.totle_video}个视频；由=={self.name}==开始下载第{current_video_num}个视频')
                id = name_id[1]
                name = name_id[0]
                try:
                    res_key_ts = SpiderVideo.get_m3u8_save_video(id, name, self.name)
                except Exception as e:
                    logger.info(e)
                    continue
                key, ts_url, video_save_path, video_name, down_th_name = res_key_ts
                down_video_res = SpiderVideo.decrypt_save_ts(key, ts_url, video_save_path, video_name, down_th_name)
                if not down_video_res:
                    self.queue_url.put(name_id)
                    logger.info(f'保存ts阶段失败，再次加入队列{name_id}')
                else:
                    continue


if __name__ == '__main__':
    th_num = 30
    video = Spider_Video()
    queue_url = video.pruduct_queue()
    totle_video = queue_url.qsize()
    th_list = []
    for th in range(th_num):
        th_name = '___党的线程' + str(th) + '____'
        th_thread = MyKeleSpider(th_name, queue_url, totle_video)
        th_list.append(th_thread)
    for j in th_list:
        j.start()
    for i in th_list:
        i.join()
        logger.info(f'线程{i.name}回收完成')