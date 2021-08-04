import requests
from tool.python_secrete import decrypt_rsa
from tool.log_util import Log
from tool.util import change_str

logger = Log('request').print_info()

# 私钥地址
rsa_filename = 'C:\\Users\\Administrator\\Desktop\\Python\\flask\\flask_test\\rsa.key'
# 登录请求，获取密钥对的地址
url = 'http://49.234.158.144:8001/user/login'
# 通过私钥跟密钥对，解除的盐值返回服务器，检查登录的地址；
url_1 = 'http://49.234.158.144:8001/user/checklogin'


def get_rsa_secrete():
    """
    发送登录请求，获取服务器用公钥产生的密钥对；
    """
    token = None
    secrete_key = None
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
    """
    再次发送请求， 携带用私钥以及密钥对解开的盐值，验证登录
    """
    data_info = None
    try:
        with open(rsa_filename, 'r') as fp:
            decrypt_key = change_str(decrypt_rsa(fp, secrete_key))
        data_info = {'decrypt_key': decrypt_key}
    except Exception as e:
        print(f'使用私钥解密失败，原因为{e}，请查看原因')

    header = {
        'Accept': 'application/json;version=2.2;charset=UTF-8',
        'iBaseToken': token,
        'Accept-Language': 'en',
    }
    method = 'GET'
    status_code, get_rsp = send_a_request(urls=url_1, method=method,
                                          headers=header, data=data_info)

    if get_rsp['msg'] == '登录成功' and status_code == 200:

        logger.info('登陆信息为 %s,登录返回状态码为：%d' % (get_rsp['msg'], status_code))
    else:
        logger.error(f'登录失败。失败状态码为{status_code}, ')



def send_a_request(urls, method, headers=None, data=None):
    """
    负责发送请求，返回请求响应的数据，以及状态码
    """
    try:
        if urls and method:
            if method == 'GET':
                rsp = requests.get(urls, headers=headers, data=data)
                data = rsp.json()
                if rsp.status_code == 200:
                    return_code = rsp.status_code
                    return return_code, data
                else:
                    return rsp.status_code, data
    except Exception as e:
        print(f'地址请求发送失败，原因为{e}，失败地址为{urls},请查看原因')

if __name__ == '__main__':
    secrete_key, token = get_rsa_secrete()
    send_key_check_login(secrete_key, token)

"""
服务端生成一对公私钥文件，通过生成的公钥与配置的加密salt，生成一个加密的秘钥，
客户端通过获取密码，使用私钥进行解密，解密出来的传回服务端，进行与设置的salt进行验证，
如果相同验证成功，不相同则失败，验证不通过；
"""
