import asyncio

from models.firebase.baseFirebase import BaseFirebase
from models.firebase.mealModel import MealModel


class RequestFirebase(BaseFirebase):
    def __init__(self, loop=asyncio.AbstractServer):
        super(RequestFirebase, self).__init__(loop=loop)
        self.data: MealModel | None = None

    def upload(self):


    def edit(self):

    def delete(self):

    def load(self):
