"""
redis中获取储存的成果信息
"""
import redis
r = redis.Redis(host='localhost',db=3,port='6379')

for i in range(1,29):
    key = 'CG'+str(i)
    info = r.lrange(key,0 ,-1)
    count = 0
    for j in info:
        print(j.decode())
        count += 1
        if count >3:
            print('*'*100)
            count = 0

