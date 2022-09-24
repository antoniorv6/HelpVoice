import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# Se conecta con la base de datos
cred = credentials.Certificate('firebase-key.json')
default_app = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://helpvoice-aporta-default-rtdb.europe-west1.firebasedatabase.app'})

# Obtenemos la base de datos de alertas
db_users = db.reference('users')

# La estructura es la siguientes 
# /alerts/id_usuario/id_alerta/datos_alerta
# Lo puedes revisar desde la web de firebase 

# Documentación firebase python:
# https://firebase.google.com/docs/database/admin/retrieve-data?hl=es-419

for element in db_users.order_by_child('name').equal_to('Alberto').get():
    print(element)