# -*-coding : utff-8 -*-
import os
import queue
import time
from threading import Thread, Lock


class MytheadWrite(Thread):
    def __init__(self, file_queue):
        super(MytheadWrite, self).__init__()
        self.name = self.getName()
        self.save_file = 'D:\\资料\\{}'
        self.lock = Lock()
        self.queue = file_queue

    def run(self):
        while True:
            if self.queue.empty():
                print(f'队列已空，当前线程{self.name},退出')
                break
            video_file = self.queue.get()
            print(f'当前线程{self.name}, 取出的文件为{video_file}')
            size = os.path.getsize(video_file)
            name = video_file.split('\\')[-1]
            save_path = self.save_file.format(name)
            print(size)
            if os.path.exists(save_path):
                print(f'文件{name}已经存在，线程{self.name},退出')
                return
            print(f'当前文件正在由线程{self.name}下载：name为：{name}，大小为：', size)
            try:
                with open(video_file, 'rb') as fp:
                    with open(save_path, 'ab+')as tp:
                        while True:
                            data = fp.read(8 * 1024 * 1024)
                            if not data:
                                print('文件读取完成，退出')
                                break
                            tp.write(data)
            except Exception as e:
                print(f'下载失败，原因为{e}')

def save_queue():
    queue_obj = queue.Queue()
    file = 'D:\\资料\\录屏资料'
    base_path = os.walk(file)
    for i in base_path:
        j, l, video_list = i
        for video in video_list:
            video_param = file + '\\' + video
            print(video_list, '========')
            queue_obj.put(video_param)
    return queue_obj


if __name__ == '__main__':
    th_num = 10
    obj_queue = save_queue()
    th_list = []
    for th_num in range(th_num):
        th = MytheadWrite(obj_queue)
        th.setName('__线程__' + str(th_num))
        th_list.append(th)
    for i in th_list:
        i.start()
    for j in th_list:
        j.join()
        print(f'线程----{j.name}回收成功')

