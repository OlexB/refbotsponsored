from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton  

# Головне меню
ClientMenu = ReplyKeyboardMarkup(resize_keyboard = True)
item1 = KeyboardButton('Мій кабінет 👤')
item2 = KeyboardButton('Адміністратор ⭐️')
item3 = KeyboardButton('Відгуки 🗣')
item4 = KeyboardButton('Наші спонсори 📌')
item5 = KeyboardButton('Стати спонсором 🔑')
item6 = KeyboardButton('PREMIUM 💎')
ClientMenu.add(item1).row(item2, item3).row(item4, item5).add(item6)

# Меню кнопки "МІЙ КАБІНЕТ"
KabinetMarkups = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
item2 = KeyboardButton('Інформація 📖')
item3 = KeyboardButton('Мої реквізити 💳')
item4 = KeyboardButton('Вивести гроші 💸')
item5 = KeyboardButton('Моя ссилка 🔗')
item6 = KeyboardButton('Головне меню ⬅️')
KabinetMarkups.add(item2, item3, item4, item5, item6)

# Інлайн клавіатура на кнопку "АДМІНІСТРАТОР"
Admin = InlineKeyboardMarkup(resize_keyboard = True)
item1 = InlineKeyboardButton('⭐️ Адміністратор ⭐️', url='https://t.me/sellswbot')
item2 =InlineKeyboardButton(text='❌ Закрити ❌', callback_data='out')
Admin.add(item1, item2)

# Інлайн клавіатура на кнопку "ВІДГУКИ"
Reviews = InlineKeyboardMarkup(resize_keyboard = True)
item1 = InlineKeyboardButton(text='💎 ВІДГУКИ 💎', url='https://t.me/widhuk')
item2 =InlineKeyboardButton(text='❌ Закрити ❌', callback_data='out')
Reviews.add(item1, item2)

# Інлайн клавіатура з кнопками спонсорів
def sponsor_markups(sponsor):
    markup = InlineKeyboardMarkup(row_width=1)
    for i in sponsor: 
        markup.add(InlineKeyboardButton(i[0], url=i[1]))
    markup.add(InlineKeyboardButton(text='❌ Закрити ❌', callback_data='out'))
    return markup

# Меню кнопки "СТАТИ СПОНСОРОМ"
next_sponsor = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('Продовжити ✅')
item2 = KeyboardButton('Головне меню ⬅️')
next_sponsor.add(item1, item2)

# Меню кнопки "ПРОДОВЖИТИ" ТАРИФИ
Tarif = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('🟢 На 3 дні')
item2 = KeyboardButton('🟢 На 6 днів')
item3 = KeyboardButton('🟢 На 10 днів')
item4 = KeyboardButton('Головне меню ⬅️')
Tarif.row(item1, item2).add(item3).add(item4)

# Кнопка ВІДМІНИТИ
Out = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('❌ Відмінити ❌')
Out.add(item1)


# Кнопка ВІДМІНИТИ ІНЛАЙН
Out_in = InlineKeyboardMarkup()
item1 =InlineKeyboardButton(text='❌ Закрити ❌', callback_data='out')
Out_in.add(item1)

# Меню кнопки "PREMIUM"
PremMune = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('Купити преміум 💎')
item2 = KeyboardButton('Головне меню ⬅️')
PremMune.add(item1, item2)

# Меню кнопки "МОЇ РЕКВІЗИТИ" коли карта додана
requisitesMENU = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
item1 = KeyboardButton('Змінити карту ⚒')
item2 = KeyboardButton('Видалити карту ❌')
item3 = KeyboardButton('Головне меню ⬅️')
requisitesMENU.add(item1, item2, item3)

# Меню кнопки "МОЇ РЕКВІЗИТИ" коли карта НЕ додана
add_kart = ReplyKeyboardMarkup(resize_keyboard = True)
item1 = KeyboardButton('Додати карту 💳')
item2 = KeyboardButton('Головне меню ⬅️')
add_kart.add(item1, item2)

# Меню стану на виводі
Sum_menu = ReplyKeyboardMarkup(resize_keyboard = True)
item1 = KeyboardButton('Ввести іншу суму')
item2 = KeyboardButton('Головне меню ⬅️')
Sum_menu.add(item1, item2)