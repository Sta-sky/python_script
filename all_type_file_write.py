import os
import time
from threading import Thread, Lock

lock = Lock()


class FileeCopy(Thread):

    @staticmethod
    def thread_file_write(file_list, storage_path):
        if not os.path.exists(storage_path):
            with open(storage_path, 'wb') as fp:
                fp.truncate()
        try:
            lock.acquire()
            for data in file_list:
                with open(storage_path, 'ab') as fp:
                    fp.write(data)
            lock.release()
        except Exception as e:
            pass

    @staticmethod
    def thread_copy_picture(file_path, split_number, target_path):
        """
        读取传入路径下所有文件，分割为指定数量的平均份数，
        :param file_path:
        :return:
        """
        file_suffix = os.path.splitext(file_path)
        try:
            file_suffix[1].split('.')[1]
        except Exception as e:
            file_ = os.walk(file_path)
            print(file_)
            for root_path, sub_dir, file_name_list in file_:
                thread_pool = []
                for file_name in file_name_list:
                    read_file_path = root_path + '\\' + file_name
                    print(root_path)
                    print(read_file_path, '40')
                    result = FileeCopy.file_split(read_file_path, split_number)

                    storage_path = target_path + '\\' + file_name
                    write_test = Thread(target=FileeCopy.thread_file_write,
                                        args=(result, storage_path))
                    thread_pool.append(write_test)
                for start_thread in thread_pool:
                    start_thread.start()
        else:
            thread_pool = []
            result = FileeCopy.file_split(file_path, split_number)
            storage_path = target_path + os.path.basename(file_path)
            write_test = Thread(target=FileeCopy.thread_file_write,
                                args=(result, storage_path))
            thread_pool.append(write_test)
            for start_thread in thread_pool:
                start_thread.start()

    @staticmethod
    def file_split(file_path, split_number):
        """
        将文件拆分为splity_number个相同大小的个数，返回
        :param split_number:
        :param file_path:
        :return: list，每份文件的内容
        """
        if file_path and split_number:
            # 获取文件大小
            try:
                lock.acquire()
                file_size = os.path.getsize(file_path)
                print(file_size)

                # 分配给每个文件应读取多少
                every_size = file_size // split_number
                print(every_size)
                file_list = []
                # 读取文件
                with open(file_path, 'rb') as f:
                    for num in range(split_number):
                        # 最后一次读取 全部读完
                        if num == split_number - 1:
                            data = f.read()
                            file_list.append(data)
                        else:
                            data = f.read(every_size)
                            file_list.append(data)
                lock.release()
                return file_list
            except Exception as e:
                print(e)


if __name__ == '__main__':
    start = times = time.time()
    file_path = 'C:\\Users\\dwx917920\\Desktop\\操作指南'
    split_number = 10
    target_name = 'C:\\Users\\dwx917920\\Desktop\\巡检\\upgrade_manifest_check\\test'

    FileeCopy().thread_copy_picture(file_path, split_number, target_name)
    stop_time = time.time()
    tall_time = stop_time - start
    print('总时间为%s ' % tall_time)
