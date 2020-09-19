"""
paramiko包含两个核心组件：SSHClient和SFTPClient。
SSHClient的作用类似于Linux的ssh命令，是对SSH会话的封装，该类封装了传输(Transport)，通道(Channel)及SFTPClient建立的方法(open_sftp)，通常用于执行远程命令。
SFTPClient的作用类似与Linux的sftp命令，是对SFTP客户端的封装，用以实现远程文件操作，如文件上传、下载、修改文件权限等操作。
"""
import datetime
import re
import sys
import time

import paramiko



class Ssh(object):
    def __init__(self):
        self.transport = None
        self.channel = None

    def return_clent(self, server_ip, username, passwd, port=22, ):
        """
        创建返回一个ssh安全连接对象
        :return:
        """
        ssh_client = {}
        try:
            # 创建一个加密通道
            self.transport = paramiko.Transport((server_ip, port))
            self.transport.start_client()

            # 密码认证方式
            self.transport.auth_password(username=username, password=passwd)

            # 打开一个通道
            self.channel = self.transport.open_session()
            self.channel.settimeout(5)

            # 获取一个终端
            self.channel.get_pty()
            # 激活器
            self.channel.invoke_shell()
            ssh_client['transport'] = self.transport
            ssh_client['channel'] = self.channel
            return ssh_client
        except Exception as e:
            print(f"创建ssh客户端失败， 失败ip为{server_ip}， 失败原因为{e}")


    def send_cmd(self, cmd, ssh_client, timeout = None, retry_times=5):
        result = ''
        # 发送要执行的命令
        try:
            channel = ssh_client['channel']
            channel.send(cmd)
            # 回显很长的命令可能执行较久，通过循环分批次取回回显
            ret_str = ''
            # 通过命令执行提示符来判断命令是否执行完成
            now_time = datetime.datetime.now()
            print(now_time)
            for retry_time in range(retry_times):
                while not re.search("last cmd result: \d+", ret_str):
                    print('------------------')
                    time.sleep(0.1)
                    print(ssh_client['channel'].closed)
                    # 如果客户端通道关闭了
                    if ssh_client['channel'].closed:
                        print('客户端是关闭状态')
                        raise Exception('客户端是关闭的')
                    print(datetime.datetime.now(),
                          now_time + datetime.timedelta(
                              minutes=int(timeout)))
                    if datetime.datetime.now() > now_time + datetime.timedelta(
                            minutes=int(timeout)):
                        raise Exception('已超过最大超时时间')
                    if not ssh_client['channel'].recv_ready():
                        continue
                    print(ret_str)
                    try:
                        ret_str = ret_str + ssh_client['channel'].recv(
                            65535).decode('utf-8')

                        # return ret_str
                    except Exception as e:
                        ret_str = ret_str.replace(' \r', '\r')
                        ret_str + ret_str.replace('\r', '')
                        ret_str + ret_str.replace(';echo last cmd result: '
                                                  '$?', '')
                        print(f'在主机上执行命令发生错误{e}')
                        continue
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    print(ret_str)
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    ret_str = ret_str.replace(' \r', '\r')
                    ret_str = ret_str.replace('\r', '')
                    ret_str = ret_str.replace(";echo last cmd result: $?", "")
                ret_str = ret_str.replace(ssh_client.get('prompt', ''), '')
                ret_str = ret_str.replace('\n\n', '\n')
                ret_str = ret_str.replace('\n', '\n\r')
                listout = ret_str.split('\r')
                print('[[[[[[[[[[[[[[[[[')
                print(listout)
                if not listout:
                    return listout

                if 0 != len(listout[0]):
                    listout = listout[1:]
                if listout and 0 != len(listout[-1]):
                    listout = listout[:-1]
                print("execute ssh_exec_command_return success.")
                return listout
        except Exception as e:
            print(e)




    @staticmethod
    def exc_cmd(trans, cmds):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client._transport = trans
            stdio, stdout, stderr = ssh_client.exec_command(cmds)
            print(bytes(stdout.read()).decode())
        except Exception as e:
            print(f"执行失败，失败原因{e}")


server_ip = '49.234.158.144'
username = 'dyy'
passwd = '107933'
cmds = 'p; echo last cmd result: $?\n'
timeout = 1

ssh = Ssh()
ssh_client = ssh.return_clent(server_ip, username, passwd)
print(ssh_client)
try:
    if ssh_client:
        res = ssh.send_cmd(cmds, ssh_client, timeout=timeout)

except Exception as e:
    print(e)

