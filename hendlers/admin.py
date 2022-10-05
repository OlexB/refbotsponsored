from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_refbot import dp, bot
from database import sqlite_db as sq
from config import ADMIN_ID
from markups import admin_mkr
import datetime
from datetime import timedelta

class FSMAdmin(StatesGroup):
    admin = State()
    search_id = State()
    search_id_next = State()
    edit_price = State()
    ed_default_price_ref = State()
    ed_premium_price_ref = State()
    ed_premium_ak_price = State()
    minimum_default_out = State()
    minimum_prem_out = State()
    days_3_price = State()
    days_6_price = State()
    days_10_price = State()
    chanel_name = State()
    channel_id = State()
    channel_url = State()
    date_channel = State()
    send = State()

# ============================================ Головне меню =============================================================

async def btn_admin(message: types.Message, state: FSMContext): 
    if message.chat.type == 'private':
# Кнопка "ПОШУК ПО ID"
        if message.text == 'Пошук по ID 🔑':
            await message.answer(f"Введіть ID користувача", reply_markup=types.ReplyKeyboardRemove())
            await FSMAdmin.search_id.set()
        elif message.text == 'Змінити ціни 💵':
            await message.answer(f"Яку ціну змінити?", reply_markup=admin_mkr.EditPrice)
        elif message.text == 'Кількість користувачів 📊':
            await message.answer(f"Всього користувачів: {await sq.count_users()}\nКористувачів без PREMIUM: {await sq.count_users()-await sq.count_users_prem()}\nКористувачів з PREMIUM: {await sq.count_users_prem()}")
        elif message.text == 'Оновити БД 🔄':
            pass
        elif message.text == 'Меню ⬅️':
            await message.answer(f'Панель адміністратора', reply_markup=admin_mkr.AdminMenu)
        elif message.text == 'Додати спонсора 👤':
            await message.answer(f"Введіть підпис кнопки", reply_markup=admin_mkr.spon)
            await FSMAdmin.chanel_name.set()

