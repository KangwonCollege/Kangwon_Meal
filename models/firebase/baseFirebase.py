import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class BaseFirebase:
    def __init__(self, loop: asyncio.AbstractEventLoop, **kwargs):
        self.loop = loop
        self.firebase_dir = None

    def init_db(self, card: credentials.Certificate = None, database_url: str = None):
        firebase_admin.initialize_app(card, {
            "databaseURL": database_url
        })

        self.firebase_dir = db.reference()

    def change_path(self, change_path):
        self.firebase_dir = db.reference(path=change_path)

    def update_db(self, data=None):
        self.firebase_dir.update(data)

    @property
    def get_db(self):
        return self.firebase_dir.get()
