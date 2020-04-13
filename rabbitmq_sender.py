#coding:utf-8
#example of sender module for rabbitmq realized in composition design pattern

import datetime
try:
    import pika
except Exception as e:
    print(f'ER - pika module missing: {e}')

class Singleton(type):
    '''Singleton design pattern realised like metaclass'''
    _instance = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instance:
            #self._instance[self] = super(RabbitMQ_singleton, self).__call__(*args, **kwargs)
            self._instance.update({self:super(Singleton, self).__call__(*args, **kwargs)})
            return self._instance.get(self)

class Rabbitmqsenderconfig(metaclass=Singleton):
    def __init__(self, queuetitle_str = 'hello', hostpath_str = 'localhost', exchange_str =''):
        '''queuetitle_str - is title of queue inside of Rabbitmq'''
        self.queuetitle_str = queuetitle_str
        self.hostpath_str = hostpath_str
        self.exchange_str = exchange_str


class Rabbitmqsender():
    '''organized accordingly composition design pattern, where ser'''
    def __init__(self, rabbitmqsenderconfig_obj):
        self.rabbitmqcfg_obj = rabbitmqsenderconfig_obj
        self._connection_obj = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmqcfg_obj.hostpath_str))
        self.channel_obj = self._connection_obj.channel()
        self.channel_obj.queue_declare(queue=self.rabbitmqcfg_obj.queuetitle_str)

    def publishpayload_fc(self, payload_dc):
        '''method for sending something to queue as a string'''
        self.channel_obj.basic_publish(exchange=self.rabbitmqcfg_obj.exchange_str,
                          routing_key=self.rabbitmqcfg_obj.queuetitle_str,
                          body=str(payload_dc)
                          )
        print(f"Msg published to queue: {payload_dc}")

    def __del__(self):
        self._connection_obj.close()

if __name__ == '__main__':
    queuetitle_str = 'hello'
    hostpath_str = 'localhost'
    exchange_str = ''
    print(f'OK - start testing rabbitMQ sender with such paramters:\ntitle of queue on server = {queuetitle_str}\nserver path = {hostpath_str}\nexchange_str = {exchange_str}')
    try:
        rabbitmqconfigure_obj = Rabbitmqsenderconfig(queuetitle_str, hostpath_str, exchange_str)
        rmqsender_obj = Rabbitmqsender(rabbitmqconfigure_obj)
        rmqsender_obj.publishpayload_fc(payload_dc={"Data":f"Hello payload {datetime.datetime.now()}"})
    except Exception as e:
        print(e)
