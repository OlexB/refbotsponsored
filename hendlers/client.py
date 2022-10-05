from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_refbot import bot
from database import sqlite_db as sq
from config import ADMIN_ID, NOT_SUB_MESSAGE, BOT_NICKNAME
from markups import client_mkr
import datetime
import re


class FSMUsers(StatesGroup):
    users = State()
    Tarif = State()
    url = State()
    zajavka = State()
    zajavka_prem = State()
    addedit_kart = State()
    sum = State()

# ============================================ Головне меню =============================================================

async def btn_client(message: types.Message, state: FSMContext): 
    if message.chat.type == 'private':
# Кнопка "МІЙ КАБІНЕТ"
        if message.text == 'Мій кабінет 👤':
            await message.answer(f"Мій кабінет 👤", reply_markup=client_mkr.KabinetMarkups)
# Кнопка "АДМІНІСТРАТОР"
        elif message.text == 'Адміністратор ⭐️':
            await message.answer(f"Щоб написати адміністратору натисніть кнопку нижче", reply_markup=client_mkr.Admin)
# Кнопка "Відгуки"
        elif message.text == 'Відгуки 🗣':
            await message.answer(f"Щоб залишити відгук перейдіть в чат з відгуками", reply_markup=client_mkr.Reviews)
# Кнопка "НАШІ СПОНСОРИ"
        elif message.text == 'Наші спонсори 📌':
            sponsor = await sq.give_sponsor()
            await message.answer(f"Список наших спонсорів 📌", reply_markup=client_mkr.sponsor_markups(sponsor))
# Кнопка "СТАТИ СПОНСОРОМ"
        elif message.text == 'Стати спонсором 🔑':
            await message.answer(f"⚠️ Щоб додати свій канал до списку спонсорів потрібно зробити канал публічним і додати цього бота в адміністратори вашого каналу\n❗️ Інакше бот не зможе перевіряти чи підписалися користувачі на ваш канал", reply_markup=client_mkr.next_sponsor)
            await message.answer(f"Якщо з'явились питання напишіть адміністратору", reply_markup=client_mkr.Admin)
# Кнопка "PREMIUM"
        elif message.text == 'PREMIUM 💎':
            if await sq.premium_user_exists(message.from_user.id) != 'prem':
                await message.answer(f"Можливості <b>PREMIUM</b>:\n💎 Мінімальний поріг виводу <b>{await sq.minimum_prem_out()}</b> грн\n💎 Ціна за кожного реферала <b>{await sq.premium_price_ref()}</b> грн\n💎 Знижка на спонсорство\n💎 Швидка обробка заявок на вивід\n\n📌 Вартість <b>PREMIUM</b> акаунту складає <b>{await sq.premium_ak_price()}</b> грн (<b>НАЗАВЖДИ</b>)", parse_mode='HTML', reply_markup=client_mkr.PremMune)
            else:
                await message.answer(f"<b>PREMIUM</b> акаунт уже активний ✅\nПриємного користування 🙂",parse_mode='HTML', reply_markup=client_mkr.ClientMenu)

# ===================================== Меню кнопки "МІЙ КАБІНЕТ" =======================================================

# Кнопка "ІНФОРМАЦІЯ"
        elif message.text == 'Інформація 📖':
            await message.answer(f"<b>Інформація</b> 📖\n\nДата реєстрації: <b>{await sq.data_reg(message.from_user.id)}</b>\nВаш баланс: <b>{await sq.user_balance(message.from_user.id)} грн</b> 💵\nКількість рефералів: <b>{await sq.count_referal(message.from_user.id)}</b> 👥\nЗнято грошей: <b>{await sq.user_balance_out(message.from_user.id)} грн</b> 💵\nВаша карта: <b>{await sq.give_kart_inf(message.from_user.id)}</b> 💳\nPREMIUM акаунт: {await sq.premium_user_ex(message.from_user.id)}", reply_markup=client_mkr.Out_in, parse_mode='HTML')
# Кнопка "МОЇ РЕКВІЗИТИ"
        elif message.text == 'Мої реквізити 💳': 
            if await sq.user_kart_exists(message.from_user.id) == True:
                await message.answer(f"Ваша карта: 💳\n{await sq.give_user_kart(message.from_user.id)}", reply_markup=client_mkr.requisitesMENU)
            else:
                await message.answer(f'⚠️ Ви ще не додали карту ⚠️', reply_markup=client_mkr.add_kart)
