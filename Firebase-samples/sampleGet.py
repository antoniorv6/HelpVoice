import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# Se conecta con la base de datos
cred = credentials.Certificate('firebase-key.json')
default_app = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://helpvoice-aporta-default-rtdb.europe-west1.firebasedatabase.app'})

# Obtenemos la base de datos de alertas
db_alerts = db.reference('/alerts')

# La estructura es la siguientes 
# /alerts/id_usuario/id_alerta/datos_alerta
# Lo puedes revisar desde la web de firebase 

# Documentación firebase python:
# https://firebase.google.com/docs/database/admin/retrieve-data?hl=es-419

# Recorremos todas las alertas
for user in db_alerts.get():
    for alert in db_alerts.get()[user]:
        for key in db_alerts.get()[user][alert].items():
            print(key)