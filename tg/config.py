import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Update
from aiogram import BaseMiddleware
from dotenv import load_dotenv
import os


if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


load_dotenv()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            logging.info(f"Received message from {event.message.from_user.username}: {event.message.text}")
        else:
            logging.info(f"Received update: {event}")
        return await handler(event, data)



bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())
router = Router()
dp.include_router(router)
