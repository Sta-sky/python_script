"""
    环境支撑：
        pip install  paramiko==2.8.1
    
    使用说明：
        执行命令：
        文件上传：
            1、指定本地文件路径
            2、指定文件上传到远程的文件名
        文件下载：
            1、指定文件下载到本地的路径 需要加保存的文件名
                注意： 要使用斜杠  不能用反斜杠
                    eg:
                        正确：E:/test.zip
                        错误：E:\test.zip
            2、指定远程文件路径
"""

import time

detail = \
    """             此程序可以执行以下操作：\n
    ---------------------   SSH    --------------------------------
                1、输入关键字即可执行相应操作
                    m: 对远程主机执行命令
                    p: 上传文件到远程主机
                    d: 下载文件到本地
                    c: 结束退出程序
    ---------------------   SSH    --------------------------------"""

ssh_detail = \
    """             请按照提示连接远程主机\n
    ---------------------   SSH    --------------------------------
                1、输入远程主机ip地址，密码，端口默认为22连接主机；
    ---------------------   SSH    --------------------------------"""



import paramiko


class Ssh(object):
    def __init__(self):
        self.cmd_ssh = None
        self.sftp = None
        self.trans = None

    def check_ip(self):
        flag = True
        server_ip = input('输入主机地址：')
        return flag, server_ip

    def create_ssh_client(self, server_ip, username, passwd, port=22):
        """
        创建一个可以传输文件，执行命令的客户端，并返回
        :return: ssh_client
        """
        print('正在连接，请等待......')
        try:
            # 创建ssh客户端
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(username=username, hostname=server_ip, password=passwd, port=port)
            # 创建命令连接通道
            self.cmd_ssh = ssh.invoke_shell()
            # 创建文件获取通道  创建sftp对象
            self.trans = ssh.get_transport()
            self.sftp = paramiko.SFTPClient.from_transport(self.trans)
            print('客户端创建成功!')
            return True
        except Exception as e:
            print(f'创建客户端出现异常，异常为：{e}')
            return False
        finally:
            print(self.cmd_ssh.recv(1024))

    def exec_cmd(self, cmd):
        """
            param cmd: 执行的命令
        """
        print(f'开始执行{cmd}，请等待....')
        if cmd:
            try:
                cmds = cmd + '\n'
                self.cmd_ssh.send(cmds)
                time.sleep(1)
                print(f"\033[1;32m {self.cmd_ssh.recv(9999).decode('utf-8')}\033[m")
            except Exception as e:
                print(f'终断命令执行失败，失败原因为{e}')
        else:
            raise Exception('执行命令为空为空')

    def put_file(self, local_path, remote_file_name):
        """
        上传文件到远程主机
        :param ssh_client: 客户端对象
        :param local_path: 本地路径
        :param remote_path: 远程路径
        :return:
        """
        print('开始上传，请等待....')
        if local_path and remote_file_name:
            remote_path = f'/home/ubuntu/file/{remote_file_name}'
            try:
                def printTotals(transferred, toBeTransferred):
                    print(f"当前传输进度: {round(transferred / toBeTransferred, 4) * 100}%")
                self.sftp.put(local_path, remote_path,callback=printTotals)
                print(f'\033[4;34m上传成功文件已上传到{remote_path}\033[m')
            except Exception as e:
                print(f'文件上传失败，失败原因：{e}')
        else:
            raise Exception(f'上传路径为空{local_path, remote_file_name}')

    def down_remote_file(self, local_path, remote_path):
        """
        下载文件到本地
        :param ssh_client: 客户端对象
        :param local_path: 本地路径
        :param remote_path: 远程路径
        :return:
        """
        if local_path and remote_path:
            try:
                self.sftp.get(remote_path, local_path)
                print(f'\033[4;34m下载成功，文件已下载到{local_path}\033[m')
            except Exception as e:
                print(e)
                if str(e).find('Errno 13') != -1:
                    print('请定义需要下载的文件名，并添加到路径中')
                if str(e).find('Errno 2') != -1:
                    print('请检查文件路径是否正确')
        else:
            raise Exception(
                f'下载路径为空{local_path, remote_path}')

    def close_client(self):
        """
            执行官远程操作关闭客户端
        """
        try:
            self.cmd_ssh.close()
            self.trans.close()
            print('客户端已关闭')
        except Exception as e:
            raise Exception(f'客户端关闭失败，原因为{e}')


if __name__ == '__main__':
    ssh = Ssh()
    print(f"\033[2;32m {ssh_detail} \033[m")
    flags, server_ip = ssh.check_ip()
    if flags:
        username = "ubuntu"
        passwd = "10793300@dD"
        create_flag = ssh.create_ssh_client(server_ip, username=username, passwd=passwd, )
        if not create_flag:
            print("\033[2;32m 创建失败，请检查ip地址 \033[m")
        else:
            try:
                while True:
                    print(f"\033[2;32m {detail} \033[m ")
                    keyword = input('请输入要执行的操作：')
                    if keyword == 'c':
                        print('程序退出')
                        break
                    elif keyword == 'm':
                        cmds = input('请输入要执行的linux命令：')
                        ssh.exec_cmd(cmd=cmds)
                    elif keyword == 'p':
                        put_local_path = input('请输入需要上传文件的路径:')
                        put_remote_path = input('请输入保存到远程主机得文件名：')
                        res_put = ssh.put_file(put_local_path, put_remote_path)
                    elif keyword == 'd':
                        # 下载文件
                        down_local_path = input('请输下载到本地的路径：')
                        print(type(down_local_path))
                        down_remote_path = input('请输入下载文件的路径：')
                        ret_get = ssh.down_remote_file(down_local_path, down_remote_path)
                    else:
                        print(detail)
                        print('关键字输入有误，请重新输入!')
            except Exception as e:
                print(e)
            finally:
                ssh.close_client()
    else:
        print('ip地址输入错误次数太多，程序退出')
