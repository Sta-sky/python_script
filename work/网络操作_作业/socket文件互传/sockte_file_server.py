import os
import socket
import struct
import time


save_file = 'C:/server_receive_file/'
if not os.path.exists(save_file):
	os.mkdir(save_file)


class Server():
	# 用来标记同时连接的客户端的数量
	number = 0
	
	def __init__(self, backlog=5, addr=('0.0.0.0', 8080)):
		# 创建套接字
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# 绑定监听的ip地址和端口号
		self.serverSocket.bind(addr)
		# 阻塞监听
		self.serverSocket.listen(backlog)
		self.connect, self.addr = self.serverSocket.accept()
		Server.number = Server.number + 1  # 客户端数量加1
		self.now_number = Server.number  # 标记当前客户端编号
		print(f"\033[1;31m----和客户端{self.now_number}建立连接,目标主机地址为：{self.addr}-----\033[m")

	
	def run(self):
		while True:
			time.sleep(0.3)
			try:
				# 申请相同大小的空间存放发送过来的文件名与文件大小信息
				fileinfo_size = struct.calcsize('128sl')
				# 接收文件名与文件大小信息
				buf = self.connect.recv(fileinfo_size)
				# 判断是否接收到文件头信息
				if buf == 'stop':
					continue
				if buf:
					self.receive_file(buf)
				options = input('是否要给客户端传输文件：yes/no?')
				if options == 'yes':
					self.send_file()
				else:
					self.connect.send('no'.encode())
					print('等待客户端发送文件...')
			except Exception as e:
				pass
	
	def send_file(self):
		filepath = input('请输入文件路径：')
		while True:
			if not os.path.isfile(filepath):
				filepath = input('请输入文件路径：')
			else:
				break
		# 定义文件头信息，包含文件名和文件大小
		fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
		# 发送文件名称与文件大小
		self.connect.send(fhead)
		
		# 将传输文件以二进制的形式分多次上传至服务器
		fp = open(filepath, 'rb')
		print('正在传输数据,请稍等...')
		while 1:
			data = fp.read(1024)
			if not data:
				print('{0} 数据传输完成...'.format(os.path.basename(filepath)))
				break
			self.connect.send(data)
	
	def receive_file(self, buf):
		# 获取文件名和文件大小
		filename, filesize = struct.unpack('128sl', buf)
		fn = filename.strip(b'\00')
		fn = fn.decode()
		print('数据名为 {0}, 数据大小为 {1}'.format(str(fn), filesize))
		recvd_size = 0  # 定义已接收文件的大小
		with open(save_file + str(fn), 'wb') as fp:
			print('开始接收客户端数据...')
			# 将分批次传输的二进制流依次写入到文件
			count = 0
			while not recvd_size == filesize:
				count += 1
				if filesize - recvd_size > 1024:
					data = self.connect.recv(1024)
					recvd_size += len(data)
				else:
					data = self.connect.recv(filesize - recvd_size)
					recvd_size = filesize
				fp.write(data)
		print('客户端数据接收完成...')

		
if __name__ == '__main__':
	print("\033[6;35m欢迎使用服务端程序！\033[m")
	print("\033[6;35m等待客户端连接......\033[m")
	server = Server()
	server.run()

