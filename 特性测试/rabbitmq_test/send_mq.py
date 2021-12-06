import pika


# 链接远程机器 用户名密码认证
def send_vm_info(body):
    credentials = pika.PlainCredentials('isoon_admin', 'Isoon_Admin')

    # 建立socket
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '127.0.0.1', 5672, '/', credentials))
    # 建立rabbit协议通道
    channel = connection.channel()
    # 声明队列
    channel.basic_publish(
        exchange='',
        routing_key='vm_test',
        body=body
    )
    channel.close()
    print('发送端消息发送成功，通道关闭')


send_vm_info('hello world')













