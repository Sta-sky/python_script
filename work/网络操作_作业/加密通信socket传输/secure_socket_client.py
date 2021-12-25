import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib


"""
    环境：
        pip install rsa==4.8
        pip install cryptography==36.0.1
    
    思路：
        客户端和服务器端建立连接
        客户端产生非对称密钥，将公钥传送给服务器端
        服务器端通过公钥将密钥进行加密并传送给客户端
        客户端接收到密钥并进行解密，双方开始通信
    
    加密过程：
        1、客户端使用rsa非对称加密，客户端生成公私钥
        2、将公钥使用hash256加密发与服务端，服务端通过hash256解密，如果hash失败抛出解密异常，正常情况下拿到公钥，
        3、服务端使用公钥，通过rsa再次进行上锁，并使用hash56再次加密，发与客户端
        4、客户端通过hash256解密，如解密失败，抛出异常，正常情况，解密获取信息
        5、通过Fernet以及服务端生成的加密密钥创建加密对象，进行数据传输
"""


class AuthenticationError(Exception):
    def __init__(self, Errorinfo):
        super().__init__()
        self.errorinfo = Errorinfo
    
    def __str__(self):
        return self.errorinfo


class Client:

    def __init__(self):
        # 产生非对称密钥 获取公钥和私钥
        self.asyKey = rsa.newkeys(2048) # 指定加密的数据长度
        self.publicKey = self.asyKey[0]
        self.privateKey = self.asyKey[1]

    def link_server(self, addr=('localhost', 8080)):
        # 创建套接字
        clientSocket = socket.socket()
        # 绑定监听的ip地址和端口号
        clientSocket.connect(addr)

        # 向服务器传递公钥，和该公钥字符串化后的sha256值
        print("\033[1;31m---------------正在向服务器传送公钥---------------\033[m")
        sendKey = pickle.dumps(self.publicKey)
        sendKeySha256 = hashlib.sha256(sendKey).hexdigest()
        clientSocket.send(pickle.dumps((sendKey, sendKeySha256)))

        # 接受服务器传递的密钥并进行解密
        symKey, symKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(symKey).hexdigest() != symKeySha256:
            raise AuthenticationError("密钥被篡改！")
        else:
            self.symKey = pickle.loads(rsa.decrypt(symKey, self.privateKey))
            print("\033[6;35m 连接服务端完成！\033[m")

        # 初始化加密对象
        fernet_obj = Fernet(self.symKey)

        while True:
            sendData = input("输入你要发送的消息：")
            if (sendData == "stop"):
                print("\033[1;31m--------------- 退出服务 Bye! ---------------\033[m")
                break
            en_sendData = fernet_obj.encrypt(sendData.encode())
            clientSocket.send(en_sendData)
            en_recvData = clientSocket.recv(1024)
            recvData = fernet_obj.decrypt(en_recvData).decode()
            print(f"\033[4;34m接受到服务器传来的消息: {recvData}\033[m")
            
if __name__ == '__main__':
    print("\033[6;35m欢迎使用客户端程序！\033[m")
    print("\033[6;35m正在连接服务端，请等待...！\033[m")
    client = Client()
    client.link_server()