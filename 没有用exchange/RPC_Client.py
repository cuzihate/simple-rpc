# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import pika
import uuid

"""
本机是客户端，然后发送命令及新建的队列名称给服务端，
服务端执行完命令，将返回结果发送到客户端发送过来的队列名的队列里面

客户端（发布者）：发送 --> 接收
服务端（订阅者）：接收 --> 发送
"""

import pika
import uuid

class Client(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.111.134'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, cmd):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='rcp',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id,),
                                   body=cmd)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

client = Client()


while True:
    a = input('命令：').strip()
    print(" [x] Requesting dir")
    response = client.call(a)
    print(" [.] Got %r" % str(response, encoding='gbk'))