# Кнопка "ВИВЕСТИ ГРОШІ"
        elif message.text == 'Вивести гроші 💸': 
            sponsor = await sq.give_sponsor()
            if await sq.user_kart_exists(message.from_user.id) == True:
                try:
                    if await check_sub_channels(await sq.give_ID_sponsor(), message.from_user.id):
                        await message.answer('Ведіть суму яку бажаєте вивести')
                        await FSMUsers.sum.set()
                    else:
                        await message.answer(NOT_SUB_MESSAGE, reply_markup=client_mkr.sponsor_markups(sponsor))
                except:
                    await bot.send_message(ADMIN_ID, "Хтось з спонсорів не додав бота в адміни")
                    await message.answer('Ведіть суму яку бажаєте вивести')
                    await FSMUsers.sum.set()
            else:
                await message.answer('⚠️ Ви ще не додали карту ⚠️', reply_markup=client_mkr.add_kart)
# Кнопка "МОЯ ССИЛКА"
        elif message.text == 'Моя ссилка 🔗':
            sponsor = await sq.give_sponsor()
            try:
                if await check_sub_channels(await sq.give_ID_sponsor(), message.from_user.id):
                    await message.answer(f"Ваша ссилка: https://t.me/{BOT_NICKNAME}?start={message.from_user.id}", reply_markup=client_mkr.KabinetMarkups)
                else:
                    await message.answer(f"❗️ Щоб отримати свою реферальну ссилку потрібно підписатися на всі канали спонсорів", reply_markup=client_mkr.sponsor_markups(sponsor))
            except:
                await bot.send_message(ADMIN_ID, f"Хтось з спонсорів не додав бота в адміни {sq.give_ID_sponsor()}")
                await message.answer(f"Ваша ссилка: https://t.me/{BOT_NICKNAME}?start={message.from_user.id}", reply_markup=client_mkr.KabinetMarkups)
# Кнопка "ГОЛОВНЕ МЕНЮ"
        elif message.text == 'Головне меню ⬅️': 
            await message.answer(f"Головне меню ⬅️", reply_markup=client_mkr.ClientMenu)

# ===================================== Меню кнопки "СТАТИ СПОНСОРОМ" =======================================================
# Кнопка "ПРОДОВЖИТИ"
        elif message.text == 'Продовжити ✅':
            await message.answer(f"Виберіть бажаний тариф:\n\n🟢 <b>На 3 дні</b>\nПрихід <b>50-150</b> підписників 👥\nВаіртість <b>{await sq.sp_3days_price()}</b> грн 💵\n(<b>Для PREMIUM {await sq.sp_3days_price()-20} грн</b>)\n\n🟢 <b>На 6 днів</b>\nПрихід <b>200-300</b> підписників 👥\nВартість <b>{await sq.sp_6days_price()}</b> грн 💵\n(<b>Для PREMIUM {await sq.sp_6days_price()-20} грн</b>)\n\n🟢 <b>На 10 днів</b>\nПрихід <b>400-500</b> підписників 👥\nВартість <b>{await sq.sp_10days_price()}</b> грн 💵\n(<b>Для PREMIUM {await sq.sp_10days_price()-20} грн</b>)", reply_markup=client_mkr.Tarif , parse_mode='HTML')
            await FSMUsers.Tarif.set()
        
# ========================================= Меню кнопки "PREMIUM" ===========================================================
# Кнопка "КУПИТИ ПРЕМІУМ"
        elif message.text == 'Купити преміум 💎':
            await message.answer(f"PREMIUM акаунт буде активовано після оплати\nВартість послуги: <b>{await sq.premium_ak_price()}</b> грн\nРеквізити для оплати:\n💳 Privat24: 5457082223804449\n💳 mono: 5375414127416989\n\nЧекаю скрін оплати 😊", parse_mode='HTML', reply_markup=client_mkr.Out)
            await FSMUsers.zajavka_prem.set()
            
# ========================================= Меню кнопки "МОЇ РЕКВІЗИТИ" =====================================================
# Кнопка "ДОДАТИ ПРЕМІУМ"
        elif message.text == 'Додати карту 💳':
            await message.answer('Введіть номер карти', reply_markup=types.ReplyKeyboardRemove())
            await FSMUsers.addedit_kart.set()
        elif message.text == 'Видалити карту ❌':
            await sq.delete_kart(message.from_user.id)
            await message.answer('Карту видалено ✅', reply_markup=client_mkr.add_kart)
        elif message.text == 'Змінити карту ⚒':
            await message.answer('Введіть номер карти', reply_markup=types.ReplyKeyboardRemove())
            await FSMUsers.addedit_kart.set()

