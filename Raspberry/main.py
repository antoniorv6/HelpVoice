from urllib import request
from gpiozero import Button
import pygame
import time
import pika
from pikaConsumer import ThreadedConsumer
import json
import sounddevice as sd
import wavio as wv
from base64 import b64encode
import numpy as np
import os
import requests
import datetime

# Config usuario
user_id = 'yERXYCKKtDN3b9aXNip4s9GWS1z1'

# Voice config
audio_path = os.path.join(os.path.dirname(__file__) ,'audios/')
audios = {}
audios['start'] = "1.mp3"
audios['ok'] = "2.mp3"
pygame.mixer.init()

# RabitMQ config
connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
channel = connection.channel()

# Creamos cola con el id del paciente
channel.exchange_declare(exchange=user_id,
                         exchange_type='fanout')

def alertFamily():
    headers={'Accept': 'application/json', 
        'Authorization': 'key=AAAAoZTf-J0:APA91bHCsxJymN-5ZVFPYzWJQ5ZaEBFC2gWhs2DLutcP6flxMVxTaZKXXVqNxtaUKeOOTgcJo5RTlJiZZGgjZDnR5jFtAFR_slJ_d9Gpf_eWzMUKSLEWvJ2mBl2oaOxE2DyjULNefI8r'
    }

    now = datetime.datetime.now()
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)

    data = {
    "to":"eD4muzh_RO-uEjMGwsHQgE:APA91bHsTsbzaoM4FS5Etk6FOuDTIOFxz5B3xJrRK7SoT_XoJkYHa3nLUYx3FhWsLER58J_Voo5K2awfqf4ybYmnjbKLlKQlqLCVR0oMz8SiGzveR0oOwxZKK8c9a9FNRx4kGQmjual2",
    "notification":{
        "title":"HelpVoice! - Nueva alerta",
        "body":"Alberto Berenguer"
    },
    "data":{
        "lat":40.4477155,
        "lon": -3.6954323,
        "time": hour+":"+minute,
        "status": "Esperando a ser atendida",
        "pred": "---"
    }
}
    requests.post('https://fcm.googleapis.com/fcm/send', json = data,
    headers = headers)

def playsound(file):
    pygame.mixer.music.load(audio_path + file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def sendMessage(msg):
    channel.basic_publish(exchange='',
                         routing_key='patient_alerts',
                         body=json.dumps(msg))
    print('enviado')

# Comenzamos a consumir
consumer = ThreadedConsumer()
consumer.start()
button = Button(18)

def action():
    #global button
    freq = 44100
    playsound(audios['start'])
    recording = np.array([])
    while True:
        tmp = sd.rec(int(freq), 
                   samplerate=freq, channels=1)

        sd.wait()
        recording = np.append(recording, tmp)
        
        if not button.is_pressed:
            wv.write("recording1.wav", recording, freq, sampwidth=2)
            f=open("recording1.wav", "rb")
            enc=b64encode(f.read())
            f.close()

            data = {}
            data['client_id'] = user_id
            data['lat'] = 40.4477155
            data['lon'] = -3.6954323
            data['audio'] = enc.decode('utf-8')
            sendMessage(data)
            playsound(audios['ok'])
            alertFamily()
            break


while True:
    if button.is_pressed:
        action()



connection.close()