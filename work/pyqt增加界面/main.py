import math
import time

import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMessageBox
import shutil

import serial
# import serial.tools.list_ports
import _thread
import xlwt
import xlrd
import matplotlib

matplotlib.use('Agg')


if not Path("./data").exists():
    os.mkdir("./data")
DataSavePath = "./data/"
DataSaveName1 = DataSavePath + "DataSave1.xls"
DataSaveName2 = DataSavePath + "DataSave2.xls"
DataSaveName3 = DataSavePath + "DataSave3.xls"
DataSaveName4 = DataSavePath + "DataSave4.xls"

SerialCom1 = "COM4"
SerialCom2 = "COM5"
SerialCom3 = "COM6"
SerialCom4 = "COM7"
SerialBand = 9600
Com_Open_Flag = 0
# custom_serial1 = serial.Serial
# custom_serial2 = serial.Serial
# custom_serial3 = serial.Serial
# custom_serial4 = serial.Serial
Serial1Data = []
Serial2Data = []
Serial3Data = []
Serial4Data = []

writeCnt1 = 0
writeCnt2 = 0
writeCnt3 = 0
writeCnt4 = 0
# 创建一个workbook 设置编码
workbook1 = xlwt.Workbook(encoding='utf-8')
workbook2 = xlwt.Workbook(encoding='utf-8')
workbook3 = xlwt.Workbook(encoding='utf-8')
workbook4 = xlwt.Workbook(encoding='utf-8')
# 创建一个worksheet
worksheet1 = workbook1.add_sheet('My Worksheet')
worksheet2 = workbook2.add_sheet('My Worksheet')
worksheet3 = workbook3.add_sheet('My Worksheet')
worksheet4 = workbook4.add_sheet('My Worksheet')

# 获取串口数据
def Com_Data_Rsv(threadName):
    global custom_serial1, custom_serial2, custom_serial3, custom_serial4  # 全局变量，需要加global
    global Com_Open_Flag
    while Com_Open_Flag:
        data1 = custom_serial1.read_all()
        data2 = custom_serial2.read_all()
        data3 = custom_serial3.read_all()
        data4 = custom_serial4.read_all()
        if data1 != b'':
            print("COM1 receive : ", data1)
            for dataditel in data1:
                Serial1Data.append(dataditel)
        if data2 != b'':
            print("COM2 receive : ", data2)
            for dataditel in data2:
                Serial2Data.append(dataditel)
        if data3 != b'':
            print("COM3 receive : ", data3)
            for dataditel in data3:
                Serial3Data.append(dataditel)
        if data4 != b'':
            print("COM4 receive : ", data4)
            for dataditel in data4:
                Serial4Data.append(dataditel)