# ============================================ Меню кнопки "ЗМІНИТИ ЦІНИ" ===================================================
# Кнопка "ЦІНА ЗАРЕФА"
        elif message.text == '📌 Ціна за рефа':
            await message.answer(f"Теперішня ціна: {await sq.default_price_ref()} грн\nВведіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.ed_default_price_ref.set()
# Кнопка "PREMIUM за рефа"
        elif message.text == '📌 PREMIUM за рефа':
            await message.answer(f"Теперішня ціна: {await sq.premium_price_ref()} грн\nВведіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.ed_premium_price_ref.set()
# Кнопка "ЦІНА СПОНСОРКИ"
        elif message.text == '📌 Ціна спонсорки':
            await message.answer(f"Теперішня ціна:\nНа 3 дні: {await sq.sp_3days_price()} грн\nНа 6 днів: {await sq.sp_6days_price()} грн\nНа 10 днів: {await sq.sp_10days_price()}")
            await message.answer(f"Виберіть яку ціну змінити", reply_markup=admin_mkr.Sponsor_day)
# Кнопка "ЦІНА PREMIUM"
        elif message.text == '📌 Ціна PREMIUM':
            await message.answer(f"Теперішня ціна: {await sq.premium_ak_price()} грн\nВведіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.ed_premium_ak_price.set()
# Кнопка "ЗВИЧАЙНИЙ ВИВІД"
        elif message.text == '📌 Звичайний вивід':
            await message.answer(f"Теперішній поріг: {await sq.minimum_default_out()} грн\nВведіть новий поріг", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.minimum_default_out.set()    
# Кнопка "ВИВІД PREMIUM"
        elif message.text == '📌 Вивід PREMIUM':
            await message.answer(f"Теперішній поріг: {await sq.minimum_prem_out()} грн\nВведіть новий поріг", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.minimum_prem_out.set()

# ============================================ Меню кнопки "ЦІНА СПОНСОРКИ" =================================================
# Кнопка "НА 3 ДНІ"
        elif message.text == '📌 Ціна на 3 дні':
            await message.answer(f"D\Введіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.days_3_price.set() 
# Кнопка "НА 6 ДНІВ"
        elif message.text == '📌 Ціна на 6 днів':
            await message.answer(f"D\Введіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.days_6_price.set() 
# Кнопка "НА 10 ДНІВ"
        elif message.text == '📌 Ціна на 10 днів':
            await message.answer(f"D\Введіть нову ціну", reply_markup=admin_mkr.Out_in)
            await FSMAdmin.days_10_price.set()

# =============================================== СИСТЕМНА ЧАСТИНА ==========================================================
# === Додати спонсора ===
# Назва кнопки "Спонсовано"
async def chanel_name(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        chanel_name = message.text
        admin_data['chanel_name'] = chanel_name
        if message.text == 'Спонсовано 👑':
            await message.answer(f"Додано ✅", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"Введіть ID каналу", reply_markup=types.ReplyKeyboardRemove())
            await FSMAdmin.channel_id.set()
        else:
            await message.answer(f"⚠️ Не коректна назва ⚠️", reply_markup=types.ReplyKeyboardRemove())
# Додати ID каналу спонсора
async def channel_id(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        channel_id = message.text
        admin_data['channel_id'] = channel_id
        if message.text[0] == '-':
            await message.answer(f"Додано ✅", reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"Введіть ссилку на канал спонсора", reply_markup=types.ReplyKeyboardRemove())
            await FSMAdmin.channel_url.set()
        else:
            await message.answer(f"⚠️ Не коректний ID ⚠️", reply_markup=types.ReplyKeyboardRemove())
# Додати ссилку на канла спонсора
async def channel_url(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        channel_url = message.text
        admin_data['channel_url'] = channel_url
        if message.text[:8] == 'https://':
            await message.answer(f"Назначте період днів:", reply_markup=admin_mkr.Sp_data_del)
            await FSMAdmin.date_channel.set()
        else:
            await message.answer(f"⚠️ Не коректна ссилка ⚠️", reply_markup=types.ReplyKeyboardRemove())
# Додати термін спонсорки
async def date_channel(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        if message.text.isdigit():
            days = int(message.text)
            data_delete = datetime.date.today() + timedelta(days=days)
            await sq.aad_channel(data_delete, admin_data['chanel_name'], admin_data['channel_id'], admin_data['channel_url'])
            await message.answer(f"Спонсора додано успішно ✅", reply_markup=admin_mkr.AdminMenu)
            await bot.send_message(admin_data['search_id'], f"Ваш канал додано до списку спонсорів ✅")
            await FSMAdmin.admin.set()
        else:
            await message.answer(f"⚠️ Це не число ⚠️")
# === Додати спонсора ===
# Пошук по ID
async def search_id(message: types.Message, state: FSMContext):
        async with state.proxy() as admin_data:
            search_id = int(message.text)
            admin_data['search_id'] = search_id
            if search_id == await sq.user_search_id(search_id):
                await message.answer(f"Користувач знайдений: @{await sq.give_username(search_id)}", reply_markup=admin_mkr.UpdateUsers)
                await FSMAdmin.search_id_next.set()
            else:
                await message.answer(f"Користувач не знайдений(")
# Дії після пошуку по ID
async def search_id_in(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        if message.chat.type == 'private':
            if message.text == 'Видати PREMIUM ⭐️':
                Premiu_id = 'prem'
                users_id = admin_data['search_id']
                await sq.get_premium(Premiu_id, users_id)
                await message.answer(f"PREMIUM видано успішно ✅")
                await bot.send_message(users_id, f"PREMIUM акаунт активовано ✅\nПриємного користування 🙂")
                await FSMAdmin.admin.set()
            elif message.text == 'Інформація 📚':
                user_id = admin_data['search_id']
                await message.answer(f"<b>Інформація про користувача</b> 📚:\n\nID користувача: <b>{user_id}</b>\nДата реєстрації: <b>{await sq.data_reg(user_id)}</b>\nUsername користувача: @{await sq.username(user_id)}\nКарта користувача: <b>{await sq.give_user_kart(user_id)}</b>\nПреміум акаунт: {await sq.premium_user_ex(user_id)}\nЗапросив людей: <b>{await sq.count_referal(user_id)}</b>\nБаланс користувача: <b>{await sq.user_balance(user_id)}</b> грн\nВивів грошей: <b>{await sq.user_balance_out(user_id)}</b> грн", parse_mode='HTML')
                await FSMAdmin.admin.set()
            elif message.text == 'Видалити PREMIUM ❌':
                users_id = admin_data['search_id']
                await sq.delete_PREMIUM(users_id)
                await message.answer(f"PREMIUM видалено успішно ✅")
                await bot.send_message(users_id, f"PREMIUM акаунт деактивовано ❌")
                await FSMAdmin.admin.set()
            elif message.text == 'Написати ✉️':
                await message.answer(f"Напишіть повідомлення")
                await FSMAdmin.send.set()
# Обработчик калбек
async def callback_cmd_admin(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'out':
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await FSMAdmin.admin.set()
# ============= Обработчики запросів на зміну цін ====================
# Зміна ціни за реферала на спотовому акаунті
async def default_price_ref(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_default_price_ref(message.text)
        await message.answer(f'Ціну змінено на: {await sq.default_price_ref()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# Зміна ціни за реферала на PREMIUM акаунті
async def premium_price_ref(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_premium_price_ref(message.text)
        await message.answer(f'Ціну змінено на: {await sq.premium_price_ref()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# Зміна ціни за реферала на PREMIUM акаунті
async def premium_ak_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_premium_ak_price(message.text)
        await message.answer(f'Ціну змінено на: {await sq.premium_ak_price()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# Зміна мінімального виводу на стоковому акаунті
async def minimum_default_out(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_minimum_default_out(message.text)
        await message.answer(f'Ціну змінено на: {await sq.minimum_default_out()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# Зміна мінімального виводу на PREMIUM акаунті
async def minimum_prem_out(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_minimum_prem_out(message.text)
        await message.answer(f'Ціну змінено на: {await sq.minimum_prem_out()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# Ціни на спонсорку
# НА 3 ДНІ
async def days_3_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_sp_3days_price(message.text)
        await message.answer(f'Ціну змінено на: {await sq.sp_3days_price()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# НА 6 ДНІВ
async def days_6_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_sp_6days_price(message.text)
        await message.answer(f'Ціну змінено на: {await sq.sp_6days_price()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# НА 10 ДНІВ
async def days_10_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await sq.ed_sp_10days_price(message.text)
        await message.answer(f'Ціну змінено на: {await sq.sp_10days_price()} грн', reply_markup=admin_mkr.EditPrice)
        await FSMAdmin.admin.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')
# ============= Обработчики запросів на зміну цін ====================
# Написати повідомлення користувачу
async def send_mess(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        await bot.send_message(admin_data['search_id'], message.text)
        await message.answer('Повідомлення відправлено ✅', reply_markup=admin_mkr.UpdateUsers)
        await FSMAdmin.admin.set()

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(btn_admin, state=FSMAdmin.admin)
    dp.register_message_handler(search_id, state=FSMAdmin.search_id)
    dp.register_callback_query_handler(callback_cmd_admin, state=FSMAdmin.all_states)
    dp.register_message_handler(default_price_ref, state=FSMAdmin.ed_default_price_ref)
    dp.register_message_handler(premium_price_ref, state=FSMAdmin.ed_premium_price_ref)
    dp.register_message_handler(premium_ak_price, state=FSMAdmin.ed_premium_ak_price)
    dp.register_message_handler(minimum_default_out, state=FSMAdmin.minimum_default_out)
    dp.register_message_handler(minimum_prem_out, state=FSMAdmin.minimum_prem_out)
    dp.register_message_handler(days_3_price, state=FSMAdmin.days_3_price)
    dp.register_message_handler(days_6_price, state=FSMAdmin.days_6_price)
    dp.register_message_handler(days_10_price, state=FSMAdmin.days_10_price)
    dp.register_message_handler(search_id_in, state=FSMAdmin.search_id_next)
    dp.register_message_handler(chanel_name, state=FSMAdmin.chanel_name)
    dp.register_message_handler(channel_id, state=FSMAdmin.channel_id)
    dp.register_message_handler(channel_url, state=FSMAdmin.channel_url)
    dp.register_message_handler(date_channel, state=FSMAdmin.date_channel)
    dp.register_message_handler(send_mess, state=FSMAdmin.send)