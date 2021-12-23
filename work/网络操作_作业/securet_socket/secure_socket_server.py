import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
import threading
import time


class AuthenticationError(Exception):
	
	def __init__(self, Errorinfo):
		super().__init__()
		self.errorinfo = Errorinfo
	
	def __str__(self):
		return self.errorinfo


class Server():
	# 用来标记同时连接的客户端的数量
	number = 0
	def __init__(self, backlog=5, addr=('0.0.0.0', 8080)):
		# 创建套接字
		self.serverSocket = socket.socket()
		# 绑定监听的ip地址和端口号
		self.serverSocket.bind(addr)
		# 阻塞监听
		self.serverSocket.listen(backlog)
	
	# 该函数需要并行处理
	def link_one_client(self):
		# 获取客户端对象和客户端地址
		ServerSocket, addr = self.serverSocket.accept()
		Server.number = Server.number + 1 # 客户端数量加1
		now_number = Server.number # 标记当前客户端编号
		print(f"\033[1;31m----和客户端{now_number}建立连接,目标主机地址为：{addr}-----\033[m")
		
		# 运用pickle进行反序列化
		# 服务端接收客户端发来的公钥 并使用pickle进行反序列化
		publicKeyPK, pubKeySha256 = pickle.loads(ServerSocket.recv(1024))
		if hashlib.sha256(publicKeyPK).hexdigest() != pubKeySha256:
			raise AuthenticationError("密钥被篡改！")
		else:
			publicKey = pickle.loads(publicKeyPK)
			print("已接受公钥")
		
		# 产生用于非对称加密的密钥
		sym_key = Fernet.generate_key()
		# 用pickle进行序列化用来进行网络传输
		# 对密钥进行hash保证其准确性
		# 通过客户端的公钥 进行rsa加密， 对加密后的数据进行hash  发送客户端进行验证
		en_sym_key = rsa.encrypt(pickle.dumps(sym_key), publicKey)
		en_sym_key_sha256 = hashlib.sha256(en_sym_key).hexdigest()
		print("\033[1;31m+++++++++正在加密传送密钥+++++++++++\033[m")
		ServerSocket.send(pickle.dumps((en_sym_key, en_sym_key_sha256)))
		
		# 这里可以添加密钥交换成功的函数
		
		# 初始化加密对象
		fernet_obj = Fernet(sym_key)
		# 下面使用对称密钥进行加密对话的过程
		
		while True:
			time.sleep(0.3)
			# 阻塞等待接收消息
			en_recvData = ServerSocket.recv(1024)
			recvData = fernet_obj.decrypt(en_recvData).decode()
			print(f"\033[4;34m接受到客户端{now_number}传来的消息: {recvData}\033[m")
			if recvData == 'stop':
				print('===')
				print(f"\033[1;31m=============和客户端{now_number}退出=============\033[m")
				continue
			# 调用图灵机器人
			sendData = '服务端的消息' + recvData
			# 对消息进行加密
			en_sendData = fernet_obj.encrypt(sendData.encode())
			ServerSocket.send(en_sendData)

if __name__ == '__main__':
	print("\033[6;35m欢迎使用服务端程序！\033[m")
	print("\033[6;35m等待客户端连接......\033[m")
	server = Server()
	while True:
		# 这里使用多线程可以避免服务器阻塞在一个客户端上
		t = threading.Thread(target=server.link_one_client)
		t.start()

