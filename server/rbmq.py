import pika

class RabbitMQModule:
    def __init__(self, queue) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='alerts', exchange_type='fanout')
        self.queue = queue
    
    def __del__(self):
        self.connection.close()
        
    def send_message(self, message):
        self.channel.basic_publish(exchange='alerts', routing_key='', body=message)
