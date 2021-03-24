import asyncio





import asyncio


async def func():
    print('test')
    response = await asyncio.sleep(2)
    print('任务完成')
    return f'执行_____完成： {response}'


task_list = [
    func(),
    func()
]


done, padding = asyncio.run(asyncio.wait(task_list))

print(padding)
print(done)