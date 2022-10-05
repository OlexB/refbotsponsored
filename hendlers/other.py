from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_refbot import dp, bot
from database import sqlite_db as sq
from config import ADMIN_ID
from markups import client_mkr, admin_mkr
import random
import datetime

class FSMOther(StatesGroup):
    capcha = State()

class FSMAdmin(StatesGroup):
    admin = State()

class FSMUsers(StatesGroup):
    users = State()

# Команда страрт
async def cmd_capcha(message: types.Message, state: FSMContext):
    async with state.proxy() as other_data:
        if message.chat.type == 'private':
            if message.from_user.id == ADMIN_ID:
                if not await sq.user_exists(message.from_user.id):
                    await sq.add_user(message.from_user.id, message.from_user.username)
                    await message.answer(f'Панель адміністратора', reply_markup=admin_mkr.AdminMenu)
                    await FSMAdmin.admin.set()
                else:
                    await message.answer(f'Панель адміністратора', reply_markup=admin_mkr.AdminMenu)
                    await FSMAdmin.admin.set()
            elif message.from_user.id != ADMIN_ID:
                if not await sq.user_exists(message.from_user.id):
                    start_command = message.text
                    referer_id = str(start_command[7:])
                    if str(referer_id) != "": 
                        if str(referer_id) != str(message.from_user.id):
                            other_data['referer_id'] = referer_id
                            other_data['capcha'] = random.randint(0,9999)
                            other_data['data'] = datetime.date.today()
                            await message.answer(f"Підтвердіть що ви не робот\nВведіть число: {other_data['capcha']}")
                            await FSMOther.capcha.set()
                        else:
                            await message.answer('Реєструватися по своїй ссилці заборонено!')
                    else:
                        other_data['capcha'] = random.randint(0,9999)
                        other_data['referer_id'] = None
                        other_data['data'] = datetime.date.today()
                        await message.answer(f"Підтвердіть що ви не робот\nВведіть число: {other_data['capcha']}")
                        await FSMOther.capcha.set()
                else:
                    await message.answer('Ви в головному меню', reply_markup=client_mkr.ClientMenu)
                    await FSMUsers.users.set()
            else:
                pass

# Перевірка на робота і реєстрація
async def capcha(message: types.Message, state: FSMContext):
    async with state.proxy() as other_data:
        data = other_data['data']
        if message.text == str(other_data['capcha']):
            if other_data['referer_id'] != None:
                referer_id = other_data['referer_id']
                await sq.add_user(message.from_user.id, message.from_user.username, data, referer_id)
                if await sq.premium_user_exists(message.from_user.id) != 'prem':
                    try:
                        user_balance = await sq.count_users_referal(referer_id)*await sq.default_price_ref()
                        await sq.edit_user_balance(user_balance, referer_id)
                        await bot.send_message(referer_id, f'По вашій ссилці зареєструвався новий користувач\nНа баланс нараховано <b>{await sq.default_price_ref()}</b> грн', parse_mode='HTML')
                    except:
                        pass
                else:
                    try:
                        user_balance = await sq.count_users_referal(referer_id)*await sq.premium_price_ref()
                        await sq.edit_user_balance(user_balance, referer_id)
                        await bot.send_message(referer_id, f'По вашій ссилці зареєструвався новий користувач\nНа баланс нараховано <b>{await sq.premium_price_ref()}</b> грн', parse_mode='HTML')
                    except:
                        pass
                await message.answer("Перевірка пройшла успішно\nВи в головному меню", reply_markup=client_mkr.ClientMenu)
                await bot.send_message(ADMIN_ID, 'Зареєструвався новий користувач')
                await FSMUsers.users.set()
            else:
                await sq.add_user(message.from_user.id, message.from_user.username, data)
                await message.answer("Перевірка пройшла успішно\nВи в головному меню", reply_markup=client_mkr.ClientMenu)
                await bot.send_message(ADMIN_ID, 'Зареєструвався новий користувач')
                await FSMUsers.users.set()
        else:
            await message.answer(f"Не правильно нахуй\nПравильно буде {other_data['capcha']}, а не {message.text}")

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(cmd_capcha, commands=['start'], state=None)
    dp.register_message_handler(capcha, state=FSMOther.capcha)