try:
    import pika
except Exception as e:
    print('Pika module dont imported')

connection_obj = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel_obj = connection_obj.channel()

channel_obj.queue_declare(queue='hello')

def callback_fc(channel_obj, method_obj, properties_obj, body_obj):
    print(f"[x] Received {body_obj}")

channel_obj.basic_consume(
    queue='hello',
    on_message_callback=callback_fc,
    auto_ack=True
)

print('[x] Waiting for messages. To exit press CTRL+C')
channel_obj.start_consuming()