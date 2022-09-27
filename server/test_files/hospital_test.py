#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
channel = connection.channel()

channel.queue_declare(queue='patient_alerts')
channel.queue_declare(queue='hospital_comms')

audio_test_content = None
with open('audio_test.txt') as audio_txt:
    audio_test_content = audio_txt.read()

request_body = {
    "user": "usuariomongolardo",
    "transcription":"Me duele mucho todo, pero ando mas flexin con mis panas sisi.",
    "audio_path":"audio_usuario1234.wav",
    "diagnostico": "ulcera",
    "level": "Prioridad Media",
    "level_int": 1,
    "coordinates": [203.45, 112.345]
}

channel.basic_publish(exchange='hospitals', routing_key='hospital1', body=json.dumps(request_body))


connection.close()