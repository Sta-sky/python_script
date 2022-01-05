import sys
import socket

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
import pandas as pd
from pandas import DataFrame

from 飞行数据处理与分析系统 import plot_col
from index_ui import Ui_Form



class MainLogin(Ui_Form, QWidget):
    
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.resize(1100, 700)
        self.img_label.setMinimumSize(100, 400)

        self.btn_fly_1.clicked.connect(self.software_1)
        self.btn_fly_2.clicked.connect(self.software_2())
        self.btn_fly_3.clicked.connect(self.software_3)
        self.btn_fy.clicked.connect(lambda: self.show_img("俯仰_度.jpg"))
        self.btn_gd.clicked.connect(lambda: self.show_img("滚转_度.jpg"))
        self.btn_fly_hx.clicked.connect(lambda: self.show_img("航向_度.jpg"))
        self.btn_wsdgd.clicked.connect(lambda: self.show_img("无线电高度高位_FT_无线电高度低位_FT.jpg"))
        self.btn_jksd.clicked.connect(lambda: self.show_img("计算空速_KT.jpg"))
        self.btn_czsd.clicked.connect(lambda: self.show_img("垂直速度_KT.jpg"))
        self.btn_mhs.clicked.connect(lambda: self.show_img("马赫数.jpg"))
        self.btn_tlnj.clicked.connect(lambda: self.show_img("推力扭矩.jpg"))

    
    def show_img(self, image):
        try:
            pix = QPixmap(image)
            self.img_label.setPixmap(pix)
            self.img_label.setScaledContents(True)  # 让图片自适应label大小
        except Exception as e:
            print(e)
        
        
    def software_1(self):
        self.status_lin_1.setText("开始运行，请等待...")
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
        i = 1
        while i > 0:
            recv_data = tcp_client_socket.recv(1024)
            # 返回的直接是服务端程序发送的二进制数据
            # print(recv_data)
            # 对数据进行解码
            recv_content = recv_data.decode("gbk")
            self.textEdit.setText(recv_content)
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
        self.status_lin_1.setText('运行完成！')
        
    def software_2(self):
        print('进来了')
        try:
            self.status_lin_2.setText('开始运行，请等待！')
            data = pd.read_csv('convert.csv', encoding='utf-8')
            cols = ['俯仰/度', '滚转/度', '航向/度', ['无线电高度高位/FT', '无线电高度低位/FT'], '计算空速/KT', '垂直速度/KT',
                    '马赫数', '推力扭矩']
            plot_col(data, cols)
            self.status_lin_2.setText('运行完成！')
        except Exception as e:
            print('========')
            self.status_lin_2.setText(f'error： {e}')
            print(e)


    def software_3(self):
        print('======第三个开始了---')
        self.status_lin_3.setText('开始运行，请等待！')

        dic1 = {}
        dic2 = {}
        with open("QAR数据（飞行航班1） - 副本.txt", "r", encoding="utf-8")as f2:
            li2 = f2.readlines()

        with open("查找.txt", "r", encoding="utf-8")as f:
            li = f.readlines()
        for i in li[0].strip().split("/"):
            dic1[i] = []

        for i2 in li[1].strip().split("/"):
            dic2[i2] = []

        print(dic1)
        print(dic2)

        for x in li[0].strip().split("/"):
            if len(x) == 2:
                for n in li2:
                    if n.startswith(f"#10{x}") or n.startswith(f"#20{x}") or n.startswith(f"#30{x}") or n.startswith(
                            f"#40{x}"):
                        dic1[x].append("\t" + n[5:9])
            if len(x) == 3:
                for n in li2:
                    if n.startswith(f"#1{x}") or n.startswith(f"#2{x}") or n.startswith(f"#3{x}") or n.startswith(
                            f"#4{x}"):
                        dic1[x].append("\t" + n[5:9])

        print("=====")

        for y in li[1].strip().split("/"):
            if len(y) == 3:
                for m in li2:
                    if m.startswith(f"#1{y}"):
                        dic2[y].append("\t" + m[5:9])

        print(dic1)
        print(dic2)

        dic1.update(dic2)

        num = 0
        for k, v in dic1.items():
            if len(v) > num:
                num = len(v)

        for k, v in dic1.items():
            if len(v) != num:
                for i in range(num - len(v)):
                    v.append("")

        # 字典中的key值即为csv中列名
        dataframe = DataFrame(dic1)
        dataframe.to_csv('result.csv', index=False, sep=',')
        import pandas as pd
        import numpy as np
        import re
        df = pd.DataFrame(pd.read_excel("译码对应数据.xls"))
        data = pd.read_csv('result.csv')

        # 这个是转化数据的函数
        def convert(x, idxs, coef):
            if type(x) == str:
                # 将16进制的数据转化为10进制，在转化为2进制
                bin_str = bin(int(x, 16))[2:]
                # 固定二进制的长度为16
                if len(bin_str) < 16:
                    bin_str = '0' * (16 - len(bin_str)) + bin_str
                if len(idxs) > 1:
                    # 从低位开始算的
                    bin_str = bin_str[-idxs[1]:-idxs[0]]
                else:
                    bin_str = bin_str[-idxs[0]]
                return int(bin_str, 2) * coef
            # 如果16进制是0，则被pandas读取成0，也就是float数据，直接返回0即可
            else:
                return 0

        convert_df = pd.DataFrame()
        for column in df.columns:
            # 获取特定位数
            if type(df[column][0]) == str:
                idxs = re.findall(r'\d+', df[column][0])
                idxs = list(map(int, idxs))
            else:
                idxs = [int(df[column][0])]
            # 获取系数
            if pd.isnull(df[column][10]):
                coef = 1
            else:
                coef = df[column][10]
            # 需要整合的数据列
            number_columns = []
            for i in range(1, 9):
                # 如果是空值则跳出循环
                if pd.isnull(df[column][i]):
                    break
                # 如果不在result.csv文件则跳过，数据问题
                if str(df[column][i]) not in data.columns:
                    continue
                number_columns.append(str(int(df[column][i])))
            # 找不到对应的数据，则跳过这个数据
            if len(number_columns) == 0:
                continue
            # 删除掉空值
            new_data = data[number_columns].copy().dropna(axis=0, how='any')
            # 整合多列的数据
            new_data = np.reshape(new_data.values, [-1])
            convert_df[column] = pd.Series(new_data)
            convert_df[column] = convert_df[column].apply(convert, args=[idxs, coef])

        convert_df.to_csv('convert.csv', encoding='utf_8_sig', index=False)

        self.status_lin_3.setText('运行结束')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    agu = MainLogin()
    agu.show()
    sys.exit(app.exec_())
