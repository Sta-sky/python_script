# 0:正常，1：ping不通
import os
import subprocess
import time
import threading
import queue

list_queue = queue.Queue(2000)
lock = threading.Lock()
ip_list = []
for index in range(1000):
    domain = 'www.kele{}.com'
    list_queue.put(domain.format(index))

def check_ip_ping(host):
    p = os.popen("ping "+ host + " -n 2")
    line = p.read()
    if "无法访问目标主机" in line:
        pass
    else:
        ip_list.append(host)
        lock.acquire()
        with open('./info_ip_back.txt', 'a+') as fp:
            fp.write(f'{host}\n')
        lock.release()
        
    
class MyThread(threading.Thread):
    def __init__(self, name):
        super(MyThread, self).__init__()
        self.queue_list = list_queue
        self.setName(name)
    
    def run(self):
        while True:
            if self.queue_list.empty():
                break
            print(f'剩余ip {self.queue_list.qsize()}')
            print(f'线程{self.name }开始了')
            ip_host = self.queue_list.get()
            check_ip_ping(ip_host)

num = 0
thread_list = []
for i in range(50):
    num += 1
    ip_host = list_queue.get()
    if not ip_host:
        break
    thread_my = MyThread(f'线程_{num}')
    thread_list.append(thread_my)


for i in thread_list:
    print(f'线程{i.name}，开始')
    i.start()
for j in thread_list:
    print(f'线程{j.name}，结束')
    j.join()



