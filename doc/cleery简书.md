# celery简书



+++

### 公共信息

 **项目目录结构**

~~~python
└─project1
    │  db.sqlite3
    │  gitignore
    │  manage.py
    │
    ├─celery_task
    │  │  delay_task.py
    │  │  main.py
    │  │  user_tasks.py
    │  │  __init__.py
    │
    ├─project1
    │  │  settings.py
    │  │  test.py
    │  │  urls.py
    │  │  wsgi.py
    │  │  __init__.py
    │
    ├─user
    │  │  admin.py
    │  │  apps.py
    │  │  models.py
    │  │  tests.py
    │  │  urls.py
    │  │  views.py
    │  │  __init__.py
~~~

+++





## 1、celery 异步任务

##### 1、异步任务配置文件

~~~python
project1/celery_task/main.py  --- 异步任务的入口配置文件，初始化celery_app对象
	
    
    from celery import Celery

    broken = 'redis://127.0.0.1/4'
    backend = 'redis://127.0.0.1/5'

    # 初始化celery
    app = Celery('project1', broker=broken, backend=backend)

    # 加载配置文件
    app.config_from_object('project1.settings')

    # 自动注册任务
    app.autodiscover_tasks(
        ["celery_task"]
    )

	
~~~

##### 2、 异步任务的编写、调用

~~~python
project1/celery_task/delay_task.py  调用celery_app对象，添加装饰器，创建异步任务

    import random
    from django_redis import get_redis_connection
    from .main import app

    @app.task()
    def write_reids_10():
        redis_obj = get_redis_connection('delay_task')
        keys = str(random.randint(1, 10000))
        val = str(random.randint(1, 10000))
        redis_obj.set(keys, val)

        
project1/user/views.py    视图中调用

from celery_task.delay_task import write_reids_10
res = write_reids_10.delay()
~~~

##### 3、启动celery

~~~python
celery -A celery_task.main worker -l info
~~~





+++





### 2、celery 定时任务  ---- 使用djcelery



##### 1、配置文件

~~~python
project1/project1/settings.py


    import djcelery
    from datetime import timedelta
    DJREIDS_IP = 'redis://@127.0.0.1:6379/'
    # 当djcelery.setup_loader()运行时，Celery便会去查看INSTALLD_APPS下包含的所有app目录中的tasks.py文件，找到标记为task的方法，将它们注册为celery task
    djcelery.setup_loader()
    # 注册app中任务
    CELERY_IMPORTS = ('celery_task.user_tasks', )

    # broker是代理人，它负责分发任务给worker去执行
    BROKER_URL = f'{DJREIDS_IP}1'

    # 任务执行结果
    CELERY_RESULT_BACKEND = f'{DJREIDS_IP}2'
    CELERY_TIMEZONE = TIME_ZONE

    CELERYBEAT_SCHEDULE = {
        'tasks1': {
            # 定时任务一
            'task': 'celery_task.user_tasks.add_redis_data',
            # 每隔5秒执行celery_task.user_tasks.add_redis_data中的任务
            'schedule': timedelta(seconds=5),
            'args': ()

        }
    }
~~~



##### 2、任务编写

~~~python
project1/celery_task/user_task.py	
	from celery import task
    from django_redis import get_redis_connection
    import random

    @task()
    def add_redis_data():
        redis_obj = get_redis_connection('task')
        keys = str(random.randint(1, 10000))
        val = str(random.randint(1, 10000))
        redis_obj.set(keys, val)

~~~



##### 3、djcelery启动任务

~~~python
# 启动worker
python3.6 manage.py celery worker -l info

# 启动定时任务
python3.6 manage.py celery beat -l info
~~~

