"""
初始化日志根据日志名称，调用对应打印的日志目录
"""
import logging
import os

LOG_NAME = ['eBackup', 'CSBS', 'Openstack', 'SDK', 'ODK', 'ssh']
BASE_PATH = os.path.realpath('./log/')
Formante = ("%(asctime)s - %(filename)s - line:%(lineno)d - %(funcName)s - %("
            "levelname)s - %(message)s")


class Log:
    def __init__(self, name):
        self.name = name
        if self.name not in LOG_NAME:
            raise Exception('日志name 为 None')
        # 获取logger实例
        self.logger = logging.getLogger(self.name)
        # 设置日志集

        self.logger.setLevel(logging.DEBUG)

        # 设置存储目录, 用于写入日志文件
        if not os.path.exists(BASE_PATH + '/' + self.name):
            os.makedirs(BASE_PATH + '/' + self.name)

        log_path = logging.FileHandler(BASE_PATH + '/' + self.name + '/' +
                                       self.name + '.log', encoding='utf-8')
        # 设置终端打印的日志, 用于打印到控制台
        console = logging.StreamHandler()
        # 设置终端打印的级别
        console.setLevel(logging.DEBUG)

        # 设置打印的格式
        formatter = logging.Formatter(Formante)

        # 为终端打印以及日志打印中加上格式
        console.setFormatter(formatter)
        log_path.setFormatter(formatter)

        # 将文件日志加入日志集中
        self.logger.addHandler(console)
        self.logger.addHandler(log_path)

    def print_info(self):
        # 设置文件中存储的日志级别
        return self.logger



