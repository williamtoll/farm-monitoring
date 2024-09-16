from appberry.models import Item
import os
import logging
from pathlib import Path
from fastapi import APIRouter


logFile = Path(os.getenv("LOG_FOLDER") + "/irrigation.log")


logging.basicConfig(
    filename=logFile,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)


router = APIRouter()

@router.get("/irrigation")
def irrigation_list():
    return {"status": "ok"}

# @router.post("/irrigation-schedule")
# def schedule_irrigation(item: Item):
#     logger.info("Running schedule_irrigation")
#     logger.info("item: %s", item)

#     return {}


# @router.post("/irrigation-start")
# def start_irrigation(item: Item):
#     logger.info("Running start_irrigation")
#     logger.info("item: %s", item)

#     return {}


# @router.post("/irrigation-stops")
# def stop_irrigation(item: Item):
#     logger.info("Running stop_irrigation")
#     logger.info("item: %s", item)

#     return {}
