from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()

BOT_API = os.getenv("BOT_API")
bot = Bot(token=BOT_API)
dp = Dispatcher()

CHANNELS = ["@g7team_ru"]
