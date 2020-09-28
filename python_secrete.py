"""
python的内置库hashlib，hmac + 外部库PyCrypto实现各种加密解密算法

Python2.5之前的版本所提供的加密模块有：md5、sha和hmac
Python2.5开始把对md5和sha算法的实现整合到一个新的模块：hashlib；
Python3.x开始去掉了md5和sha模块，仅剩下hashlib和hmac模块；
Python3.6增加了一个新的可以产生用于密钥管理的安全随机数的模块：secrets。

HASH： 一般翻译为“散列”（也有直接音译为“哈希”）
MD5： 全称为 Message Digest algorithm 5，即信息摘要算法。
    该算法可以生成定长的数据指纹，被广泛应用于加密和解密技术
SHA： 全称为 Secure Hash Algorithm，即安全散列算法/安全哈希算法。
    该算法是数字签名等密码学应用中的重要工具
HMAC： 全称为 Hash Message Authentication Code，
    即散列消息鉴别码。HMAC是基于密钥的哈希算法认证协议，主要是利用哈希算法

"""
import base64
import hashlib
import hmac
import secrets
import string

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from log_util import Log

logger = Log('secrete').print_info()

876562995
def generate_base64(keywords):
    """
    base64 编码
        # base64穿入的参数只能是字节串  要用encode()参数进行转换
    # base64的编码
    """
    try:
        res = base64.b64encode(keywords.encode()).decode()
        return res
    except Exception as e:
        logger.error(f'base64生成失败，失败原因为{e}')


def decrypt_base64(keywords):
    """
    :param keywords: 编码后的关键字，str类型
    :return: 
    """
    try:
        resutl = base64.b64decode(keywords).decode()
        return resutl
    except Exception as e:
        logger.error(f'base64解码失败，失败原因为{e}')


def generate_hamc(keywords, secrete_type='md5', salt=None):
    """
    hashlib / hmac 的单向加密
    type:  md5, sha256,
    """
    if not salt:
        if keywords and secrete_type == 'md5':
            # MD5
            try:
                passwd_md5 = hashlib.md5(keywords.encode()).hexdigest()
                return passwd_md5
            except Exception as e:
                logger.error(f'hamc的md5密码生成失败。关键字为{keywords},失败原因为{e}')
        # sha256
        if keywords and secrete_type == 'sha256':
            try:
                passwd_sha256 = hashlib.sha256(keywords.encode()).hexdigest()
                return passwd_sha256
            except Exception as e:
                logger.error(f'hamc的sha256密码生成失败。关键字为{keywords},失败原因为{e}')
    else:
        # hamc的加盐方式加密  key 跟msg都需要字节串
        if keywords:
            try:
                passwd_sha256 = hmac.new(
                    key=keywords.encode('utf-8'),
                    msg=salt.encode('utf-8'), digestmod=secrete_type).hexdigest()
                return passwd_sha256
            except Exception as e:
                logger.error(f'hamc的sha256密码生成失败。关键字为{keywords},失败原因为{e}')


def generate_hashlib(keywords, secrete_type):
    # hashlib的sha256
    if keywords and secrete_type == 'sha256':
        try:
            passwd_sha256 = hashlib.sha256(keywords.encode()).hexdigest()
            return passwd_sha256
        except Exception as e:
            logger.error(f'hashlib的sha256密码生成失败。关键字为{keywords},失败原因为{e}')


def generate_safe_link(url, params):
    """
    secrets  产生随机秘钥模块 产生安全链接：token_urlsafe
        secrets.choise ： 随机选取一个值
        string.ascii_letters ： 26个英文字母的大写加小写  共52个，
        string.digits ： 阿拉伯数字 0-9
        logger.info(secrets.token_hex())# 返回一个包含n个bytes的16进制随机文本字符串，每个字节转换成两个16进制数字，一般用来生成随即密码
        logger.info(secrets.token_bytes()) # 返回一个包含n个bytes的随机字符串
    """
    if params == 'get_random_secrete':
        try:
            sinum = string.ascii_letters + string.digits
            passwd = ''.join(secrets.choice(sinum) for i in range(10))
            return passwd
        except Exception as e:
            logger.error(f'获取随机秘钥失败，原因为{e}')
    if params == 'get_safe_url' and url:
        url_ = secrets.token_urlsafe()
        logger.info(url_)
        return url.format(url_)


"""
pycrypt 模块介绍，加密，解密一段数据
需要注意的是，pycrypto模块最外层的包（package）不是pycrypto，而是Crypto。
它根据加密方式类别的不同把各种加密方法的实现分别放到了不同的子包（sub packages）中，
且每个加密算法都是以单独的Python模块（一个.py文件）存在的
"""


