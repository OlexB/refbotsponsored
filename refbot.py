from aiogram.utils import executor
from create_refbot import dp
from database import sqlite_db as sq


async def on_startup(_):
    print('БОТ ОНЛАЙН')
    sq.sql_start()

from hendlers import client, admin, other

other.register_handlers_other(dp)
client.register_handlers_client(dp) 
admin.register_handlers_admin(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)