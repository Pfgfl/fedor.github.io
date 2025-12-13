import telebot
import sqlite3
bot = telebot.TeleBot('8030061214:AAGCzzCJdNwTxzMjWZu_p098MoYaUApxuMY')

balance = 100000
name = None


@bot.message_handler(commands=['boss'])
def boss(message):
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    information = ''
    for el in users:
        information += f'Имя: {el[1]}, Баланс: {el[2]}\n'

    cur.close()
    conn.close()

    if len(information) > 0:
        bot.send_message(message.chat.id, information)
    else:
        bot.send_message(message.chat.id, 'Пока что клиентов ноль')

@bot.message_handler(commands=['start'])
def client_name(message):
    global balance
    global name
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()
    #cur.execute('DROP TABLE IF EXISTS users') #удаление таблицы перед началом
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), balance INTEGER)')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, я админ, как к вам можно обращаться?')
    bot.register_next_step_handler(message, client_menu)

def client_menu(message):
    name = message.text.strip()
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users(name, balance) VALUES (?, ?)', (name, balance))

    conn.commit()
    cur.close()
    conn.close()

    menu_menu = telebot.types.InlineKeyboardMarkup()
    menu_menu1 = (telebot.types.InlineKeyboardButton('Поставить ставочку', callback_data='rate'))
    menu_menu.row(menu_menu1)
    bot.send_message(message.chat.id, f'{name}, поставь ставку на кастомку дока2, напиши /balance чтобы увидеть свой баланс', reply_markup=menu_menu)


@bot.message_handler(commands=['balance'])
def user_balance(message):
    global balance
    bot.send_message(message.chat.id,f'Твой баланс: {balance}₽')

@bot.callback_query_handler(func=lambda call: call.data in ['rate'])
def vibor(callback):
    kastom_menu = telebot.types.InlineKeyboardMarkup()
    kastom_menu1 = (telebot.types.InlineKeyboardButton('1x6', callback_data='cast1'))
    kastom_menu2 = (telebot.types.InlineKeyboardButton('overthrow', callback_data='cast2'))
    kastom_menu.row(kastom_menu1, kastom_menu2)
    bot.send_message(callback.message.chat.id, 'Выбери режим кастомочки:', reply_markup=kastom_menu)



@bot.callback_query_handler(func=lambda call: call.data in ['cast1', 'cast2'])
def callback(callback):
    global balance
    if callback.data == 'cast1':
        button_menu = telebot.types.InlineKeyboardMarkup()
        button_menu1 = (telebot.types.InlineKeyboardButton('Sashin-Yashin(Негид)', callback_data='negit'))
        button_menu2 = (telebot.types.InlineKeyboardButton('Азер брат(димсик про в 1х6)', callback_data='dima'))
        button_menu3 = (telebot.types.InlineKeyboardButton('Тимоха(админ дока2)', callback_data='tima'))
        button_menu4 = (telebot.types.InlineKeyboardButton('федор арбалет(федос)', callback_data='fedos'))
        button_menu5 = (telebot.types.InlineKeyboardButton('Тахенчик(где бабка????)', callback_data='taxen'))
        button_menu6 = (telebot.types.InlineKeyboardButton('makenagagreatagain(ярик)', callback_data='iarik'))
        button_menu.row(button_menu1, button_menu2)  # Кнопки 1 и 2 в одной строке
        button_menu.row(button_menu4)  # Кнопка 3 в отдельной строке
        button_menu.row(button_menu3, button_menu5)
        button_menu.row(button_menu6)
        bot.send_message(callback.message.chat.id, 'выбери кто победит:', reply_markup=button_menu)

    elif callback.data == 'cast2':
        button_menu = telebot.types.InlineKeyboardMarkup()
        button_menu1 = (telebot.types.InlineKeyboardButton('Sashin-Yashin(Негид)', callback_data='negit'))
        button_menu2 = (telebot.types.InlineKeyboardButton('Азер брат(димсик про в 1х6)', callback_data='dima'))
        button_menu3 = (telebot.types.InlineKeyboardButton('Тимоха(админ дока2)', callback_data='tima'))
        button_menu4 = (telebot.types.InlineKeyboardButton('федор арбалет(федос)', callback_data='fedos'))
        button_menu5 = (telebot.types.InlineKeyboardButton('Тахенчик(где бабка????)', callback_data='taxen'))
        button_menu6 = (telebot.types.InlineKeyboardButton('makenagagreatagain(ярик)', callback_data='iarik'))
        button_menu.row(button_menu1, button_menu2)  # Кнопки 1 и 2 в одной строке
        button_menu.row(button_menu4)  # Кнопка 3 в отдельной строке
        button_menu.row(button_menu3, button_menu5)
        button_menu.row(button_menu6)
        bot.send_message(callback.message.chat.id, 'выбери кто победит:', reply_markup=button_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['negit', 'dima', 'tima', 'fedos', 'taxen', 'iarik'])