def Com_Data_Check(threadName):
    global writeCnt1, writeCnt2, writeCnt3, writeCnt4
    global Serial1Data,Serial2Data,Serial3Data,Serial4Data
    Cnt1 = 0
    DataOldlen1 = 0
    Cnt2 = 0
    DataOldlen2 = 0
    Cnt3 = 0
    DataOldlen3 = 0
    Cnt4 = 0
    DataOldlen4 = 0
    while Com_Open_Flag:
        if DataOldlen1 != len(Serial1Data):
            DataOldlen1 = len(Serial1Data)
            Cnt1 = 0
        Cnt1 += 1
        if Cnt1 > 1000:
            if len(Serial1Data) != 0:
                print("receive all Data: ", Serial1Data[3:10])
                DataCHeck = Serial1Data[3:10]
                ls2 = b''
                for DataDitel in DataCHeck:
                    ls2 += DataDitel.to_bytes(1, 'big', signed=False)
                print(ls2)
                worksheet1.write(writeCnt1, 1, label=bytes.decode(ls2))
                workbook1.save(DataSaveName1)
                writeCnt1 += 1
            Serial1Data = []
            Cnt1 = 0

        if DataOldlen2 != len(Serial2Data):
            DataOldlen2 = len(Serial2Data)
            Cnt2 = 0
        Cnt2 += 1
        if Cnt2 > 1000:
            if len(Serial2Data) != 0:
                print("receive all Data: ", Serial2Data[3:10])
                DataCHeck = Serial2Data[3:10]
                ls2 = b''
                for DataDitel in DataCHeck:
                    ls2 += DataDitel.to_bytes(1, 'big', signed=False)
                print(ls2)
                worksheet2.write(writeCnt2, 1, label=bytes.decode(ls2))
                workbook2.save(DataSaveName2)
                writeCnt2 += 1
            Serial2Data = []
            Cnt2 = 0

        if DataOldlen3 != len(Serial3Data):
            DataOldlen3 = len(Serial3Data)
            Cnt3 = 0
        Cnt3 += 1
        if Cnt3 > 1000:
            if len(Serial3Data) != 0:
                print("receive all Data: ", Serial3Data[3:10])
                DataCHeck = Serial3Data[3:10]
                ls2 = b''
                for DataDitel in DataCHeck:
                    ls2 += DataDitel.to_bytes(1, 'big', signed=False)
                print(ls2)
                worksheet3.write(writeCnt3, 1, label=bytes.decode(ls2))
                workbook3.save(DataSaveName3)
                writeCnt3 += 1
            Serial3Data = []
            Cnt3 = 0

        if DataOldlen4 != len(Serial4Data):
            DataOldlen4 = len(Serial4Data)
            Cnt1 = 0
        Cnt4 += 1
        if Cnt4 > 1000:
            if len(Serial4Data) != 0:
                print("receive all Data: ", Serial4Data[3:10])
                DataCHeck = Serial4Data[3:10]
                ls2 = b''
                for DataDitel in DataCHeck:
                    ls2 += DataDitel.to_bytes(1, 'big', signed=False)
                print(ls2)
                worksheet4.write(writeCnt4, 1, label=bytes.decode(ls2))
                workbook4.save(DataSaveName4)
                writeCnt4 += 1
            Serial4Data = []
            Cnt4 = 0

