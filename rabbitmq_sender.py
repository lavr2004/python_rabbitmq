try:
    import pika
except Exception as e:
    print('Pika module missing')

connection_obj = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel_obj = connection_obj.channel()

channel_obj.queue_declare(queue='hello')

channel_obj.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello world RabbitMQ!'
                          )
print("Msg published!")
connection_obj.close()