def generate_pycrypt_aes(salt_key, secrete_data, iv_params):
    """
        pycrypt模块的AES加密
        使用AES算法加密，
    :param secrete_key: 自定义的salt值  长度必须是16的倍数
    :param secrete_data: 要加密的数据，长度必须是16的倍数
    :param iv_params: IV参数， 长度必须是16的倍数
    :return:
    """
    # 数据加密
    try:
        aesl_init = AES.new(salt_key.encode(), AES.MODE_CBC, iv_params.encode())
        aes_passwd = aesl_init.encrypt(secrete_data.encode())
        logger.info('加密后的数据 ： %s' % aes_passwd)
        return aes_passwd
    except Exception as e:
        logger.error(f'数据加密失败，失败的数据为{secrete_data}，失败原因为{e}')


def decrypt_pycrypt_aes(salt_key, passwd_bytes, iv_params):
    # 解密数据
    decrypt_secrete = None
    try:
        aesl_init_2 = AES.new(salt_key.encode(), AES.MODE_CBC, iv_params.encode())
        decrypt_secrete = aesl_init_2.decrypt(passwd_bytes)
        return decrypt_secrete
    except Exception as e:
        logger.error(f'数据解密失败，失败的数据为{decrypt_secrete}，失败原因为{e}')



def generate_pub_rsa_key():
    """
        使用RSA算法生成密钥对儿
    :return:
    """
    # 获取一个伪随机数生成器
    random_generate = Random.new().read
    logger.info(random_generate)
    # 获取一个rsa算法对应的秘钥对生成器实例
    rsa = RSA.generate(1024, random_generate)
    logger.info(rsa)
    # 生成私钥并保存
    private_pem = rsa.exportKey()
    with open('rsa.key', 'w') as f:
        f.write(private_pem.decode())

    # 生成公钥并保存
    public_pem = rsa.publickey().exportKey()
    with open('rsa.pub.key', 'w') as f:
        f.write(public_pem.decode())


"""
用法  随机生成一个数字，用用户本地的私钥，将用户上传的公钥，
传入私钥解密所需要的参数中，查看与生成的随机数是否相等；
"""


def user_pub_add_salt(txet, user_secrete):
    """
        公钥加密
    :param txet: 公钥文件的read()后的io对象
    :param user_secrete: 自定义的salt
    :return: 公钥跟salt加密后的秘钥对
    """
    try:
        public_key = txet.read()
        rsa_key_obj = RSA.importKey(public_key)
        passwd_obj = PKCS1_v1_5.new(rsa_key_obj)
        passwd_text = base64.b64encode(
            passwd_obj.encrypt(user_secrete.encode()))
        return passwd_text
    except Exception as e:
        logger.error(f'公钥生成秘钥对失败，失败原因为{e}')


def decrypt_rsa(txet, Key_Pair):
    """
    私钥解密
    :param txet: 私钥文件read()后的io对象
    :param Key_Pair:  生成的秘钥对
    :return: 使用私钥解密后的salt
    """
    try:
        rsa_key_data = txet.read()
        # 创建私钥对象
        rsa_key_obj = RSA.importKey(rsa_key_data)
        passwd_rsa_data = PKCS1_v1_5.new(rsa_key_obj)
        random_generate = Random.new().read
        logger.info(random_generate)
        passwd_rsa_text = passwd_rsa_data.decrypt(base64.b64decode(Key_Pair),
                                                  random_generate)
        return passwd_rsa_text
    except Exception as e:
        logger.error(f'私钥解密失败，失败原因为{e}')



"""
hashlib	Y	主要提供了一些常见的单向加密算法（如MD5，SHA等），每种算法都提供了与其同名的函数实现。
hmac	Y	提供了hmac算法的实现，hamc也是单向加密算法，但是它支持设置一个额外的密钥(通常被称为'salt')来提高安全性
random	Y	该模块主要用于一些随机操作，如获取一个随机数，从一个可迭代对象中随机获取指定个数的元素。
secrets	Y	这是Python 3.6中新增的模块，用于获取安全随机数。
base64	Y	该模块主要用于二进制数据与可打印ASCII字符之间的转换操作，它提供了基于Base16, Base32, 和Base64算法以及实际标准Ascii85和Base85的编码和解码函数。
pycrypto	N	支持单向加密、对称加密和公钥加密以及随机数操作，这是个第三方模块，需要额外安装。

pycryto模块不是Python的内置模块，它的官方网站地址是这里。pycrypto模块是一个实现了各种算法和协议的加密模块的结合，
提供了各种加密方式对应的多种加密算法的实现，包括 单向加密、对称加密以及公钥加密和随机数操作。而上面介绍的hashlib
和hmac虽然是Python的内置模块，但是它们只提供了单向加密相关算法的实现，如果要使用对称加密算法（如, DES，AES等）
或者公钥加密算法我们通常都是使用pycryto这个第三方模块来实现。
"""
