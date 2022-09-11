import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

class DBModule:

    def __init__(self, url) -> None:
        credentials = firebase_admin.credentials.Certificate('firebase-key.json')
        self.db_app = firebase_admin.initialize_app(credentials,  {'databaseURL': 'https://helpvoice-aporta-default-rtdb.europe-west1.firebasedatabase.app'})

    def get(self, sub_url):
        reference = self.db_app.reference(f"{self.base_url}{sub_url}")
        return reference.get()

    def post(self, sub_url, query_update):
        reference = self.db_app.reference(f"{self.base_url}{sub_url}")
        reference.update(query_update)
