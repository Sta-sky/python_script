import requests
import os
from lxml import etree
import time
import fake_useragent

"""
    环境:
        python版本：3.7.8
        依赖包：
            lxml == 4.5.2
            fake_useragent == 0.1.11
            requests == 2.25.1
            

    spider_img.py:
        get_img:
            1、查看网页 获取主页的地址，根据规律翻页index + 1, 从而确定base_url，循环爬取十页
            2、获取使用fake_user_agent生成chrome请求头
            3、获取图片a标签的src，拼接成图片请求地址，并请求图片数据，
            4、存储本地
"""


def get_image():
    
    base_url = 'https://pic.netbian.com/index_{}.html'  # 网页地址
    dir_name = "spider_img"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    ua = fake_useragent.UserAgent()
    # 指定chrome浏览头，
    headers = { 'User-Agent': ua.chrome }
    
    # 爬取10页
    count = 0
    for page in range(2, 12):
        url = base_url.format(page)
        res = requests.get(url, headers=headers).text
        # xpath解析
        html_ = etree.HTML(res)
        # get src  图片地址
        for index in range(1, 21):  # 遍历hrefs 拼接地址
            count += 1
            print(f'正在保存第{count}张图片')
            img_xpath = "//*[@id='main']/div[3]/ul/li[{}]/a/img/@src".format(index)
            href = html_.xpath(img_xpath)[0]
            
            # 完整地址
            address = 'https://pic.netbian.com' + href
            # 请求图片数据
            imgData = requests.get(address).content
            with open(f"{dir_name}/{count}.jpg", "wb")as f:  # 保存图片
                f.write(imgData)
            count += 1
        time.sleep(0.5) # 0.5后去请求


if __name__ == '__main__':
    get_image()