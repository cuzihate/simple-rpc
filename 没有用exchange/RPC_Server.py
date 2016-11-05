# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import pika
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.111.134'))
channel = connection.channel()
channel.queue_declare(queue='rcp')

def task_mission(cmd):

    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = result.stdout.read()
    if not result:
        return bytes('输入命令不合法', encoding='gbk')  # windows
    return result


def on_request(ch, method, props, body):
    body = body.decode()
    print(" [.] 执行的命令：%s" % body)
    response = task_mission(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rcp')

print(" [x] Awaiting RPC requests")
channel.start_consuming()