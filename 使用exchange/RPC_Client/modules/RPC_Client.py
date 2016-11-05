# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

import pika
import uuid
import time

"""
本机是客户端，然后发送命令及新建的队列名称给服务端，
服务端执行完命令，将返回结果发送到客户端发送过来的队列名的队列里面

客户端（发布者）：发送 --> 接收
服务端（订阅者）：接收 --> 发送
"""

class Client(object):
    def __init__(self, sever_list):
        self.sever_list = sever_list

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.111.134'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='rpc', type='direct')

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)
        #  绑定用来接收服务端消息的队列并监听

    def on_response(self, ch, method, props, body):  # 接收服务端信息的函数
        for corr_id in self.sever_list:
            if corr_id == props.correlation_id:
                self.response.append(body.decode())

    def call(self, cmd):  # 发送消息的函数
        self.response = []
        # self.corr_id = str(uuid.uuid4())
        for corr_id in self.sever_list:
            #  发布者，将corr_id既当routing_key，又当correlation_id传递
            self.channel.basic_publish(exchange='rpc', routing_key=corr_id,
                                       properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                       correlation_id=corr_id,),
                                       body=cmd)

        while not self.response or len(self.response) != len(self.sever_list):
            #  一个小bug就是如果长度不等，就会一直hang on ..
            self.connection.process_data_events()
        # time.sleep(0.5)  # 之前想用sleep来等待接收，发现效果不佳
        return self.response


