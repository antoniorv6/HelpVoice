from gpiozero import Button
import time
import pyttsx3
import requests

# Voice config
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'spanish+f4')

# API config



def saySomething(text):
    engine.say(text)
    engine.runAndWait()

button = Button(18)


def action():
     global button
     counter = 0
     saySomething('Dime')
     
     while True:
        if not button.is_pressed:
            data = dict()
            data['client_id'] = 131233 # Set by default

            saySomething('De acuerdo. No se preocupe, la ambulancia está de camino')
            break
    

while True:
    if button.is_pressed:
        action()
