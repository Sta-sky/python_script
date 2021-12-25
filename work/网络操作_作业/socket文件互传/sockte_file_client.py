import os
import socket
import struct

save_file = 'C:/client_receive_file/'
if not os.path.exists(save_file):
    os.mkdir(save_file)


class Client:
    def __init__(self):
        # 创建套接字
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定监听的ip地址和端口号
        self.addr = ('localhost', 8080)
        self.client.connect(self.addr)

    def run(self):
        while True:
            filepath = input("请输入文件路径：")
            # 判断是否为文件
            if os.path.isfile(filepath):
                # 定义文件头信息，包含文件名和文件大小
                fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
                # 发送文件名称与文件大小
                self.client.send(fhead)
    
                # 将传输文件以二进制的形式分多次上传至服务器
                fp = open(filepath, 'rb')
                print('正在传输数据,请稍等...')
                while 1:
                    data = fp.read(1024)
                    if not data:
                        print('{0} 数据传输完成...'.format(os.path.basename(filepath)))
                        break
                    self.client.send(data)
               
                print('等待服务端传输文件... ')
                # 申请相同大小的空间存放发送过来的文件名与文件大小信息
                fileinfo_size = struct.calcsize('128sl')
                # 接收文件名与文件大小信息
                buf = self.client.recv(fileinfo_size)
                if buf == "no":
                    continue
                else:
                    self.receive_file(buf)
                    

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
                    data = self.client.recv(1024)
                    recvd_size += len(data)
                else:
                    data = self.client.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
        print('客户端数据接收完成...')



if __name__ == '__main__':
    print("\033[6;35m欢迎使用客户端程序！\033[m")
    print("\033[6;35m正在连接服务端，请等待...！\033[m")
    client = Client()
    client.run()