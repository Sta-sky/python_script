import time

import jwt

# 定义加密所使用的密钥
SECRET_KEY = 'mysecretkey'

# 定义payload

def genrate_token(username):
    payload = {
        'username': username,
        'exp': time.time() + 24 * 60 * 60
    }
    
    # 生成token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print(token)
    return  token

def parse_token(token):

    try:
        # 解码token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        # token过期
        print('Token expired !')
    except jwt.InvalidTokenError:
        # token无效
        print('Invalid token !')

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJleHAiOjE2Nzg2MDI2NjMuMDQ1OTYyNn0.8QHY95wPz6PNlsEwcy56wD_r-PtGIkd3POqZtUyuu9o'

username =  'root'

# genrate_token(username)

parse_token(token)