from main_ui import Ui_Form
class AngleUi(Ui_Form, QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.resize(1200, 700)
        self.buttoncalculation.clicked.connect(self.calculation)
        self.buttonOpenCom.clicked.connect(self.OpenCom)


    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        progrem_size = self.geometry()
        newLeft = int((screen.width() - progrem_size.width()) / 2)
        newtop = int((screen.height() - progrem_size.height()) / 2)
        self.move(newLeft, newtop)

    def calculation(self):
        try:
            data = [0, 0, 0, 0]
            files = []
            if not Path("./data1").exists():
                os.mkdir("./data1")
            for info in os.listdir("./data"):
                if str.endswith(info, ".xls"):
                    files.append(info)
            for i in range(0, len(files)):
                df = pd.read_excel("./data/" + files[i])
                data[i] = df.iloc[len(df) - 1, df.shape[1] - 1]
                shutil.move("./data/" + files[i], "./data1/" + files[i])
            self.input1cssj.setText('0.05,' + str(data[0]))
            self.input2cssj.setText('0.10,' + str(data[1]))
            self.input3cssj.setText('0.15,' + str(data[2]))
            self.input4cssj.setText('0.20,' + str(data[3]))
            x1 = float(self.input1cssj.text().split(',')[0])
            y1 = float(self.input1cssj.text().split(',')[1])
            x2 = float(self.input2cssj.text().split(',')[0])
            y2 = float(self.input2cssj.text().split(',')[1])
            x3 = float(self.input3cssj.text().split(',')[0])
            y3 = float(self.input3cssj.text().split(',')[1])
            x4 = float(self.input4cssj.text().split(',')[0])
            y4 = float(self.input4cssj.text().split(',')[1])
            x = np.array([x1, x2, x3, x4])
            y = np.array([y1, y2, y3, y4])
            if y2 == 0:
                x = np.array([x1])
                y = np.array([y1])
            elif y3 == 0:
                x = np.array([x1, x2])
                y = np.array([y1, y2])
            elif y4 == 0:
                x = np.array([x1, x2, x3])
                y = np.array([y1, y2, y3])
            w, b = self.fit(x, y)
            pred_y = w * x + b
            plt.scatter(x, y)
            plt.plot(x, pred_y, c='r', label='line')
            plt.savefig("./test.jpg")
            pix = QPixmap('test.jpg')
            self.label_img_show.setGeometry(0, 0, 500, 210)
            self.label_img_show.setPixmap(pix)
            self.inputpzjd.setText(str(math.atan(w) * (180 / math.pi)))
            with open("./data1/data.txt", "a") as f:
                f.write("型号为%s，鞋码为%s，拉力为%s，偏向角度结果为%s\n" % (
                    self.inputxh.text(), self.inputxm.text(), self.inputyl.text(), str(math.atan(w) * (180 / math.pi))))
        except Exception as E:
            message = QMessageBox()
            message.warning(None, '错误', str(E))

    def fit(self, data_x, data_y):
        """
        最小二乘法
        :param data_x:
        :param data_y:
        :return:
        """
        m = len(data_y)
        x_bar = np.mean(data_x)
        sum_yx = 0
        sum_x2 = 0
        sum_delta = 0
        for i in range(m):
            x = data_x[i]
            y = data_y[i]
            sum_yx += y * (x - x_bar)
            sum_x2 += x ** 2
        # 根据公式计算w
        w = sum_yx / (sum_x2 - m * (x_bar ** 2))

        for i in range(m):
            x = data_x[i]
            y = data_y[i]
            sum_delta += (y - w * x)
        b = sum_delta / m
        return w, b

    def OpenCom(self):
        global custom_serial1, custom_serial2, custom_serial3, custom_serial4  # 全局变量，需要加global
        global Com_Open_Flag
        if self.buttonOpenCom.text() == "打开设备":
            print("Click")
            # custom_serial1 = serial.Serial(SerialCom1, SerialBand, timeout=0.5)
            # custom_serial2 = serial.Serial(SerialCom2, SerialBand, timeout=0.5)
            # custom_serial3 = serial.Serial(SerialCom3, SerialBand, timeout=0.5)
            # custom_serial4 = serial.Serial(SerialCom4, SerialBand, timeout=0.5)
            print("Test Status 1")
            custom_serial1.isOpen()
            custom_serial2.isOpen()
            custom_serial3.isOpen()
            custom_serial4.isOpen()
            print("Test Status 2")
            self.buttonOpenCom.setText("停止测量")
            Com_Open_Flag = 1
            _thread.start_new_thread(Com_Data_Rsv, ("Thread-1",))
            _thread.start_new_thread(Com_Data_Check, ("Thread-1",))

            time.sleep(1)
            Data_Send_Test = [0x80, 0x06, 0x03, 0x77]
            custom_serial1.write(Data_Send_Test)
            custom_serial2.write(Data_Send_Test)
            custom_serial3.write(Data_Send_Test)
            custom_serial4.write(Data_Send_Test)
        else:
            Com_Open_Flag = 0
            self.buttonOpenCom.setText("打开设备")
            custom_serial1.close()
            custom_serial2.close()
            custom_serial3.close()
            custom_serial4.close()


    def SendData(self):
        global custom_serial1, custom_serial2, custom_serial3, custom_serial4  # 全局变量，需要加global
        global Com_Open_Flag
        if Com_Open_Flag:
            print("发送数据")
            Data_Send_Test = [0x80, 0x06, 0x03, 0x77]
            custom_serial1.write(Data_Send_Test)
            custom_serial2.write(Data_Send_Test)
            custom_serial3.write(Data_Send_Test)
            custom_serial4.write(Data_Send_Test)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    agu = AngleUi()
    agu.show()
    sys.exit(app.exec_())
