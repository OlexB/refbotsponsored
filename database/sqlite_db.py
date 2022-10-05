import psycopg2 as sq
from tkinter import NO
from create_refbot import bot

# ================================================== ЗАПРОСИ БД ДЛЯ КОРИСТУВАЧІВ ======================================================
# Підключення до БД
def sql_start():
    global base, cur
    base = sq.connect('database/database.db')
    cur = base.cursor()
    if base:
        print('БД ПОДКЛЮЧЕНА')
    base.commit()
# Перевірка чи зареєстрований користувач
async def user_exists(user_id):
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if user == None:
        return False
    else:
        return True
# Реєстрація користувача з реф ID і без реф ID
async def add_user(user_id, username, data, referer_id=None):
    if referer_id != None:
        cur.execute("INSERT INTO users (data_reg, user_id, username, referer_id) VALUES (?, ?, ?, ?)", (data, user_id, username, referer_id,))
    elif referer_id == None:
        cur.execute("INSERT INTO users (data_reg, user_id, username) VALUES (?, ?,?)", (data, user_id, username,))
    else:
        pass
    base.commit()
# Перевірка чи є у користувача PREMIUM акаунт
async def premium_user_exists(user_id):
    return cur.execute("SELECT user_premium_id FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]
# Перевірка чи є у користувача PREMIUM акаунт ДЛЯ КНОПКИ "ІНФО"
async def premium_user_ex(user_id):
    prem =  cur.execute("SELECT user_premium_id FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]
    if prem != None:
        return '✅'
    else:
        return '❌'
# Вивід кількості рефералів 
async def count_referal(user_id):
    return cur.execute("SELECT COUNT (id) FROM users WHERE referer_id == '{key}'".format(key=user_id)).fetchone()[0]
# Вивід кількості рефералів 
async def count_users_referal(referer_id):
    return cur.execute("SELECT COUNT (id) FROM users WHERE referer_id == '{key}'".format(key=referer_id)).fetchone()[0]
# Вивід дати реєстрації в боті
async def data_reg(user_id):
    return cur.execute("SELECT data_reg FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]
# Нарахування балансу рефереру за реєстрацію нового користувача
async def edit_user_balance(user_balance, referer_id):
    cur.execute("UPDATE users SET user_balance = '{}' WHERE user_id == '{key}'".format(user_balance, key=referer_id))
    base.commit()
# Вивід всіх полів таблиці "ЦІНИ"
# Ціна спонсорки на 3 дні
async def sp_3days_price():
    return cur.execute("SELECT * FROM prices").fetchone()[3]
# Ціна спонсорки на 6 днів
async def sp_6days_price():
    return cur.execute("SELECT * FROM prices").fetchone()[4]
# Ціна спонсорки на 10 днів
async def sp_10days_price():
    return cur.execute("SELECT * FROM prices").fetchone()[5]
# Ціна за реферала на стоковому акаунті
async def default_price_ref():
    return cur.execute("SELECT * FROM prices").fetchone()[0]
# Ціна за реферала на PREMIUM акаунті
async def premium_price_ref():
    return cur.execute("SELECT * FROM prices").fetchone()[1]
# Ціна  мінімального виводу для звичайного акаунту
async def minimum_default_out():
    return cur.execute("SELECT * FROM prices").fetchone()[6]
# Ціна за мінімального виводу для PREMIUM акаунту
async def minimum_prem_out():
    return cur.execute("SELECT * FROM prices").fetchone()[7]
# Ціна PREMIUM акаунту
async def premium_ak_price():
    return cur.execute("SELECT * FROM prices").fetchone()[2]
# Операції з спонсорами
# Вивід каналів для клавіатури
async def give_sponsor():
    return cur.execute("SELECT name, sponsor_url FROM sponsor").fetchall()
# Вивід ID каналу для перевірки підписки
async def give_ID_sponsor():
    return cur.execute("SELECT sponsor_id FROM sponsor").fetchall()
# Операції з користуваче
# Вивід username користувача
async def username(user_id):
    return cur.execute("SELECT username FROM users WHERE user_id = '{}'".format(user_id)).fetchone()[0]
# Вивід балансу користувача
async def user_balance(user_id):
    balance = cur.execute("SELECT user_balance FROM users WHERE user_id = '{}'".format(user_id)).fetchone()[0]
    if balance == None:
        return 0
    else:
        return balance
# Змінити баланс користувача
async def edit_balance(user_balance, user_id):
    cur.execute("UPDATE users SET user_balance = '{}' WHERE user_id == '{key}'".format(user_balance, key=user_id))
    base.commit()
# Операції з реквізитами
# Перевірка наявності карти користувача 
async def user_kart_exists(user_id):
    kart = cur.execute("SELECT user_kart_id FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()[0]
    if kart == None:
        return False
    else:
        return True
# Вивід номера карти користувача
async def give_user_kart(user_id):
    return cur.execute("SELECT user_kart_id FROM users WHERE user_id = '{}'".format(user_id)).fetchone()[0]
# Вивід суми виводу користувача
async def user_balance_out(user_id):
    sum_out =  cur.execute("SELECT user_sum_out FROM users WHERE user_id = '{}'".format(user_id)).fetchone()[0]
    if sum_out == None:
        return 0
    else:
        return sum_out
# Змына суми виводу користувача
async def edit_sum_out(user_id, sum_out):
    cur.execute("UPDATE users SET user_sum_out = '{}' WHERE user_id == '{key}'".format(sum_out, key=user_id))
    base.commit()
# Вивід номера карти користувача ДЛЯ КНОПКИ "ІНФО"
async def give_kart_inf(user_id):
    kart = cur.execute("SELECT user_kart_id FROM users WHERE user_id = '{}'".format(user_id)).fetchone()[0]
    if kart != None:
        return kart
    else:
        return '❌'
# Добавити або змінити карту користувача
async def addedit_kart(user_id, kart_id):
    cur.execute("UPDATE users SET user_kart_id = '{}' WHERE user_id == '{}'".format(kart_id, user_id))
    base.commit()
    print('Карту додано')
# Видалити карту користувача
async def delete_kart(user_id):
    cur.execute("UPDATE users SET user_kart_id = NULL WHERE user_id == '{key}'".format(key=user_id))
    base.commit()

# ================================================== ЗАПРОСИ БД ДЛЯ АДМІНІСТРАТОРА =====================================================
# Вивід шуканого ID
async def user_search_id(search_id):
    return cur.execute("SELECT user_id FROM users WHERE user_id == '{key}'".format(key=search_id)).fetchone()[0]
# Вивід USERNAME шуканого користувача
async def give_username(search_id):
    return cur.execute("SELECT username FROM users WHERE user_id == '{key}'".format(key=search_id)).fetchone()[0]
# Видати преміум
async def get_premium(Premiu_id, users_id):
    cur.execute("UPDATE users SET user_premium_id = '{}' WHERE user_id ='{}'".format(Premiu_id, users_id))
    base.commit()
# Додати спонсора
async def aad_channel(data_delete, chanel_name, channel_id, channel_url):
    cur.execute("INSERT INTO sponsor ('data_delete', 'name', 'sponsor_id', 'sponsor_url') VALUES (?, ?, ?, ?)", (data_delete, chanel_name, channel_id, channel_url,))
    base.commit()
# Видалити преміум
async def delete_PREMIUM(users_id):
    cur.execute("UPDATE users SET user_premium_id = NULL WHERE user_id == '{}'".format(users_id))
    base.commit()

# ====================== Вивід кількості користувачів ======================
# Всього
async def count_users():
    return cur.execute("SELECT COUNT (id) from users").fetchone()[0]
# З PREMIUM
async def count_users_prem():
    return cur.execute("SELECT COUNT (id) from users WHERE user_premium_id == 'prem'").fetchone()[0]

# ============================ Запроси на зміну цін ========================
# Зміна ціни за рефа на спотовому акаунті
async def ed_default_price_ref(message):
    cur.execute("UPDATE prices SET default_price_ref = '{}'".format(message))
    base.commit()
# Зміна ціни за рефа на PREMIUM акануті
async def ed_premium_price_ref(message):
    cur.execute("UPDATE prices SET premium_price_ref = '{}'".format(message))
    base.commit()
# Зміна ціни на PREMIUM акануті
async def ed_premium_ak_price(message):
    cur.execute("UPDATE prices SET premium_ak_price = '{}'".format(message))
    base.commit()
# Зміна мінімального виводу на стоковому акаунті
async def ed_minimum_default_out(message):
    cur.execute("UPDATE prices SET minimum_default_out = '{}'".format(message))
    base.commit()
# Зміна мінімального виводу на PREMIUM акаунті
async def ed_minimum_prem_out(message):
    cur.execute("UPDATE prices SET minimum_prem_out = '{}'".format(message))
    base.commit()
# Ціни на спонсорку
# НА 3 ДНІ
async def ed_sp_3days_price(message):
    cur.execute("UPDATE prices SET sp_3days_price = '{}'".format(message))
    base.commit()
# НА 6 ДНів
async def ed_sp_6days_price(message):
    cur.execute("UPDATE prices SET sp_6days_price = '{}'".format(message))
    base.commit()
# НА 10 ДНів
async def ed_sp_10days_price(message):
    cur.execute("UPDATE prices SET sp_10days_price = '{}'".format(message))
    base.commit()