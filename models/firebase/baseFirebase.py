import os
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from models.firebase.mealModel import MealModel
from utils.directory import directory


class BaseFirebase:
    def __init__(self, loop: asyncio.AbstractEventLoop, default_path: str | None = None):
        self.loop = loop
        path = os.path.join(directory, "config", "token.json")
        self.card = credentials.Certificate(path)
        firebase_admin.initialize_app(self.card, {
            'databaseURL': "https://everflow-knumeal-default-rtdb.firebaseio.com"
        })

        self.firebase_dir = db.reference()

    def update_data(self, path: str | None = None, data: MealModel | None = None):
        self.firebase_dir = db.reference(path=path)
        self.firebase_dir.update(data)

    @property
    def get_data(self, path: str | None = None, param: str | None = None) -> MealModel:
        self.firebase_dir = db.reference(path=path)
        data = self.firebase_dir.get()

        return data
