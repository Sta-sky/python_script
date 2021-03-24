import os
import IPy
import time
import jwt
import requests
import xlwt
from log_util import Log

CODING_LIST = ['UTF-8', 'GBK', 'ISO-8859-1']
logger = Log('tool_fun').print_info()
SALT_KEY = 'PXU9@ctuNov20!'


def change_str(args):
    if args and isinstance(args, bytes):
        for coding in CODING_LIST:
            try:
                return args.decode(encoding=coding)
            except UnicodeDecodeError:
                logger.error('字符串转换错误')
        logger.error("transfer bytes to str error: %s" % args)
        return args
    elif isinstance(args, list):
        return [change_str(coding) for coding in args]
    elif isinstance(args, dict):
        return {change_str(key): change_str(val) for key, val in args.items()}
    else:
        return args


def is_ipv4_address(ip):
    if ip:
        try:
            res = IPy.IP(ip)
            print(res)
            return True
        except Exception as e:
            print(e, 'cdsaca=====')
            return False


def generate_token(username, exp=3600 * 24):
    """
    过期时间为一天
    :param salt: 加盐值
    :param exp: 过期时间
    :return:
    """
    key = SALT_KEY
    now = time.time()
    payload = {'username': username, 'exp': exp + now}
    return change_str(jwt.encode(payload=payload, key=key, algorithm='HS256'))


def time_tool(times=0):
    count = 0
    print('进入线程')
    for i in range(times):
        count += 1
        print('已等待：%s 秒,还剩：%s' % (count, times - count))
        time.sleep(1)

s = generate_token('cd')
print(s)


def save_xml(data, fields):
    """
    传入一个如下格式的数据，
        data格式为data[
            [count, name,age],
            [count, name,age]
        ]
        fields格式为：[序号，姓名，年龄]
    保存xml表格, 路径，文件名可自定义，
    :param data:
    :param fields:
    :return:
    """
    file_save_path = 'G:\\MAT\\video\\{}'
    work = xlwt.Workbook(encoding='utf-8')
    sheet = work.add_sheet('video')
    for num in range(len(fields)):
        sheet.write(0, num, fields[num])

    for row in range(1, len(data) + 1):
        for col in range(len(fields)):
            lists_res = data[row - 1][col]
            print(lists_res)
            sheet.write(row, col, lists_res)
    file_name = 'video.xml'
    file_path = file_save_path.format(file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    work.save(file_path)
    print('保存成功')


def return_requests_data(param_url):
    """
    requests 请求工具，最大请求数20次
    param_url : 需要请求的单个地址，
    """
    retry_times = 20
    retry_count = 0
    for i in range(retry_times):
        retry_count += 1
        try:
            if retry_count > 1:
                print(f'重试第{retry_count - 1}次请求，当前请求地址为{param_url}请等待...')
            http_res = requests.get(url=param_url, verify=False, timeout=10)
            return http_res
        except Exception as e:
            if retry_count >= retry_times:
                raise Exception(f'{param_url},请求失败，原因{e}')
            else:
                continue


def time_wappre(func):
    """
    函数执行时间装饰器
    """
    def rewappre(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'文件执行了{"%.2f" % (end_time - start_time)}秒')
        return result
    return rewappre

