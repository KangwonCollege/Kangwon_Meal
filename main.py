import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from utils.directory import directory
from utils.import_supporter import ImportSupporter

app = FastAPI()
background_scheduler = BackgroundScheduler()
log = logging.getLogger(__name__)

view_image_supporter = ImportSupporter(app)
task_image_supporter = ImportSupporter(background_scheduler)

view_image_supporter.load_modules('routers', directory)
task_image_supporter.load_modules('tasks', directory, after_loaded=lambda: background_scheduler.start())
