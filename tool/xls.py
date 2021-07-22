# coding=utf-8
import datetime
import os

import random
import pymysql, xlwt

"""
功能  mysql数据表导出；
"""


class WriteXlwtFile(object):
    """
    输入数据库，输入数据表，
    进行下载；
    """

    def __init__(self):
        base_file = "C:/Users/Administrator/Desktop/python_exc/xml_download/{" \
                    "}/"
        retry_times = 0
        while retry_times < 5:
            retry_times += 1
            try:
                database = input('请输入数据库名称:')
                self.connect_sql = pymysql.Connect(host='127.0.0.1',
                                                   password='123456',
                                                   user='root',
                                                   port=3306,
                                                   database=database)
                if os.path.exists(base_file.format(database)):
                    self.file_path = base_file.format(database) + '{}.xlsx'
                else:
                    self.file_path = os.mkdir(base_file.format(database))
                break
            except Exception as e:
                print('数据库名称输入有误,请重新输入!', e)
                if retry_times >= 5:
                    raise ('输入次数过多，请重新启动程序')

        self.cousor = self.connect_sql.cursor()

        # 表格字体彩色  开关
        # self.color = random.randint(0, 200)
        self.color = 0x7FFF
        self.weight = 200

    def connect_database(self):
        # 执行语句
        retry_times = 0
        while retry_times < 5:
            retry_times += 1
            try:
                name = input('请输入要导出的数据表名称')
                sql = 'select * from %s' % name
                self.cousor.execute(sql)
                print(name)
                self.file_path = self.file_path.format(name)
                print(self.file_path)
                break
            except Exception as e:
                print('数据库名称输入有误,请重新输入', e)
                if retry_times >= 5:
                    raise ('输入次数过多，请重新启动程序')

        # 获取所有数据
        result = self.cousor.fetchall()
        return result, self.file_path

    def write_xwlt(self, data_result, file_name):
        # 获取数据表中字段
        print(file_name)
        fields = self.cousor.description
        print(fields)
        # 初始化xlwt对象
        workbook = xlwt.Workbook(encoding='utf8', style_compression=2)
        # 添加sheet页                   cell_overwrite_ok 参数用于确认同一个cell单元是否可以重设值。
        self.sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

        # 循环读取字段，写入sheet页中
        for i in range(len(fields)):
            color = random.randint(0, 10)
            print(color)
            self.sheet1.write(0, i, fields[i][0], self.set_style(u'微软雅黑', 300,
                                                            color=self.color))

        print('开始写入%s文件中' % file_name)
        num = len(data_result)
        count = 0

        for row in range(1, len(data_result) + 1):
            count += 1
            print('已写入%.2f' % ((count / num) * 100) + '%')
            for col in range(len(fields)):
                data = data_result[row - 1][col]
                if isinstance(data, datetime.datetime):

                    styles = self.set_style('Times New Roman', self.weight,
                                            self.color)
                    styles.num_format_str = 'yyyy-mm-DD hh:mm:ss'
                    self.sheet1.write(row, col, data, styles)
                else:
                    # color = random.randint(0, 200)
                    self.sheet1.write(row, col, data, self.set_style(u'微软雅黑', self.weight,
                                                                self.color))
        workbook.save(file_name)

    def set_style(self, font_name, height, color, bg_color=0):
        """
            bg_color : 0 - 10 颜色变化
        """
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = font_name
        font.height = height
        font.colour_index = color
    
        # 设置对其方式
        """
			VERT_TOP = 0x00 上端对齐
			VERT_CENTER = 0x01 居中对齐(垂直方向上)
			VERT_BOTTOM = 0x02 低端对齐
			HORZ_LEFT = 0x01 左端对齐
			HORZ_CENTER = 0x02 居中对齐(水平方向上)
			HORZ_RIGHT = 0x03 右端对齐
		"""
        al = xlwt.Alignment()
        al.HORZ_CENTER = 0x02
        al.VERT_CENTER = 0x01
    
        # 设置背景色
        pattern_top = xlwt.Pattern()
        pattern_top.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern_top.pattern_fore_colour = bg_color
    
        style.alignment = al
        style.pattern = pattern_top
        style.font = font
        return style

    def set_cell_width(self, col):
        """ 设置表格宽
            width : 256 * 20    256为衡量单位，20表示20个字符宽度
            col: 列索引 int
        """
        """   """
        item_col = self.sheet1.col(col)
        item_col.width = 256 * 20

    def run(self):
        result, file_name = self.connect_database()
        self.write_xwlt(result, file_name)


if __name__ == '__main__':
    start_write = WriteXlwtFile()
    start_write.run()
