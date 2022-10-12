import json
import pika
import time

import pygame
import os


# Some configuration variables
RABBIT_URL = 'amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'
ROUTING_KEY = ''
QUEUE_NAME = ROUTING_KEY
EXCHANGE = 'yERXYCKKtDN3b9aXNip4s9GWS1z1'
THREADS = 2
# Voice config

class ThreadedConsumer():
    def __init__(self):

        parameters = pika.URLParameters(RABBIT_URL)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        self.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS*10)
        self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback)
        self.channel.basic_consume(QUEUE_NAME, on_message_callback=self.callback)
        self.audio_path = os.path.join(os.path.dirname(__file__) ,'audios/')
        self.audios = {}

        self.audios['ambulancia'] = "3.mp3"
        pygame.mixer.init()

    def callback(self, channel, method, properties, body):

        body = body.decode().replace("\'", "\"")
        message = json.loads(body)
        time.sleep(1)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        self.stop()
        self.playsound(self.audios['ambulancia'])
        
    def run(self):
        print ('starting thread to consume from rabbit...')
        self.channel.start_consuming()

    def stop(self):
        print ('stopping thread to consume from rabbit...')
        self.channel.stop_consuming()

    def playsound(self, file):
        pygame.mixer.music.load(self.audio_path + file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

