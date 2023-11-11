import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

from utils.directory import directory
from utils.import_supporter import ImportSupporter

app = FastAPI()
background_scheduler = AsyncIOScheduler()
log = logging.getLogger(__name__)

view_image_supporter = ImportSupporter(app)
task_image_supporter = ImportSupporter(background_scheduler)

view_image_supporter.load_modules('routers', directory)
task_image_supporter.load_modules('tasks', directory, after_loaded=lambda: background_scheduler.start())


host = "127.0.0.1"
port = 8000
app_name = "routers.router:app"

if __name__ == "__main__":
    config = uvicorn.Config(app=app_name, host=host, port=port, reload=True)
    server = uvicorn.Server(config=config)
    server.run()
