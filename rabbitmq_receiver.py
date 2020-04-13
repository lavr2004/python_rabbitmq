#coding:utf-8
#example of receiver module for rabbitmq realized in composition design pattern

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

class Rabbitmqreceiverconfig():
    def __init__(self, hostpath_str = 'localhost', queuetitle_str = 'hello'):
        self.hostpath_str = hostpath_str
        self.queuetitle_str = queuetitle_str

class Rabbitmqreceiver(metaclass=Singleton):

    def __init__(self, rabbitmqreceiverconfig_obj):
        self.rmqreceivercfg_obj = rabbitmqreceiverconfig_obj
        self._connection_obj = pika.BlockingConnection(pika.ConnectionParameters(host=self.rmqreceivercfg_obj.hostpath_str))
        self._channel_obj = self._connection_obj.channel()
        self.tmp_obj = self._channel_obj.queue_declare(self.rmqreceivercfg_obj.queuetitle_str)

    def _callback_fc(self, channel_obj, method_obj, properties_obj, body_obj):
        '''method for locking what objects got from queue'''
        print(f"[x] Received channel_obj: {channel_obj}")
        print(f"[x] Received method_obj: {method_obj}")
        print(f"[x] Received properties_obj: {properties_obj}")
        print(f"[x] Received body_obj: {body_obj}")
        print('='*100)

    def process_fc(self, isauto_ack = True):
        ''' main operation of class'''
        self._channel_obj.basic_consume(queue=self.rmqreceivercfg_obj.queuetitle_str, on_message_callback=self._callback_fc, auto_ack=isauto_ack)
        print('[*] Waiting for messages. To exit press CTRL+C')
        self._channel_obj.start_consuming()

if __name__ == '__main__':
    hostpath_str = 'localhost'
    queuetitle_str = 'hello'
    print(f'OK - start testing rabbitMQ sender with such paramters:\ntitle of queue on server = {queuetitle_str}\nserver path = {hostpath_str}')
    try:
        rabbitmqreceivercfg_obj = Rabbitmqreceiverconfig(hostpath_str, queuetitle_str)
        rabbitmqreceiver_obj = Rabbitmqreceiver(rabbitmqreceivercfg_obj)
        rabbitmqreceiver_obj.process_fc()
    except Exception as e:
        print(e)