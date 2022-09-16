# -*- coding: utf-8 -*-

import os

# 获取到的header中t值,必须修改为自己的
t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0MTUzMjIsIm5iZiI6MTY2MzMxMzEyMiwiaWF0IjoxNjYzMzExMzIyLCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo1NTIwOTAyLCJkZWJ1ZyI6IiIsImxhbmciOiIifQ.i33Z-GA-n-7vEylL-vLZWXtTLD7zP8ViIiAphxfTqoo"
# 以下参数根据自己的需要进行修改：
SYS_CONFIG = {

    "header_t": t,
    # 获取到的header中的user-agent值
    "header_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
    # 设定的完成耗时，单位s，默认-1随机表示随机生成1s~1h之内的随机数，设置为正数则为固定
    "cost_time": -1,
    # 需要通关的次数，默认1
    "cycle_count": 10
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
