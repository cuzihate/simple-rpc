# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import pika
import subprocess

get_server_ip = '/sbin/ifconfig|grep "inet addr"|grep -v 127.0.0.1|sed -e "s/^.*addr://;s/Bcast.*$//"'
result = subprocess.Popen(get_server_ip, shell=True, stdout=subprocess.PIPE)
ip = result.stdout.read().decode().strip()  # 获取本机IP

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.111.134'))
channel = connection.channel()

channel.exchange_declare(exchange='rpc', type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='rpc', queue=queue_name, routing_key=ip)



def task_mission(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = result.stdout.read()
    if not result:
        return ip + ': 输入命令不合法\n'
    return ip + ':\n' + result.decode()


def on_request(ch, method, props, body):  # 接收客户端信息
    body = body.decode()
    print(" [.] 执行的命令：%s" % body)
    response = task_mission(body)  # 处理消息

    ch.basic_publish(exchange='',  # 再将返回值发送给客户端
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=queue_name)

print(" [x] Awaiting RPC requests")
channel.start_consuming()