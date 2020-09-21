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

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from log_test import Log
logger = Log('secrete').print_info()
logger.info(__name__)

logger.info(
    '========================================================================================================================================')
"""
base64 编码
"""
# base64穿入的参数只能是字节串  要用encode()参数进行转换
# base64的编码
# st = 'hello world!'.encode()  # 默认以utf8编码
res = base64.b64encode('hello world!'.encode())
logger.info(res)
logger.info(res.decode())  # 默认以utf8解码
# base64的解密
_str = base64.b64decode(res)
logger.info(_str.decode())

logger.error(
    '========================================================================================================================================')
"""
hashlib / hmac 的单向加密
"""
# hashlib的md5
s = 'fdsa'
passwd = hashlib.md5(s.encode()).hexdigest()
logger.info(passwd)

# hashlib的sha256
pss = hashlib.sha256(s.encode()).hexdigest()
logger.info(pss)

# hamc的加密  key 跟msg都需要字节串
dex = 'dyy'
strs = '1234'
passwd = hmac.new(key=strs.encode('utf-8'), msg=dex.encode('utf-8'),
                  digestmod='md5')
logger.info(passwd.hexdigest())

logger.info(
    '========================================================================================================================================')
"""
secrets  产生随机秘钥模块 产生安全链接：token_urlsafe
    secrets.choise ： 随机选取一个值
    string.ascii_letters ： 26个英文字母的大写加小写  共52个，
    string.digits ： 阿拉伯数字 0-9
"""
sinum = string.ascii_letters + string.digits
passwd = ''.join(secrets.choice(sinum) for i in range(10))
# print(passwd)

url_ = 'https://www.dyy.com?res={}'.format(secrets.token_urlsafe())
logger.info(secrets.token_hex())
logger.info(secrets.token_bytes())
logger.info(url_)

logger.info(
    '========================================================================================================================================')
"""
pycrypt 模块介绍，加密，解密一段数据

需要注意的是，pycrypto模块最外层的包（package）不是pycrypto，而是Crypto。
它根据加密方式类别的不同把各种加密方法的实现分别放到了不同的子包（sub packages）中，
且每个加密算法都是以单独的Python模块（一个.py文件）存在的
"""
# pycrypto使用实例
# 实例1： 使用SHA256算法加密
hash = SHA256.new()
hash.update('defd'.encode())
digest = hash.hexdigest()
logger.info(digest)

# 实例2： 使用AES算法加密，解密一段数据
# 定义需要加密的秘钥 长度必须是16的倍数
secrete_key = 'dangyuanyangdang'
# 要加密的明文数据，长度必须是16的倍数
secrete_data = '1234123412341234'
# IV参数， 长度必须是16的倍数
iv_params = '2345234523452345'

# 数据加密
aesl_init = AES.new(secrete_key.encode(), AES.MODE_CBC, iv_params.encode())
data = aesl_init.encrypt(secrete_data.encode())
logger.info('加密后的数据 ： %s' % data)

# 解密数据
aesl_init_2 = AES.new(secrete_key.encode(), AES.MODE_CBC, iv_params.encode())
data_2 = aesl_init_2.decrypt(data)
logger.info("解密后的数据%s" % data_2)


# 实例3：使用RSA算法生成密钥对儿
def generate_pub_rsa_key():
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


# 公钥加密，私钥解密
"""
用法  随机生成一个数字，用用户本地的私钥，将用户上传的公钥，
传入私钥解密所需要的参数中，查看与生成的随机数是否相等；
"""
def user_pub_add_salt():
    user_secrete = 'dyy107933'
    with open('rsa.pub.key', 'r') as f:
        public_key = f.read()
        rsa_key_obj = RSA.importKey(public_key)
        passwd_obj = PKCS1_v1_5.new(rsa_key_obj)
        passwd_text = base64.b64encode(passwd_obj.encrypt(user_secrete.encode()))
        logger.info('生成的私钥对：%s ' % passwd_text.decode())
        return passwd_text


# Key_Pair 生成的秘钥对
def decrypt_rsa(Key_Pair):
    with open('rsa.key', 'r') as f:
        rsa_key_data = f.read()
        # 创建私钥对象
        rsa_key_obj = RSA.importKey(rsa_key_data)
        passwd_rsa_data = PKCS1_v1_5.new(rsa_key_obj)
        random_generate = Random.new().read
        logger.info(random_generate)
        passwd_rsa_text = passwd_rsa_data.decrypt(base64.b64decode(Key_Pair),
                                                  random_generate)
        logger.info("解密后的秘钥 ： %s" % passwd_rsa_text.decode())
        return passwd_rsa_text

# 生成公私钥文件
generate_pub_rsa_key()

# 用户添加自定义的盐 跟公钥中的文件，使用加密算法生成一个秘钥对
key_pair = user_pub_add_salt()

# 服务器通过私钥与秘钥对，解密出用户自定义的盐值，来判断是否是同一个用户
decrypt_key = decrypt_rsa(key_pair)



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

