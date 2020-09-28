import os

import requests
from python_secrete import decrypt_rsa
from bytes_to_str import change_str
from log_util import Log

logger = Log('request').print_info()


def get_rsa_secrete():
    token = None
    secrete_key = None
    url = 'http://127.0.0.1:5001/user/login'
    method = 'GET'
    status_code, data = send_a_request(url, method=method)
    logger.info((status_code, data))
    if status_code == 200:
        for key, val in data.items():
            if key == 'secrete':
                secrete_key = val
            if key == 'token':
                token = val
    else:
        logger.error(f'get rsa secrete failed, status_code{status_code}')

    return secrete_key, token


def send_key_check_login(secrete_key, token):
    # rsa_filename = os.path.realpath('../flask_test/rsa.key')
    rsa_filename = 'C:\\Users\\Administrator\\Desktop\\Python\\flask\\flask_test\\rsa.pub.key'
    with open(rsa_filename, 'r') as fp:
        decrypt_key = change_str(decrypt_rsa(fp, secrete_key))
    print(decrypt_key)
    data_info = {'decrypt_key': decrypt_key}

    header = {
        'Accept': 'application/json;version=2.2;charset=UTF-8',
        'iBaseToken': token,
        'Accept-Language': 'en',
    }
    urls = 'http://127.0.0.1:5001/user/checklogin'
    method = 'GET'
    status_code, get_rsp = send_a_request(urls=urls, method=method,
                                          headers=header, data=data_info)
    logger.info(get_rsp['msg'])
    logger.info(status_code)


def send_a_request(urls, method, headers=None, data=None):
    if urls and method:
        if method == 'GET':
            rsp = requests.get(urls, headers=headers, data=data)
            if rsp.status_code == 200:
                return_code = rsp.status_code
                data = rsp.json()
                return return_code, data
            else:
                return rsp.status_code, data.json()


if __name__ == '__main__':
    secrete_key, token = get_rsa_secrete()
    send_key_check_login(secrete_key, token)

"""
服务端生成一对公私钥文件，通过生成的公钥与配置的加密salt，生成一个加密的秘钥，
客户端通过获取密码，使用私钥进行解密，解密出来的传回服务端，进行与设置的salt进行验证，
如果相同验证成功，不相同则失败，验证不通过；
"""
