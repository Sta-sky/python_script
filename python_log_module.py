"""
初始化日志根据日志名称，调用对应打印的日志目录
"""
import logging
import os
import sys

LOG_NAME = ['eBackup', 'CSBS', 'Openstack', 'SDK', 'ODK']
BASE_PATH = os.path.realpath('./var/log/')
Formante = (
    "%(asctime)s - %(filename)s - line:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s")


class Log:
    def __init__(self, name):
        self.name = name

    def info(self):
        if self.name not in LOG_NAME:
            raise
        # 设置日志集
        logger = logging.getLogger(self.name)
        logger.setLevel('INFO')

        # 设置存储目录
        if not os.path.exists(BASE_PATH + '/' + self.name):
            os.makedirs(BASE_PATH + '/' + self.name)
        print(self.name)
        print(BASE_PATH)
        log_path = logging.FileHandler(BASE_PATH + '/' +self.name + '/' +
                                       self.name + '.log')
        # 设置文件中存储的日志级别
        log_path.setLevel('INFO')

        # 设置终端打印的日志
        console = logging.StreamHandler()
        # 设置终        端打印的级别
        console.setLevel('DEBUG')

        # 设置打印的格式
        formatter = logging.Formatter(Formante)

        # 为终端打印以及日志打印中加上格式
        console.setFormatter(formatter)
        log_path.setFormatter(formatter)

        # 将文件日志加入日志集中
        logger.addHandler(console)
        logger.addHandler(log_path)
fr = 'Openstack'
l = Log(fr)
l.info()
try:
    print(ca)
    raise Exception
except:
    print(sys._getframe(0))
    print(sys.exc_info()[2].tb_frame.f_code)
    s = sys.exc_info()[2].tb_frame.f_code
    co_name = s.f_code.co_name
    print(co_name)
    file_line = s.f_lineno,
    print(file_line)

    file_name = s.f_code_co_filename
    print(file_name)
