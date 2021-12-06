import asyncio


async def set_res(fut):
    print('start')
    await asyncio.sleep(2)
    fut.set_result('666')


async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务（Future对象）， 这个任务什么都不做
    fut = loop.create_future()

    # 时间循环中添加任务
    loop.create_task(set_res(fut))

    # 等待任务最终的结果（future对象），没有结果则会一直等待下去。
    data = await fut
    return data


res = asyncio.run(main())
print(res)
