import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram import BaseMiddleware
from dotenv import load_dotenv
from aiogram.enums import ParseMode
import os
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup


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
            logging.info(
                f"Received message from {event.message.from_user.username}: {event.message.text}"
            )
        else:
            logging.info(f"Received update: {event}")
        return await handler(event, data)


bot = Bot(
    token=os.getenv("API_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.update.middleware(LoggingMiddleware())
router = Router()


class Registration(StatesGroup):
    waiting_for_username = State()
    waiting_for_email = State()
    waiting_for_password = State()


class Login(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