def rate(callback):
    rate_menu = telebot.types.InlineKeyboardMarkup()
    rate_menu1 = (telebot.types.InlineKeyboardButton('10.000₽', callback_data='10'))
    rate_menu2 = (telebot.types.InlineKeyboardButton('25.000₽', callback_data='25'))
    rate_menu3 = (telebot.types.InlineKeyboardButton('50.000₽', callback_data='50'))
    rate_menu4 = (telebot.types.InlineKeyboardButton('75.000₽', callback_data='75'))
    rate_menu5 = (telebot.types.InlineKeyboardButton('100.000₽', callback_data='100'))
    rate_menu.row(rate_menu1, rate_menu2)  # Кнопки 1 и 2 в одной строке
    rate_menu.row(rate_menu4)  # Кнопка 3 в отдельной строке
    rate_menu.row(rate_menu3, rate_menu5)
    bot.send_message(callback.message.chat.id, 'выбери сколько хочешь залить:', reply_markup=rate_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['10', '25', '50', '75', '100'])
def callback(callback):
    global balance
    if callback.data == '10':
        if balance - 10000<0:
            bot.send_message(callback.message.chat.id,f'Недостаточно средств для ставки в 10.000₽. Ваш баланс: {balance}₽')
        else:
            balance -= 10000
            bot.send_message(callback.message.chat.id, f'Вы поставили 10.000₽, ваш баланс {balance}₽')
            conn = sqlite3.connect('clients.sql')
            cur = conn.cursor()

            cur.execute('UPDATE users SET balance = ? WHERE name = ?', (balance, name))

            conn.commit()
            cur.close()
            conn.close()
    elif callback.data == '25':
        if balance - 25000<0:
            bot.send_message(callback.message.chat.id,f'Недостаточно средств для ставки в 25.000₽. Ваш баланс: {balance}₽')
        else:
            balance -= 25000
            bot.send_message(callback.message.chat.id, f'Вы поставили 25.000₽, ваш баланс {balance}₽')
            conn = sqlite3.connect('clients.sql')
            cur = conn.cursor()

            cur.execute('UPDATE users SET balance = ? WHERE name = ?', (balance, name))

            conn.commit()
            cur.close()
            conn.close()
    elif callback.data == '50':
        if balance - 50000<0:
            bot.send_message(callback.message.chat.id,f'Недостаточно средств для ставки в 50.000₽. Ваш баланс: {balance}₽')
        else:
            balance -= 50000
            bot.send_message(callback.message.chat.id, f'Вы поставили 50.000₽, ваш баланс {balance}₽')
            conn = sqlite3.connect('clients.sql')
            cur = conn.cursor()

            cur.execute('UPDATE users SET balance = ? WHERE name = ?', (balance, name))

            conn.commit()
            cur.close()
            conn.close()
    elif callback.data == '75':
        if balance - 75000<0:
            bot.send_message(callback.message.chat.id,f'Недостаточно средств для ставки в 75.000₽. Ваш баланс: {balance}₽')
        else:
            balance -= 75000
            bot.send_message(callback.message.chat.id, f'Вы поставили 75.000₽, ваш баланс {balance}₽')
            conn = sqlite3.connect('clients.sql')
            cur = conn.cursor()

            cur.execute('UPDATE users SET balance = ? WHERE name = ?', (balance, name))

            conn.commit()
            cur.close()
            conn.close()
    elif callback.data == '100':
        if balance - 100000<0:
            bot.send_message(callback.message.chat.id,f'Недостаточно средств для ставки в 100.000₽. Ваш баланс: {balance}₽')
        else:
            balance -= 100000
            bot.send_message(callback.message.chat.id, f'Вы поставили 100.000₽, ваш баланс {balance}₽')
            conn = sqlite3.connect('clients.sql')
            cur = conn.cursor()

            cur.execute('UPDATE users SET balance = ? WHERE name = ?', (balance, name))

            conn.commit()
            cur.close()
            conn.close()

    menu_menu = telebot.types.InlineKeyboardMarkup()
    menu_menu1 = (telebot.types.InlineKeyboardButton('Поставить ставочку', callback_data='rate'))
    menu_menu.row(menu_menu1)
    bot.send_message(callback.message.chat.id, f'{name}, поставь ставку на кастомку дока2, напиши /balance чтобы увидеть свой баланс',reply_markup=menu_menu)

bot.polling(none_stop=True)






