## 协程

#### 1、协程理解

~~~
async 协程创建

async:
	定义此函数为异步函数
	异步函数的特点：
		此函数执行的过程中能够中断，挂起（一般函数会从上往下执行完，不会中断）
await：
	用来声明，此异步函数在此处被挂起了，执行await后面的异步函数。
	await后面只能跟异步程序或者有__await__属性的对象，
		如果没有异步属性，就相当于直接调用普通函数，执行的过程中要等待函数执行返回后，才会执行下面步骤，
		而跟有异步属性的对象，当前程序会跳到异步程序中，然后跳出来，让异步程序自己去执行，然后继续执行后面的步骤。
~~~

#### 2、协程的意义

~~~python
1、在一个线程中，如果遇到io等待的时间，线程不会等待，此函数的执行会被中断挂起，去执行其他的任务。充分利用系统资源。
2、以协程的方式实现异步编程。
~~~



#### 3、实现协程的方式：

~~~
1、greenlet，早期模块。gevente底层基于这个greenlet实现。
2、yiled 关键字。
3、asyncio 装饰器 （python3.4）
4、async、await关键字（py3.5以后）【推荐】
~~~



##### 3.1 greenlet 实现协程 

~~~python
from greenlet import greenlet

def func_1():
    print(1)
    gr2.switch()  # --- >跳到func_2
    print(2)
    gr2.switch()  # -- 跳到func_2

def func_2():
    print(3)
    gr1.switch()  ---> 跳到func_1
    print(4)

gr1 = greenlet(func_1)
gr2 = greenlet(func_2)

gr1.switch()  -- 跳到func_1 
~~~



##### 3.2 yiled关键字实现协程

~~~python

def func_1():
    yield 1
    yield from func_2()
    yield 2

def func_2():
    yield 3
    yield 4

res = func_1()
for i in res:
    print(i)
~~~



##### 3.3  asyncio装饰器模块实现协程 py3.4之后

~~~python
import asyncio
# py3.8之后装饰器方式已经弃用

# asyncio装饰器_实现协程
@asyncio.coroutine
def func_1():
    print(4)
    yield from asyncio.sleep(2)
    print(2)


@asyncio.coroutine
def func_2():
    print(3)
    yield from asyncio.sleep(2)
    print(4)


task = [
    asyncio.ensure_future(func_1()),
    asyncio.ensure_future(func_2())
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))

~~~



##### 1.4 async、await关键字

​	python3.5之后使用

~~~python
import asyncio


async def func_1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def func_2():
    print(3)
    await asyncio.sleep(2)
    print(4)


task = [
    asyncio.ensure_future(func_1()),
    asyncio.ensure_future(func_2())
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))

~~~

#### 4、同步异步

~~~python
同步：
	任务挨个执行，并等待结果返回，再执行下一个任务，为同步
异步：
	任务执行，不等待结果，执行下一个，为异步。
~~~



#### 5、异步编程

##### 5.1 事件循环

~~~python
概念：事件循环再异步编程中，会循环检测可执行的异步事件，拿出可执行的任务进行执行，直到可执行事件为空。循环停止。

# 生成一个事件循环
loop = asyncio.get_event_loop()
# 将任务放到人物列表，循环检测，直到所有任务完成，退出
loop.run_until_complete(asyncio.wait(task))
~~~

##### 5.2 协程函数

- 协程函数：协程函数，定义时如果函数前有async关键字，就称之为协程函数。
- 协程对象：协程函数初始化，得到的对象，称为协程对象。

~~~python

async def func():
    pass

# 注意：初始化协程函数后，内部代码不会执行
res = func()

func : 	协程函数
res: 	协程对象
~~~

##### 5.2 协程函数运行

- 需要借助以下三者共同完成：
  - 协程函数
  - 写成对象
  - 事件循环

~~~python
import asyncio

async def func():
    pass

res = func()

# 循环事件对象
loop = asyncio.get_event_loop()
loop.run_until_complete(res)

python_3.7之后使用一下方式就可以执行， run()中实现的就是上面1、创建事件循环，2、将任务加入事件循环中；
asyncio.run(res)
~~~



##### 5.3 await关键字

- await + 可等待对象
- 三种可等待对象 ：
  - 协程对象
  - Future
  - Task对象
- await 等待后面跟的协程对象返回之后，再执行后面代码。



- 示例:1

~~~python

import asyncio

async def func():
	print('test')
    response = await asyncio.sleep(2)
    print('任务执行完成', response)
    
async_obj = func()
asyncio.run(async_obj)
    



~~~

- 示例：2

~~~python
import asyncio

async def func():
	print('test')
    response = await asyncio.sleep(2)
    print('任务执行完成', response)
  
async def main():
    print('main')
    await func()
    print('main结束' )
async_obj = main()
asyncio.run(async_obj)

~~~



- 示例：3

~~~python
import asyncio

async def func():
	print('test')
    response = await asyncio.sleep(2)
    print('任务执行完成', response)
  
async def main():
    print('main')
    await func()
    print('main结束' )
    
    print('main2')
    await func()
    print('main结束2' )
async_obj = main()
asyncio.run(async_obj)

~~~



##### 5.4 task对象

~~~python
作用：
	task对象用于并发调度协程。
	会自动往事件循环中添加多个任务。
三种创建方式：
	asyncio.create_task(协程对象) 
	loop.create_task(协程对象)
	ensure_future(协程对象)
	
	注意： asyncio.create_task()函数在python3.7才被引入，
	之前的可以使用ensure_future()函数创建，
	
~~~

- ​	示例1：

```python
import asyncio

async def func():
    print('test')
    response = await asyncio.sleep(2)
    print('任务完成')
    return f'执行_____完成： {response}'


async def main():
    print('main')
    ret1 = asyncio.create_task(func())
    ret2 = asyncio.create_task(func())
    
    res1 = await ret1
    res2 = await ret2
    print('主线程运行')
    print('main结束2')


async_obj = main()
asyncio.run(async_obj)
```



- 示例2  - - 列表task写法：

```python

async def func():
    print('test')
    response = await asyncio.sleep(2)
    print('任务完成')
    return f'执行_____完成： {response}'


async def main():
    print('main')
    
    # 注意  name='n1' name修改3.8以上才能修改
    task_list = [
        asyncio.create_task(func(), name='n1'),
        asyncio.create_task(func(), name='n2')
    ]
    done, padding = await asyncio.wait(task_list, timeout=3)
    print(done)
    print(padding)
    print('主线程运行')


async_obj = main()
asyncio.run(async_obj)


```



- 示例3：

```python


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
```



##### 5.5  asyncio.Future对象

- Task继承Future对象，Task对象内部await结果处理 是基于Future对象来的



- 示例1：

```python
async def main()
	# 获取当前事件循环
    loop = asyncio.get_running_loop()
    
    # 创建一个任务（Future对象）， 这个任务什么都不做
    fut = loop.create_future()
    
    # 等待任务最终的结果（future对象），没有结果则会一直等待下去。
    await fut
    
asyncio.run(main())

```



##### 5.6  concurent.futures.Future对象

注：跟asyncio中的Future没有关系

作用：使用线程池、进程池实现异步操作的时候使用到的对象



##### 5.7asyncio + 不支持异步模块的使用

- 示例1 爬虫案例

```python

```



##### 5.7 异步迭代器

- 定义: 内部实现了__aiter__()方法  __anext__()方法

```python
内部的循环去取  内部的对象  不行 不听不听  我要你来嘛~~

```



