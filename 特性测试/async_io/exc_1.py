# from greenlet import greenlet
# import asyncio
#
#
# # asyncio装饰器_实现协程
#
# async def func_1():
#     print(1)
#     await asyncio.sleep(2)
#     print(2)
#
#
# async def func_2():
#     print(3)
#     await asyncio.sleep(2)
#     print(4)
#
#
# task = [
#     asyncio.ensure_future(func_1()),
#     asyncio.ensure_future(func_2())
# ]
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(task))
import random
import secrets
import string

from autobahn.wamp.message import Hello

sinum = string.ascii_letters + string.digits
passwd = ''.join(secrets.choice(sinum) for i in range(40))
print(passwd)

list_ = [1, 2, 3, 4, 5]
print(random.sample(list_, k=4))
