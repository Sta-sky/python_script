import random
import secrets
import string
import time

import redis
from tool_script.byte_change_str import change_str

set_name = 'my_video_name'
NUM = 2000
ts_base = 'https://ggcc01.com/archives/category/jingpin/page/{}'

redis_clent = redis.Redis(host='127.0.0.1', db=2)


def get_ts_list():
    ts_str = ''
    for i in range(NUM):
        urls = ts_base.format(i) + '|'
        ts_str += urls
    return ts_str


def generato_data():
    for i in range(100):
        name = '变形金刚' + str(i)
        sinum = string.ascii_letters + string.digits
        save_path = 'c:\\data\\nihao\\{}.mp4'.format(name)
        key = ''.join(secrets.choice(sinum) for i in range(15))
        index_path_key = save_path + '_' + key
        ts = get_ts_list()

        # 存储视频索引
        name_res = redis_clent.sadd(set_name, index_path_key)
        print(name_res)
        # 存储ts列表
        res = redis_clent.hset(name=save_path, key=index_path_key, value=ts)
        print(res)


def get_data():
    while True:
        totle_num = redis_clent.scard(set_name)
        if totle_num == 0:
            print('所有下载完成，退出')
            break
        print(f'当前总共有{totle_num}个ts')
        #
        get_set_key = change_str(redis_clent.spop(set_name))
        new_save_path = get_set_key.split('_')[0]
        key_res = get_set_key.split('_')[1]
        print(get_set_key)
        if not key_res:
            keys = None
            print('没有key，不需要解密')
        else:
            keys = key_res
        # 根据set中返回的元素，查找hash中的ts
        print(new_save_path)
        if redis_clent.exists(new_save_path):
            hash_val = change_str(redis_clent.hgetall(new_save_path))
            print(f'返回的hash{hash_val}, key为{keys}, 新的保存路径为{new_save_path}')
        time.sleep(2)


if __name__ == '__main__':

    # generato_data()
    get_data()



# TODO 集合的操作
""""
# 1.1.5. 随机从集合返回指定个数元素   srandmember key [count]
# 1.1.3. 计算元素个数   scard key
# 1.1.4. 判断元素是否在集合中  sismember key element
# 1.1.6. 从集合随机弹出元素  spop key
# 总共还有多少个

"""

"""
使用集合存储文件保存路径，作为hash的索引

hash保存ts，使用保存路径作为key, name+ts数量 作为name，value为ts列表字符串
"""




