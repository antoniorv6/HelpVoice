import pika

class RabbitMQModule():
    def __init__(self, channel) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=channel)
        
    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key='hello', body=message)
    
    def __del__(self):
        self.connection.close()
