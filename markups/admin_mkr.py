from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton  

# Головне меню
AdminMenu = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
item1 = KeyboardButton('Пошук по ID 🔑')
item2 = KeyboardButton('Змінити ціни 💵')
item4 = KeyboardButton('Кількість користувачів 📊')
item5 = KeyboardButton('Додати спонсора 👤')
item6 = KeyboardButton('Оновити БД 🔄')
AdminMenu.row(item1, item2).add(item4).add(item5).add(item6)

# Меню кнопки "ПОШУК ПО ID"
UpdateUsers = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
item1 = KeyboardButton('Інформація 📚')
item2 = KeyboardButton('Видати PREMIUM ⭐️')
item3 = KeyboardButton('Видалити PREMIUM ❌')
item4 = KeyboardButton('Написати ✉️')
item5 = KeyboardButton('Меню ⬅️')
UpdateUsers.add(item1,item4).add(item2).add(item3).add(item5)

# Меню кнопки "ЗМІНИТИ ЦІНИ"
EditPrice = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
item1 = KeyboardButton(text='📌 Ціна за рефа', callback_data='default_price_ref')
item2 = KeyboardButton(text='📌 PREMIUM за рефа', callback_data='premium_price_ref')
item3 = KeyboardButton(text='📌 Ціна спонсорки', callback_data='price3')
item4 = KeyboardButton(text='📌 Ціна PREMIUM', callback_data='premium_ak_price')
item5 = KeyboardButton(text='📌 Звичайний вивід', callback_data='minimum_default_out')
item6 = KeyboardButton(text='📌 Вивід PREMIUM', callback_data='minimum_prem_out')
item7 = KeyboardButton('Меню ⬅️')
EditPrice.add(item1, item2, item3, item4, item5, item6, item7)

# Клавіатура спосорки
Sponsor_day = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('📌 Ціна на 3 дні')
item2 = KeyboardButton('📌 Ціна на 6 днів')
item3 = KeyboardButton('📌 Ціна на 10 днів')
item4 = KeyboardButton('Меню ⬅️')
Sponsor_day.add(item1, item2, item3, item4)

# Кнопка ВІДМІНИТИ ІНЛАЙН
Out_in = InlineKeyboardMarkup()
item1 =InlineKeyboardButton(text='❌ Закрити ❌', callback_data='out')
Out_in.add(item1)

# Кнопка СПОНСОВАНО
spon = ReplyKeyboardMarkup(resize_keyboard = True)
item1 = KeyboardButton('Спонсовано 👑')
spon.add(item1)

# Клавіатура спосорки
Sp_data_del = ReplyKeyboardMarkup(resize_keyboard = True, row_width=3)
item1 = KeyboardButton('3')
item2 = KeyboardButton('6')
item3 = KeyboardButton('10')
Sp_data_del.add(item1, item2, item3)