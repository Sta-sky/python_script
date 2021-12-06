"""
SFTP：
    上传文件：
        不需要创建客户端，只需要打开通道【Transport】再创建sftp的客户端，
    下载文件：
        需要创建ssh客户端【SSHClient】，通过ssh客户端获取通道实例【trans = ssh_client.get_transport】
        最后创建sftp客户端，将通道传入，使用get()下载文件
    问题：
        是否可以使用下载文件中的sftp对象上传文件，相反，是否也成立
    验证结果 成立都可以使用
"""
from tool.log_util import Log
from tool.util import is_ipv4_address

detaile = \
    """此程序可以执行一下操作\n
    ---------------------   SSH    --------------------------------
                1、输入关键字即可执行相应操作
                    cmd: 对远程主机执行命令
                    put: 上传文件到远程主机
                    down: 下载文件到本地
                    c: 结束退出程序
    ---------------------   SSH    --------------------------------"""

ssh_detaile = \
    """请按照提示连接远程主机\n
    ---------------------   SSH    --------------------------------
                1、输入远程主机ip地址，密码，端口默认为22连接主机；
    ---------------------   SSH    --------------------------------"""

import paramiko

log_sing = 'ssh'
logger = Log(log_sing).print_info()


class Ssh(object):
    def __init__(self):
        print(self.__class__.__name__)

    def check_ip(self):
        ip = ''
        flag = False
        for count in range(3):
            server_ip = input('输入主机地址：')
            if not is_ipv4_address(server_ip):
                continue
            else:
                flag = True
                break
        return flag, server_ip

    def create_ssh_client(self, server_ip, username, passwd, port=22):
        """
        创建一个可以传输文件，执行命令的客户端，并返回
        :return: ssh_client
        """
        ssh_client = {}
        print('正在连接，请等待......')

        try:
            # 创建ssh客户端
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(username=username, hostname=server_ip, password=passwd,
                        port=port)
            # 创建通道
            ssh.invoke_shell()
            trans = ssh.get_transport()

            # 创建sftp对象
            sftp = paramiko.SFTPClient.from_transport(trans)
            ssh_client['ssh_client'] = ssh
            ssh_client['trans'] = trans
            ssh_client['sftp'] = sftp
            print('客户端创建成功!')
            return ssh_client
        except Exception as e:
            print(f'创建客户端出现异常，异常为：{e}')

    def exec_cmd(self, ssh_client, cmd):
        """
        执行命令，并返回状态码
        :param ssh_client: ssh客户端对象
        :param cmd: 执行的命令
        :return:
        """
        print(f'开始执行{cmd}，请等待....')
        if cmd and ssh_client:
            try:
                stdin, stdout, stderr = \
                    ssh_client['ssh_client'].exec_command(cmd)
                print(stdout.read().decode('utf-8'))
                cmd_status = stdout.channel.recv_exit_status()
                print(cmd_status)
                if cmd_status != 0:
                    raise Exception(f'执行命令为：{cmd}状态码为：{cmd_status}')
                print('命令执行完的状态为：', cmd_status)
                return cmd_status
            except Exception as e:
                print(f'终断命令执行失败，失败原因为{e}')
        else:
            raise Exception(
                f'执行命令为空{cmd}或客户端为空')

    def put_file(self, ssh_client, local_path, remote_path):
        """
        上传文件到远程主机
        :param ssh_client: 客户端对象
        :param local_path: 本地路径
        :param remote_path: 远程路径
        :return:
        """
        print('开始上传，请等待....')
        if local_path and remote_path and ssh_client:
            try:
                res = ssh_client['sftp'].put(local_path, remote_path)

                print(res)
                print(f'上传成功文件已上传到{remote_path}')
            except Exception as e:
                print(f'文件上传失败，失败原因：{e}')
        else:
            raise Exception(
                f'上传路径为空{local_path, remote_path}')

    def down_remote_file(self, ssh_client, local_path, remote_path):
        """
        下载文件到本地
        :param ssh_client: 客户端对象
        :param local_path: 本地路径
        :param remote_path: 远程路径
        :return:
        """
        print('开始下载，请等待....')
        if local_path and remote_path and ssh_client:
            try:

                ssh_client['sftp'].get(remote_path, local_path)
                print(f'下载成功，文件已下载到{local_path}')
            except Exception as e:
                print(e)
                if str(e).find('Errno 13') != -1:
                    print('请定义需要下载的文件名，并添加到路径中')
                if str(e).find('Errno 2') != -1:
                    print('请检查文件路径是否正确')
        else:
            raise Exception(
                f'下载路径为空{local_path, remote_path}')

    def close_client(self, ssh_client):
        """
        执行官远程操作关闭客户端
        :param ssh_client: 传入的客户端对象
        :return:
        """
        flag = False
        if ssh_client:
            print(ssh_client)
            try:
                ssh_client['ssh_client'].close()
                ssh_client['trans'].close()
                print('客户端已关闭')
                flag = True
                return flag
            except Exception as e:
                raise Exception(f'客户端关闭失败，原因为{e}')
        else:
            return flag


if __name__ == '__main__':
    ssh = Ssh()
    print(ssh_detaile)
    flags, server_ip = ssh.check_ip()
    print(flags, server_ip)
    if flags:
        username = input('输入连接用户：')
        passwd = input('输入连接密码：')
        ssh_client = ssh.create_ssh_client(server_ip, username=username,
                                           passwd=passwd, )
        try:
            while True:
                print(detaile)
                keyword = input('请输入要执行的操作：')

                if keyword == 'c':
                    print('程序退出')
                    break
                elif keyword == 'cmd':
                    cmds = input('请输入要执行的linux命令：')
                    ret = ssh.exec_cmd(ssh_client=ssh_client, cmd=cmds)
                elif keyword == 'put':
                    put_local_path = input('请输入需要上传文件的路径:')
                    put_remote_path = input('请输入目标机器路径：')
                    res_put = ssh.put_file(ssh_client, put_local_path,
                                           put_remote_path)
                elif keyword == 'down':
                    # 下载文件
                    down_local_path = input('请输下载到本地的路径：')
                    print(type(down_local_path))
                    down_remote_path = input('请输入下载文件的路径：')
                    ret_get = ssh.down_remote_file(ssh_client, down_local_path,
                                                   down_remote_path)
                else:
                    print(detaile)
                    print('关键字输入有误，请重新输入!')
        except Exception as e:
            print(e)
        finally:

            ssh.close_client(ssh_client)
    else:
        print('ip地址输入错误次数太多，程序退出')
