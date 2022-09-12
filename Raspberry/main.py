from gpiozero import Button
import time
import pyttsx3
import requests

# Voice config
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'spanish+f4')

# API config

url = 'amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'

def saySomething(text):
    engine.say(text)
    engine.runAndWait()

button = Button(18)


def action():
     global button
     counter = 0
     saySomething('Dime')
     
     while True:
        counter+=1
        print(counter)
        if not button.is_pressed:
            data[''] = 
            saySomething('De acuerdo. No se preocupe, la ambulancia está de camino')
            break
    

while True:
    if button.is_pressed:
        action()
"""
print('Lets go')
p= Process(target=action, args=())
while True:
    input_state = gpio.input(18)
    print('jje')
    if input_state == False:
        recoding = True
        p.start()
        
        time.sleep(0.2)
    else:
        recoding = False
"""
