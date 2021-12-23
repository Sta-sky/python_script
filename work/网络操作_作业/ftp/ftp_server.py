# 搭建FTP服务器

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket                        # 主要用于获取当前主机IP地址


def ftp_server():
	
	# 1. 添加授权用户
	authorizer = DummyAuthorizer()
	# 添加非匿名用户, 各项分别代表: 用户名, 密码, 用户根目录, 用户权限
	authorizer.add_user('Administrator', '123456', 'D:\\', 'elradfmwM')
	# 添加匿名用户, 各项分别代表: 匿名用户根目录
	authorizer.add_anonymous('./')
	
	# 2. 更改FTP处理器的授权用户属性(归属于"类属性")
	handler = FTPHandler
	handler.authorizer = authorizer
	
	# 3. 通过主机名与端口号实例化FTP服务器, 并启动
	server = FTPServer(("0.0.0.0", 9999), handler)
	server.serve_forever()
	
if __name__ == '__main__':
	ftp_server()