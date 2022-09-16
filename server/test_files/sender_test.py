#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
channel = connection.channel()

channel.queue_declare(queue='patient_alerts')
channel.queue_declare(queue='hospital_comms')

channel.basic_publish(exchange='', routing_key='patient_alerts', body=json.dumps({"client_id":1234, "audio":"adsfasdf jaiosfjaseiof jaiof hjasdofiu hasdo fiuahdsfija"}))
channel.basic_publish(exchange='', routing_key='hospital_comms', body='Mensaje de hospital!')

print(" [x] Sent 'Hello World!'")
connection.close()