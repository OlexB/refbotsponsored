import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config as cfg
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)