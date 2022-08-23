import firebase_admin

class DBModule:

    def __init__(self, url) -> None:
        self.base_url = url
        credentials = firebase_admin.credentials.Certificate("credentials.json")

    def get(self, sub_url):
        reference = db.reference(f"{self.base_url}{sub_url}")
        return reference.get()

