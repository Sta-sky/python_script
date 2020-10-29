# -*-coding : utff-8 -*-
import os
import queue
import time
from threading import Thread, Lock
from tool_script.util import time_wappre


def time_wappre(func):
    def rewappre(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'文件执行了{"%.2f" % (end_time - start_time)}秒')
        return result
    return rewappre


class MytheadWrite(Thread):
    def __init__(self, file_queue, target_path):
        super(MytheadWrite, self).__init__()
        self.name = self.getName()
        self.save_file = target_path
        self.lock = Lock()
        self.queue = file_queue

    @time_wappre
    def run(self):
        while True:
            curr_queue_num = self.queue.qsize()
            if self.queue.empty():
                print(f'队列已空，当前线程{self.name},退出')
                break
            video_file = self.queue.get()
            print(f'当前线程{self.name}, 取出的文件为{video_file}')
            curr_file_size = os.path.getsize(video_file)
            name = video_file.split('\\')[-1]
            save_path = self.save_file + '\\' + name
            if os.path.exists(save_path):
                print(f'文件{name}已经存在，线程{self.name},退出')
                return
            print(f'当前由线程{self.name}下载，name为：{name}，大小为：', curr_file_size)
            print(f'队列中剩余{curr_queue_num}个文件待下载')
            try:
                with open(video_file, 'rb') as fp:
                    with open(save_path, 'ab+')as tp:
                        while True:
                            data = fp.read(8 * 1024 * 1024)
                            if not data:
                                print('文件读取完成，退出')
                                break
                            tp.write(data)
                continue
            except Exception as e:
                print(f'下载失败，原因为{e}')
                continue


def save_queue(locals_path):
    queue_obj = queue.Queue()
    file = locals_path
    base_path = os.walk(file)
    for file_obj in base_path:
        file_base_path_str, dir_list, file_list = file_obj
        for video in file_list:
            video_param = file + '\\' + video
            print(file_list)
            queue_obj.put(video_param)
    return queue_obj


if __name__ == '__main__':
    local_path = input('请输入本地文件路径：')
    target_path = input('请输入文件保存路径：')
    queues = save_queue(local_path)
    th_list = []
    for th_num in range(10):
        th = MytheadWrite(queues, target_path)
        th.setName('__线程__' + str(th_num))
        th_list.append(th)
    for i in th_list:
        i.start()
    for j in th_list:
        j.join()
        print(f'线程----{j.name}回收成功')

