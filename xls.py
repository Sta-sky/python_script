# coding=utf-8
import datetime
import os

import random

import pymysql, xlwt


class WriteXlwtFile(object):
    def __init__(self):
        self.file_path = "C:\\Users\\13617\Desktop\\user_info.xls"

        if os.path.exists(self.file_path):
            s = self.file_path
            os.remove(self.file_path)

        self.connect_sql = pymysql.Connect(host='127.0.0.1',
                                           password='123456',
                                           user='root',
                                           port=3306,
                                           database='dada')
        self.cousor = self.connect_sql.cursor()


    def connect_database(self):
        sql = "select * from user_regist"
        # 执行语句
        self.cousor.execute(sql)
        # 获取所有数据
        result = self.cousor.fetchall()
        return result

    def write_xwlt(self, data_result):
        # 获取数据表中字段
        fields = self.cousor.description
        # 初始化xlwt对象
        workbook = xlwt.Workbook(encoding='utf8', style_compression=2)
        # 添加sheet页                   cell_overwrite_ok 参数用于确认同一个cell单元是否可以重设值。
        sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

        # 循环读取字段，写入sheet页中
        for i in range(len(fields)):
            color = random.randint(0,200)
            sheet1.write(0, i, fields[i][0],self.set_style('Times New Roman',400,color))

        print('开始写入%s文件中' % self.file_path)
        num = len(data_result)
        count = 0

        for row in range(1, len(data_result) + 1):
            count += 1
            print('已写入%.2f' % ((count / num) * 100) + '%')
            for col in range(len(fields)):
                data = data_result[row - 1][col]
                print(type(data))
                print(data)
                if isinstance(data, datetime.datetime):
                    color = random.randint(0, 200)
                    styles = self.set_style('Times New Roman',300,color)
                    styles.num_format_str = 'yyyy-mm-DD hh:mm:ss'
                    sheet1.write(row, col, data, styles)
                else:
                    color = random.randint(0, 200)
                    sheet1.write(row, col, data, self.set_style('Times New Roman',300,color))
        workbook.save(self.file_path)

    def set_style(self,font_name,height,color):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = font_name
        font.height = height
        font.colour_index = color
        style.font = font
        return style

    def run(self):
        result = self.connect_database()
        self.write_xwlt(result)


if __name__ == '__main__':
    start_write = WriteXlwtFile()
    start_write.run()
