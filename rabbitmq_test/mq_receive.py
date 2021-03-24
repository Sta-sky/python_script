import pika

credentials = pika.PlainCredentials('isoon_admin', 'Isoon_Admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1', 5672, '/', credentials))
channel = connection.channel()
# 2、创建队列,可以只让一方创建，主要是分不清哪边先跑起来，所以这儿也要创建同样的队列
# channel.queue_declare(queue='vm_score_1')


# 3、构建回调函数
def callback(ch, method, properties, body):
    print(ch, method, properties)
    print(body)


# 确定监听队列：hello，一旦有值出现，则触发回调函数：callback
channel.basic_consume(
                queue='work_queue',
                on_message_callback=callback,
                auto_ack=True,
)

print('监听。。。。。')
channel.start_consuming()
