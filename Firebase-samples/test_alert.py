import requests
def alertFamily():
    headers={'Accept': 'application/json', 
        'Authorization': 'key=AAAAoZTf-J0:APA91bHCsxJymN-5ZVFPYzWJQ5ZaEBFC2gWhs2DLutcP6flxMVxTaZKXXVqNxtaUKeOOTgcJo5RTlJiZZGgjZDnR5jFtAFR_slJ_d9Gpf_eWzMUKSLEWvJ2mBl2oaOxE2DyjULNefI8r'
    }
    data = {
    "to":"cKVVzWkqRhCdM2bAvN7T_h:APA91bGaSOjJOsm-JLgNFfep-1pOOnUyGti7q2Sh5cgDYE0MNJk_pIJ_4nW5UNbQC7vnEs4qGnN21-RdxdzA7b0Zwx-1pyH1ebbK0oCO4z90TE-G3BM1AuTIULC7tWwIfU1HCRDQ-YDX",
    "notification":{
        "title":"HelpVoice! - Nueva alerta",
        "body":"Alberto Berenguer"
    },
    "data":{
        "lat":40.4477155,
        "lon": -3.6954323,
        "status": "Una ambulancia está en camino",
        "pred": "Rotura de cadera"
    }
    }
    requests.post('https://fcm.googleapis.com/fcm/send', json = data,
    headers = headers)




alertFamily()