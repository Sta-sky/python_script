import asyncio
import requests
import urllib3

#
async def requests_tool(param_url):
    print(param_url)
    retry_times = 20
    retry_count = 0
    for i in range(retry_times):
        retry_count += 1
        try:
            if retry_count > 1:
                print(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
            http_res = requests.get(url=param_url, verify=False, timeout=5)
            http_res.close()
            return http_res
        except Exception as e:
            if retry_count >= retry_times:
                print(f'{param_url},请求失败，原因{e}')
                return False
            else:
                continue


async def baidu_spider():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url_list = [
        'https://www.yzlfxy.com/jiaocheng/python/332440.html',
        'https://blog.csdn.net/weixin_34090643/article/details/89443762',
        'https://blog.csdn.net/whatday/article/details/106885916'
    ]

    task_list = [
        requests_tool(url) for url in url_list
    ]

    respose = await asyncio.wait(task_list)
    return respose


async def parse(task_obj):
    print(task_obj, '[[[[[[[[[[')
    return None

done, padding = asyncio.run(baidu_spider())







