import json
import pika
import time
import threading

# Some configuration variables
RABBIT_URL = 'amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'
ROUTING_KEY = ''
QUEUE_NAME = ROUTING_KEY
EXCHANGE = 'yERXYCKKtDN3b9aXNip4s9GWS1z1'
THREADS = 2

class ThreadedConsumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        parameters = pika.URLParameters(RABBIT_URL)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        self.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS*10)
        self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback)
        threading.Thread(target=self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback))

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        time.sleep(1)
        print(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        print ('starting thread to consume from rabbit...')
        self.channel.start_consuming()