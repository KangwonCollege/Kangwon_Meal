import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from mealDataclass import MealDatabase


class BaseFirebase:
    def __init__(self, loop: asyncio.AbstractEventLoop, default_path: str | None = None):
        self.loop = loop
        self.card = credentials.Certificate("./token.json")
        firebase_admin.initialize_app(self.card)

        self.firebase_dir = db.reference(default_path)

    def update_data(self, path: str | None = None, data: MealDatabase | None = None):
        self.firebase_dir = db.reference(path=path)
        self.firebase_dir.update(data)

    @property
    def get_data(self, path: str | None = None, param: str | None = None) -> MealDatabase:
        self.firebase_dir = db.reference(path=path)
        data = self.firebase_dir.get()

        return data
