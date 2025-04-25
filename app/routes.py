import logging
import os
import random
import time
from typing import Optional

import httpx
from fastapi import APIRouter, Response

TARGET_ONE_SVC = os.environ.get("TARGET_ONE_SVC", "localhost:8000")
TARGET_TWO_SVC = os.environ.get("TARGET_TWO_SVC", "localhost:8000")

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def read_root():
    logger.info("Hello World")
    return {"msg": "Hello World"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logger.info("items")
    return {"item_id": item_id, "q": q}


@router.get("/io_task")
async def io_task():
    time.sleep(1)
    logger.info("io task")
    return "IO bound task finish!"


@router.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    logger.info("cpu task")
    return "CPU bound task finish!"


@router.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logger.info("random status")
    return {"path": "/random_status"}


@router.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logger.info("random sleep")
    return {"path": "/random_sleep"}


@router.get("/info_test")
async def info_test(response: Response):
    logger.info("got error!!!!")
    raise ValueError("value error")


@router.get("/chain")
async def chain(response: Response):
    logger.info("Chain Start")

    async with httpx.AsyncClient() as client:
        await client.get(
            "http://localhost:8000/",
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            f"http://{TARGET_ONE_SVC}/io_task",
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            f"http://{TARGET_TWO_SVC}/cpu_task",
        )
    logger.info("Chain Finished")
    return {"path": "/chain"}
