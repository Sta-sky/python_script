# -*- coding: utf8 -*-
import contextlib

path = 'nihao'

@contextlib.contextmanager
def handle_file(filename, method):
    global path
    print(f'start: { filename } in __enter__')
    file_handle = open(filename, method)
    try:
        yield file_handle
    except Exception as exc:
        print('file error')
    finally:
        print(f'close file {filename} in __exit__')
        file_handle.close()
        return

#
# with handle_file('./await_1.py', 'rb') as f:
#     print(f.read().decode())
import json
import random

res = random.randint(1, 4)
print(res)
li = [1 ,5 ,2, 3,]
print(li[:res][-1])


print(100 - (2 * 38))


s = ['年后', '我拉了', '我们', 'hah']
# print(s)
# json.dumps(s)
# print(s)
# print(type(s))
print(json.loads(s))