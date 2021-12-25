# 搭建FTP客户端
from ftplib import FTP

"""
	使用说明：
	
		2、命令 i 说明
			进入 i 指令后：
				1、 输入 .. 表示进入当前目录的父目录中
				2、输入目录名进入指定目录中
				3、可以多级输入 test1/test2/test3 直接进入test3目录中
	
		2、下载文件 d 说明：
			1、再当前展示的目录中输入要下载的文件名
			2、输入要保存的目标地址 + 文件名
				例如下载: test.png
				    1、输入远程文件名: test.png
				    2、输入本地文件路径：E:/info.png
				此过程为将远程的test.png下载到本地E:/下 命名为info.png
				
		3、上传文件 p 说明：
				例如: 上传当前目录下的 test.png
				    1、输入本地文件路径：E:/test_1.txt
				    2、输入保存到远程文件名: test_2.txt
				此过程为将本地的 test_2.txt 上传到 text_1.txt
		4、退出 q
"""


detail = """    输入提示
		文件下载：d
		文件上传：p
		进入目录：i
		退出：   q
"""


class FtpClient():
	def __init__(self):
		self.ftp = FTP()

	
	def connect_ftp(self):
		# 实例化FTP对象, 并连接
		self.ftp.connect("192.168.1.22", 9999)
		# username = input('请输入用户名： ')
		# username = input('请输入密码： ')
		self.ftp.login("Administrator", "123456")
		
	def enter_dir(self, cmd):
		try:
			self.ftp.cwd(cmd)
		except Exception as e:
			print(f'\033[6;35m 目录不存在，错误信息{e}\033[m')
	
	def down_file(self, remote_file, local_file):
		# 下载文件
		try:
			file_path = self.ftp.pwd() + "/" + remote_file
			print(file_path)
			self.ftp.retrbinary(f"RETR {file_path}", open(local_file, 'wb').write)
			print("\033[1;32m文件下载成功\033[m")
		except Exception as e:
			print(f'\033[6;35m请检查目录是否正确，错误信息{e}\033[m')
		
	def upload_file(self, remote_file, local_file):
		# 上传文件
		try:
			self.ftp.storbinary(f"STOR {remote_file}", open(local_file, 'rb'))
			print("\033[1;32m文件上传成功\033[m")
		except Exception as e:
			print(f'\033[6;35m请检查目录是否正确，错误信息{e}\033[m')
	
			
	def run(self):
		self.connect_ftp()
		self.ftp.cwd('.')
		while True:
			self.ftp.dir()
			print(f'\033[2;32m{detail}\033[m')
			res = input('\033[4;34m 请输入选项:\033[m')
			if res == 'd':
				remotename = input('\033[4;34m输入远程文件名:\033[m')
				file = input('\033[4;34m输入本地文件路径\033[m')
				self.down_file(remotename, file)
			elif res == 'p':
				remotename = input('\033[4;34m输入保存到远程文件名:\033[m')
				file = input('\033[4;34m输入本地文件路径：\033[m')
				self.upload_file(remotename, file)
			elif res == 'i':
				dir = input('\033[4;34m请输入要进入的文件夹：\033[m')
				self.enter_dir(dir)
			elif res == 'q':
				break
			else:
				print('输入有误，请重新输入！')
				continue
		self.quit()
		print('\033[4;34m----Bye----\033[m')
		
	def quit(self):
		# 4. 退出
		self.ftp.close()


if __name__ == '__main__':
	ftp_obj = FtpClient()
	ftp_obj.run()
 