# =============================================== СИСТЕМНА ЧАСТИНА ==========================================================

# Перевірка підписки на канал
async def check_sub_channels(channels, user_id):
    channel = await sq.give_ID_sponsor()
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[0], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

# Обработчик калбек
async def callback_cmd(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'out':
        await bot.delete_message(callback.from_user.id, callback.message.message_id)

# Оброботчик вибору тарифа на спонсорку
async def tarif_sponsor(message: types.Message, state: FSMContext):
    async with state.proxy() as users_data:
        if message.text == '🟢 На 3 дні':
            users_data['date'] = '3 дні'
            users_data['price'] = await sq.sp_3days_price()
            await message.answer(f'Відправте ссилку на канал', reply_markup=client_mkr.Out)
            await FSMUsers.url.set()
        elif message.text == '🟢 На 6 днів':
            users_data['date'] = '6 днів'
            users_data['price'] = await sq.sp_6days_price()
            await message.answer(f'Відправте ссилку на канал', reply_markup=client_mkr.Out)
            await FSMUsers.url.set()
        elif message.text == '🟢 На 10 днів':
            users_data['date'] = '10 днів'
            users_data['price'] = await sq.sp_10days_price()
            await message.answer(f'Відправте ссилку на канал', reply_markup=client_mkr.Out)
            await FSMUsers.url.set()
        elif message.text == 'Головне меню ⬅️':
            await message.answer(f"Головне меню ⬅️", reply_markup=client_mkr.ClientMenu)
            await FSMUsers.users.set()
        else:
            await message.answer(f'Я вас не розумію 😕')

# Обработчик ссилки на канал спонсора
async def url(message: types.Message, state: FSMContext):
    async with state.proxy() as users_data:
        url = message.text
        users_data['url'] = url
        if url == '❌ Відмінити ❌':
            await FSMUsers.users.set()
            await message.answer(f'Ви в головному меню', reply_markup=client_mkr.ClientMenu)
        elif url[:8] == 'https://':
            await message.answer(f"Канал з'явиться в списку спонсорів після оплати\nВартість послуги: <b>{users_data['price']}</b> грн\nРеквізити для оплати:\n💳 Privat24: 5457082223804449\n💳 mono: 5375414127416989\n\nЧекаю на скрін оплати 😊", parse_mode='HTML', reply_markup=client_mkr.Out)
            await FSMUsers.zajavka.set()
        elif url[:8] != 'https://':
            await message.answer(f'⚠️ Це не ссилка ⚠️')

# Обробка скріна оплати і відправка заявки на спонсорство
async def zajavka(message: types.Message, state: FSMContext):
    async with state.proxy() as users_data:
        mess_time = datetime.datetime.today().replace(microsecond=0)
        if message.text == '❌ Відмінити ❌':
            await message.answer(f'Ви в головному меню', reply_markup=client_mkr.ClientMenu)   
            await FSMUsers.users.set()
        elif message.photo:
            photo = message.photo[-1].file_id
            await bot.send_photo(ADMIN_ID, photo=photo, caption=(f"Заявка на спонсорство 🔑\nВід: @{await sq.username(message.from_user.id)}\nID: @{message.from_user.id}\nСсилка на канал: {users_data['url']}\nДо сплати: {users_data['price']} грн\nПеріод: {users_data['date']}\nДата: {mess_time}"))
            await message.answer(f"Заявку успішно відправлено ✅\nВаш канал з'явиться у списку спонсорів через кілька хвилин 👌\nЯкщо цього не сталося зверніться до адміністратора 👤", reply_markup=client_mkr.ClientMenu)
            await FSMUsers.users.set()
        else:
            await message.answer(f'⚠️ Це не фото ⚠️')

# Відправка заявки на PREMIUM акаунт
async def zajavka_prem(message: types.Message, state: FSMContext):
    async with state.proxy() as admin_data:
        mess_time = datetime.datetime.today().replace(microsecond=0)
        if message.text == '❌ Відмінити ❌':
            await message.answer(f'Ви в головному меню', client_mkr.ClientMenu)   
            await FSMUsers.users.set()
        elif message.photo:
            photo = message.photo[-1].file_id
            await bot.send_photo(ADMIN_ID, photo=photo, caption=(f'Заявка на PREMIUM акаунт 🔑\nВід: @{await sq.username(message.from_user.id)}\nID: @{message.from_user.id}\nДата: {mess_time}'))
            await message.answer(f"Заявку успішно відправлено ✅\nPREMIUM акаунт буде доступний через кілька хвилин 👌\nЯкщо цього не сталося зверніться до адміністратора 👤", reply_markup=client_mkr.ClientMenu)
            await FSMUsers.users.set()
        else:
            await message.answer(f'⚠️ Це не фото ⚠️')

# Довати або змінити карту юзера  
async def addedit_kart(message: types.Message, state: FSMContext):
    if re.match(r'\d{4}\s\d{4}\s\d{4}\s\d{4}', message.text) and len(message.text) == 19 or re.match(r'\d{16}', message.text) and len(message.text) == 16:        
        kart_id = message.text
        await sq.addedit_kart(message.from_user.id, kart_id)
        await message.answer(f"Карту {message.text} успішно додано ✅", reply_markup=client_mkr.requisitesMENU)
        await FSMUsers.users.set()
    else:
        await message.answer('⚠️ Це не номер карти ⚠️')

# @dp.message_handler(state=FSMUsers.sum)
async def sum(message: types.Message, state: FSMContext):
    mess_time = datetime.datetime.today().replace(microsecond=0)
    if message.text.isdigit():
        user_sum = int(message.text)
        if user_sum <= (await sq.user_balance(message.from_user.id)):
            if await sq.premium_user_exists(message.from_user.id) != 'prem':
                if user_sum >= await sq.minimum_default_out():
                    user_balance = (await sq.user_balance(message.from_user.id))-user_sum
                    await sq.edit_balance(message.from_user.id, user_balance)
                    await bot.send_message(ADMIN_ID, f"Заявка на вивід грошей 💵\nВід: @{await sq.username(message.from_user.id)}\nID користувача: @{message.from_user.id}\nСума: <b>{user_sum}</b> грн\n Дата: {mess_time}", parse_mode='HTML')
                    await message.answer(f'Заявку на вивід успішно відправлено ✅\nГроші будуть на вашій карті через кілька хвилин 👌\nЯкщо гроші не прийшли зверніться до адміністратора 👤', reply_markup=client_mkr.ClientMenu)
                    sum_out = (await sq.user_balance_out(message.from_user.id)+user_sum)
                    await sq.edit_sum_out(message.from_user.id, sum_out)
                    await FSMUsers.users.set()
                elif user_sum < await sq.minimum_default_out():
                    await message.answer(f'⚠️ Мінімальна сума виводу: {await sq.minimum_default_out()} ⚠️')
            elif await sq.premium_user_exists(message.from_user.id) == 'prem':
                if user_sum >= await sq.minimum_prem_out():
                    user_balance = (await sq.user_balance(message.from_user.id))-user_sum
                    await sq.edit_balance(message.from_user.id, user_balance)
                    await bot.send_message(ADMIN_ID, f"Заявка на вивід грошей 💵\nВід: @{await sq.username(message.from_user.id)}\nID користувача: @{message.from_user.id}\nСума: <b>{user_sum}</b> грн\nПреміум: ✅\n Дата: {mess_time}", parse_mode='HTML')
                    await message.answer(f'Заявку на вивід успішно відправлено ✅✅\nГроші будуть на вашій карті через кілька хвилин 👌\nЯкщо гроші не прийшли зверніться до адміністратора 👤', reply_markup=client_mkr.ClientMenu)
                    sum_out = (await sq.user_balance_out(message.from_user.id)+user_sum)
                    await sq.edit_sum_out(message.from_user.id, sum_out)
                    await FSMUsers.users.set()
                elif user_sum < await sq.minimum_prem_out():
                    await message.answer(f'⚠️ Мінімальна сума виводу: {await sq.minimum_prem_out()} ⚠️')
        else:
            await message.answer('⚠️ На вашому рахунку не достатньо коштів ⚠️', reply_markup=client_mkr.Sum_menu)
            FSMUsers.users.set()
    else:
        await message.answer('⚠️ Це не число ⚠️')

# Реєстрація всіх хедлерів
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(btn_client, state=FSMUsers.users)
    dp.register_callback_query_handler(callback_cmd, state=FSMUsers.all_states)
    dp.register_message_handler(tarif_sponsor, state=FSMUsers.Tarif)
    dp.register_message_handler(url, state=FSMUsers.url)
    dp.register_message_handler(zajavka, state=FSMUsers.zajavka, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(zajavka_prem, state=FSMUsers.zajavka_prem, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(addedit_kart, state=FSMUsers.addedit_kart)
    dp.register_message_handler(sum, state=FSMUsers.sum)