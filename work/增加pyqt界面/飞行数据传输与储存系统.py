import socket

if __name__ == '__main__':
    # 1.创建tcp客户端套接字对象
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2.和服务端应用程序建立连接
    tcp_client_socket.connect(("192.168.4.1", 8086))
    # 代码执行到此，说明连接建立成功
    # 准备发送的数据
    send_data = "start".encode("gbk")
    # 3.发送数据
    tcp_client_socket.send(send_data)
    # 4.接收数据, 这次接收的数据最大字节数是10+24
    i =1
    while i>0:
        recv_data = tcp_client_socket.recv(1024)
        # 返回的直接是服务端程序发送的二进制数据
        # print(recv_data)
        # 对数据进行解码
        recv_content = recv_data.decode("gbk")
        # print("收到的数据：", recv_content)
        with open('数据1.txt', 'a', encoding='utf-8') as f:
            data = recv_content
            plist = list(data)
            plist.pop()
            plist.pop()
            plist.pop(10)
            data_1 = ''.join(plist[:])
            print("保存的数据：", data_1)
            f.write(data_1)
            f.close()
            # 5.关闭套接字
            # tcp_client_socket.close()