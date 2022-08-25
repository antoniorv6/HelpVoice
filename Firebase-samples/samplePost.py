import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

# Se conecta con la base de datos
cred = credentials.Certificate('firebase-key.json')
default_app = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://helpvoice-aporta-default-rtdb.europe-west1.firebasedatabase.app'})

# Obtenemos la base de datos de alertas
db_alerts = db.reference('/alerts')

# Dentro de update() le metes el json que quieras

db_alerts.update({
    'id_alerta_2': {
        'id_usuario': '091824014u',
        'lat': '18.322314',
        'lon': '-0.421312452'
    }
})