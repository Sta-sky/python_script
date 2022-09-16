

抓包工具：Fiddler【PC】

代码见 `main.py` ，配置文件 `config.py` 需要自行按需修改，具体怎么使用见下方使用教程，t 的值使用软件怎么获取这里不描述，自行探索，懂的都懂，感谢 issues 贡献方法老铁们，集思广益汇集力量，本内容会随时间发生改变，请自行分辨。

环境：python3.9

 `config.py` ，修改抓取的必填t值，其他参数按照注释按需修改
```shell
    # 获取到的header中t值,必须修改为自己的
    "header_t": "eyxxxxxxxxx.xxxx",
    # 获取到的header中的user-agent值
    "header_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
    # 设定的完成耗时，单位s，默认-1随机表示随机生成1s~1h之内的随机数，设置为正数则为固定
    "cost_time": -1,
    # 需要通关的次数，默认1
    "cycle_count": 1
```

执行文件
```python
python3 main.py
```

