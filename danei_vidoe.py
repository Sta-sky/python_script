"""
达内视频 下载

需要修改的地方：
    headers 中的cookie
    selenium 模拟登录的用户名密码
    下载地址
    user-agent尽量写自己电脑的 user-agent
    安装Crypto库   pip3 install pycryptodome
"""
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
import time
import requests
from lxml import etree
import re
from fake_useragent import UserAgent
from Crypto.Cipher import AES

class Daneispider(object):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.url = 'http://www.tmooc.cn/'
        self.url1 = 'http://tts.tmooc.cn/studentCenter/toMyttsPage'
        self.browser = webdriver.Firefox(options=options)

        # TODO self.cut表示 被反扒断开后，重新开始下载从第多少个文件开始  可以自由设定
        #  但要小于count 一般 在print(count)的值的前两位开始 大于会导致视频下不完整　
        #   81-85空档期 86 tornado 开始  self+.cut = 126 开始下载数据开发

        self.cut = 96

        self.headers = {
                #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
                'User-Agent':UserAgent().random,
                # TODO  写成自己TTS学习中心页面的 cookie
                #  cookie随时会变  匹配不到视频地址链接列表 或者视频名称 八成是cookie变了  浏览器中重新复制cookie
                # 'Cookie':'cloudAuthorityCookie=0; isCenterCookie=no; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1581843354,1581900640,1581934250,1581983937; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1581900665,1581900810,1581902796,1581983943; __root_domain_v=.tmooc.cn; _qddaz=QD.1o8in1.jffxzx.k46l5mbm; versionListCookie=AIDTN201908; defaultVersionCookie=AIDTN201908; versionAndNamesListCookie=AIDTN201908N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV07N22N728138; courseCookie=AID; stuClaIdCookie=728138; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1581983937; TMOOC-SESSION=183067d64ed94d0d90557a3acc32af55; sessionid=183067d64ed94d0d90557a3acc32af55|E_bfup31v; JSESSIONID=D509E7CFC8A4DA4BBE57661047A8431E; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1581984071; _qdda=3-1.1us199; _qddab=3-gplnzc.k6r4e8xs; _qddamta_2852189568=3-0',
                'Cookie':'isCenterCookie=no; cloudAuthorityCookie=0; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1582035310,1582035564,1582083367,1582088524; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1582083383,1582083580,1582086352,1582088530; __root_domain_v=.tmooc.cn; _qddaz=QD.1o8in1.jffxzx.k46l5mbm; versionListCookie=AIDTN201908; defaultVersionCookie=AIDTN201908; versionAndNamesListCookie=AIDTN201908N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV07N22N728138; courseCookie=AID; stuClaIdCookie=728138; _qdda=3-1.1us199; _qddamta_2852189568=3-0; TMOOC-SESSION=30b76f88c80949c6b77f52864b53893a; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1582088524; sessionid=30b76f88c80949c6b77f52864b53893a|E_bfup31v; JSESSIONID=37E66CC988C2A78128B9CF7E7F9620E3; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1582088711; _qddab=3-e0isuj.k6sunxfa',
                'Referer':'http://www.tmooc.cn/'}
        self.m3u8_url = "http://c.it211.com.cn/{}/{}"



    def login_html(self):
        """
        用selenium 登录 找出学习中心页面 的每个视频连接列表  以及每个视频的名称列表
        :return:
        """
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//a[@id="login_xxw"]').click()

        # TODO 自己的 账号 密码
        self.browser.find_element_by_xpath('//input[@id="js_account_pm"]').send_keys('18419360851')
        self.browser.find_element_by_xpath('//input[@id="js_password"]').send_keys('52370851')
        self.browser.find_element_by_xpath('//button[@id="js_submit_login"]').click()
        # time.sleep(3)

        tow_html = requests.get(url=self.url1,headers = self.headers).text
        # print(tow_html)
        parse_html = etree.HTML(tow_html)
        # print(parse_html)
        link_lists = parse_html.xpath('//li[@class="sp"]/a/@href')
        print(link_lists)

        #匹配出 视频名称列表
        word_list = parse_html.xpath('//li[@class="opened"]/p')
        print(word_list)
        self.load_video(link_lists[self.cut:],word_list[self.cut:])



    def load_video(self,link_lists,word_list):
        """
        匹配出  向每个视频地址发送请求，请求出视频加载页面
        构造视频页面的请求头  请求头中referer中的的menuId根据视频不同需要构造
        headerss 是m3u8地址动态加载视频数据的请求头
        使用正则 处理 拼接 视频名称
        :param link_lists:  视频连接列表
        :param word_list:   视频名称列表
        :return:
        """
        count = -1
        while count <= 147:
            # 匹配出每个视频链接的menuId  放入referer  构成headers
            link = link_lists[count+1]
            r = re.findall(".*=(.*)&.*", link)

            print(count)
            if (count)+2 % 5 == 0:
                time.sleep(60)
            referre = 'http://tts.tmooc.cn/video/showVideo?menuId={}&version=AIDTN201908'.format(r[0])
            # print(referre)
            headers = {

                #'Cookie': 'isCenterCookie=no; cloudAuthorityCookie=0; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1581843354,1581900640,1581934250,1581983937; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1581902796,1581983943,1581985499,1581986520; __root_domain_v=.tmooc.cn; _qddaz=QD.1o8in1.jffxzx.k46l5mbm; versionListCookie=AIDTN201908; defaultVersionCookie=AIDTN201908; versionAndNamesListCookie=AIDTN201908N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV07N22N728138; courseCookie=AID; stuClaIdCookie=728138; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1581983937; TMOOC-SESSION=183067d64ed94d0d90557a3acc32af55; sessionid=183067d64ed94d0d90557a3acc32af55|E_bfup31v; JSESSIONID=0CD929C514A53791789F9EA435D141CF; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1581986725; _qdda=3-1.1us199; _qddab=3-gplnzc.k6r4e8xs; _qddamta_2852189568=3-0',
                'Cookie': 'isCenterCookie=no; cloudAuthorityCookie=0; _qddac=3-3-1.1us199.e0isuj.k6sunxfa; Hm_lvt_51179c297feac072ee8d3f66a55aa1bd=1582035310,1582035564,1582083367,1582088524; tedu.local.language=zh-CN; Hm_lvt_e997f0189b675e95bb22e0f8e2b5fa74=1582083383,1582083580,1582086352,1582088530; __root_domain_v=.tmooc.cn; _qddaz=QD.1o8in1.jffxzx.k46l5mbm; versionListCookie=AIDTN201908; defaultVersionCookie=AIDTN201908; versionAndNamesListCookie=AIDTN201908N22NPython%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%25E5%2585%25A8%25E6%2597%25A5%25E5%2588%25B6%25E8%25AF%25BE%25E7%25A8%258BV07N22N728138; courseCookie=AID; stuClaIdCookie=728138; _qdda=3-1.1us199; _qddamta_2852189568=3-0; TMOOC-SESSION=30b76f88c80949c6b77f52864b53893a; Hm_lpvt_51179c297feac072ee8d3f66a55aa1bd=1582088524; sessionid=30b76f88c80949c6b77f52864b53893a|E_bfup31v; JSESSIONID=37E66CC988C2A78128B9CF7E7F9620E3; Hm_lpvt_e997f0189b675e95bb22e0f8e2b5fa74=1582088705; _qddab=3-e0isuj.k6sunxfa',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
                'Referer': referre}

            headerss = {
                "Origin": "http://tts.tmooc.cn",

                "Referer":referre,
                # 建议写本机的User-Agent
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
            }
            # print(link_lists)
            count +=1

            #匹配出 上午下午视频的 m3u8 的地址
            tow_html = requests.get(url=link_lists[count+1], headers=headers).content
            # print(tow_html)
            r = re.findall('.*\'(.*)\'', tow_html.decode())
            print(r)
            if r[1] == '':
                continue
            links = []

            e = re.findall('(.*)\.', r[1])
            f = re.findall('(.*)\.', r[2])
            link_am = self.m3u8_url.format(e[0],r[1])
            link_pm = self.m3u8_url.format(f[0],r[2])
            links.append(link_am)
            links.append(link_pm)
            if r[3] != '':
                d = re.findall('(.*)\.',r[3])
                link_d = self.m3u8_url.format(d[0],r[3])
                links.append(link_d)
            if  r[4] != '':
                g = re.findall('(.*)\.',r[4])
                link_g = self.m3u8_url.format(g[0],r[4])
                links.append(link_g)
            if  r[6] != '':
                g = re.findall('(.*)\.',r[6])
                link_g = self.m3u8_url.format(g[0],r[6])
                links.append(link_g)
            if  r[7] != '':
                g = re.findall('(.*)\.',r[7])
                link_g = self.m3u8_url.format(g[0],r[7])
                links.append(link_g)
            if  r[8] != '':
                g = re.findall('(.*)\.',r[8])
                link_g = self.m3u8_url.format(g[0],r[8])
                links.append(link_g)
            if  r[9] != '':
                g = re.findall('(.*)\.',r[9])
                link_g = self.m3u8_url.format(g[0],r[9])
                links.append(link_g)
            if  r[10] != '':
                g = re.findall('(.*)\.',r[10])
                link_g = self.m3u8_url.format(g[0],r[10])
                links.append(link_g)
            if  r[11] != '':
                g = re.findall('(.*)\.',r[11])
                link_g = self.m3u8_url.format(g[0],r[11])
                links.append(link_g)
            if  r[12] != '':
                g = re.findall('(.*)\.',r[12])
                link_g = self.m3u8_url.format(g[0],r[12])
                links.append(link_g)

            # 用正则处理名称格式
            words = word_list[count+1].text.strip().replace(' ', '')
            words = re.findall(r'\w+', words)

            if len(words) <=2:
                words = words[0] + words[1]
            elif len(words) >= 3:
                words = words[0] + words[1]+words[2]

            print(words+'开始下载')
            self.get_key_ts(links,headerss,words)

            print(words+'下载结束')

    def get_key_ts(self,links,headerss,words):
        """通过正值表达式获取m3u8文件内容中key和ts的url"""
        # 获取m3u8内容
        count = 0
        length = len(links)
        print(length)
        e = 2
        for i in range(len(links)-1):
            # 每个视频的每个m3u8地址请求加睡眠时间
            # time.sleep(0.5)
            m3u8_content = requests.get(url=links[i], headers=headerss).text
            # key的正则匹配
            k = re.compile(r"http://.*?\.key")
            # ts的正则匹配
            t = re.compile(r"http://.*?\.ts")
            # key的url
            key_url = k.findall(m3u8_content)[0]
            # ts的url列表
            ts_urls = t.findall(m3u8_content)
            # 下载key的二进制数据
            key = self.get_key(key_url,headerss)
            # 解密,保存ts文件

            words = words[:-2] + '_' + str(i)
            self.decrypt_save_ts(key,ts_urls,words)
            # if count == 1:
            #     words = words+'_am'
            #     self.decrypt_save_ts(key, ts_urls,words)
            # elif count == 2:
            #     words = words[:-2]+'_pm'
            #     self.decrypt_save_ts(key, ts_urls, words)
            # elif count == 3:
            #     words = words[:-3] + '_aam'
            #     self.decrypt_save_ts(key, ts_urls, words)
            # elif count == 4:
            #     words = words[:-4] + '_ppm'
            #     self.decrypt_save_ts(key, ts_urls, words)
            # else:
            #     print('超限视频未下载')

    def get_key(self, key_url,headerss):
        """功能函数1-下载key的二进制数据"""
        key = requests.get(url=key_url, headers=headerss).content
        return key

    def decrypt_save_ts(self, key, ts_urls,words):
        """功能函数2:解密,保存"""
        # TODO filename 换成自己要存储的目录 .format之后不用换

        directory = 'F:\\danei_video\\video\\{}'.format(words)
        if not os.path.exists(directory):
            os.makedirs(directory)
            # decrypt方法的参数需要为16的倍数，如果不是，需要在后面补二进制"0"

            for ts_url in ts_urls:

                ts_name = ts_url.split("/")[-1]  # ts文件名
                # 解密，new有三个参数，
                # 第一个是秘钥（key）的二进制数据，
                # 第二个使用下面这个就好
                # 第三个IV在m3u8文件里URI后面会给出，如果没有，可以尝试把秘钥（key）赋值给IV
                sprytor = AES.new(key, AES.MODE_CBC, IV=key)

                # 获取ts文件二进制数据
                print("正在下载：" + ts_name)
                # time.sleep(0.3)

                ts = requests.get(url=ts_url, headers=self.headers).content
                # 密文长度不为16的倍数，则添加b"0"直到长度为16的倍数
                while len(ts) % 16 != 0:
                    ts += b"0"
                filename = 'F:\\danei_video\\video\\{}\\{}.mp4'.format(words,words)
                with open(filename, "ab") as file:
                    file.write(sprytor.decrypt(ts))
        else:
            print(words+'已经下载 ！ 请等待下个视频下载')

    def run(self):
        self.login_html()


if __name__ == '__main__':
    danei = Daneispider()
    danei.run()

