import telebot
import sqlite3
bot = telebot.TeleBot('7893176190:AAE15dw-OaMvq-LAoAXedfDosveUcbRaU1w')

classescl = 0
name = None
vk = 'https://vk.com/id894655226'
tg = 'https://t.me/+GBEVAynuQ5xlNTEy'
@bot.message_handler(commands=['clients'])
def boss(message):
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    information = ''
    for el in users:
        information += f'Имя: {el[1]}, Номер: {el[2]}, Отзыв: {el[3]}, Кол-во посещ-ых занятий: {el[4]}\n'

    cur.close()
    conn.close()

    if len(information) > 0:
        bot.send_message(message.chat.id, information)
    else:
        bot.send_message(message.chat.id, 'Пока что клиентов ноль :(')

@bot.message_handler(commands=['start'])
def client(message):
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()
    #cur.execute('DROP TABLE IF EXISTS users') #удаление таблицы перед началом
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), number VARCHAR(50), review VARCHAR(500), classes VARCHAR(100))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Здравствуйте, я Павел, как к вам можно обращаться?')
    bot.register_next_step_handler(message, namecl)

def namecl(message):
    global name
    global client_id
    global classescl
    classescl = 0
    name = message.text.strip()
    if name.lower() == 'босс':
        bot.send_message(message.chat.id, 'Приветствую босс вот команда для вас, если вы хотите увидеть всех ваших клиентов: /clients')
    else:
        conn = sqlite3.connect('clients.sql')
        cur = conn.cursor()

        cur.execute('INSERT INTO users(name, classes) VALUES (?, ?)', (name, classescl))
        client_id = cur.lastrowid

        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, f'{name}, для того чтобы я мог связаться с вами, пожалуйста введите свой номер телефона')
        bot.register_next_step_handler(message, number)

def number(message):
    global number
    number = message.text.strip()
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET number = ? WHERE id = ?', (number, client_id))

    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'спасибо!')
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = (telebot.types.InlineKeyboardButton('Информация обо мне', callback_data='info'))
    button_menu2 = (telebot.types.InlineKeyboardButton('Мои соц.сети', callback_data='seti'))
    button_menu3 = (telebot.types.InlineKeyboardButton('Запись на занятие', callback_data='help'))
    button_menu4 = (telebot.types.InlineKeyboardButton('Интересные факты о собаках', callback_data='facts'))
    button_menu5 = (telebot.types.InlineKeyboardButton('Оставить отзыв', callback_data='review'))
    button_menu6 = (telebot.types.InlineKeyboardButton('У меня было занятие. 1 занятие-1 нажатие', callback_data='classes'))
    button_menu.row(button_menu1, button_menu2)  # Кнопки 1 и 2 в одной строке
    button_menu.row(button_menu4)  # Кнопка 3 в отдельной строке
    button_menu.row(button_menu3, button_menu5)
    button_menu.row(button_menu6)
    bot.send_message(message.chat.id, 'Вот функции нашего бота, выбирайте то что вам нужно', reply_markup=button_menu)
@bot.callback_query_handler(func=lambda call: call.data in ['info', 'seti', 'help', 'facts', 'review', 'classes'])
def callback(callback):
    global classescl
    if callback.data == 'info':
        bot.send_message(callback.message.chat.id, 'Пример: Я Павел. Стаж дрессировки собак 25 лет. Имею 3 высших образования. В своей жизни было 5 собак')
    elif callback.data == 'seti':
        bot.send_message(callback.message.chat.id,f'Вот моя страничка в ВК: {vk}\n А вот наш чат в ТГ по дрессировке: {tg}')
    elif callback.data == 'help':
        bot.send_message(callback.message.chat.id, f'Вы хотите запсиаться на занятие по дрессировке. Проверьте это ваш номер телефона {number}?(Пример ответа:да)')
        bot.register_next_step_handler(callback.message, provcl)
    elif callback.data == 'review':
        bot.send_message(callback.message.chat.id,'Напишите свой отзыв о занятии, нам очень важно ваше мнение')
        bot.register_next_step_handler(callback.message, handle_review)
    elif callback.data == 'facts':
        button_dogs = telebot.types.InlineKeyboardMarkup()
        button_dogs1 = telebot.types.InlineKeyboardButton('Хаски', callback_data='haski')
        button_dogs2 = telebot.types.InlineKeyboardButton('Бигль', callback_data='bigl')
        button_dogs3 = telebot.types.InlineKeyboardButton('Пудель', callback_data='pudel')
        button_dogs.add(button_dogs1, button_dogs2, button_dogs3)
        bot.send_message(callback.message.chat.id, 'Выберите про какую пораду собак вы хотите узнать больше.', reply_markup=button_dogs)
    elif callback.data == 'classes':
        classescl += 1
        bot.send_message(callback.message.chat.id, f'Мы рады, что у нас с вами прошло занятие. Сейчас проведённых занятий: {classescl}\n Поделитесь своими впечетленияниями о занятии, по кнопке "Оставить отзыв"')
        conn = sqlite3.connect('clients.sql')
        cur = conn.cursor()

        cur.execute('UPDATE users SET classes = ? WHERE id = ?', (classescl, client_id))

        conn.commit()
        cur.close()
        conn.close()

@bot.callback_query_handler(func=lambda call: call.data in ['haski', 'bigl', 'pudel'])
def calldogs(callback):
    if callback.data == 'haski':
        bot.send_message(callback.message.chat.id, 'Вот информация о [Хаски](https://www.proplan.ru/dog/breeds/haski/)', parse_mode='Markdown')
    elif callback.data == 'bigl':
        bot.send_message(callback.message.chat.id, 'Вот информация о [Бигле](https://www.proplan.ru/dog/breeds/bigl/)', parse_mode='Markdown')
    elif callback.data == 'pudel':
        bot.send_message(callback.message.chat.id, 'Вот информация о [Пуделе](https://www.proplan.ru/dog/breeds/pudel/)', parse_mode='Markdown')

def handle_review(message):
    reviewcl = message.text.strip()
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET review = ? WHERE id = ?', (reviewcl, client_id))

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Спасибо, за ваше мнение, мы учтем каждое пожелание:)')
def provcl(message):
    if message.text.lower() == 'да':
        button_menu = telebot.types.InlineKeyboardMarkup()
        button_menu1 = (telebot.types.InlineKeyboardButton('Информация обо мне', callback_data='info'))
        button_menu2 = (telebot.types.InlineKeyboardButton('Мои соц.сети', callback_data='seti'))
        button_menu3 = (telebot.types.InlineKeyboardButton('Запись на занятие', callback_data='help'))
        button_menu4 = (telebot.types.InlineKeyboardButton('Интересные факты о собаках', callback_data='facts'))
        button_menu5 = (telebot.types.InlineKeyboardButton('Оставить отзыв', callback_data='review'))
        button_menu6 = (telebot.types.InlineKeyboardButton('У меня было занятие\nНажмите эту кнопку, если у вас прошло занятие,\n Одно занятие-одно нажатие этой кнопки', callback_data='classes'))
        button_menu.row(button_menu1, button_menu2)  # Кнопки 1 и 2 в одной строке
        button_menu.row(button_menu4)  # Кнопка 3 в отдельной строке
        button_menu.row(button_menu3, button_menu5)
        button_menu.row(button_menu6)
        bot.send_message(message.chat.id, f'Хорошо, мы записали вас на занятие.\n Сейчас посещенных занятий:  {classescl}.\n Свяжусь с вами в ближайшее время для обсуждения подробностей, а пока что можете узнать интересную вам информацию', reply_markup=button_menu)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id,'Пожалуйста укажите свой действительный номер телефона')
        bot.register_next_step_handler(message, handle_number)
def handle_number(message):
    global number
    number = message.text.strip()
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET number = ? WHERE id = ?", (number, number))

    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'спасибо!')
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = (telebot.types.InlineKeyboardButton('Информация обо мне', callback_data='info'))
    button_menu2 = (telebot.types.InlineKeyboardButton('Мои соц.сети', callback_data='seti'))
    button_menu3 = (telebot.types.InlineKeyboardButton('Запись на занятие', callback_data='help'))
    button_menu4 = (telebot.types.InlineKeyboardButton('Интересные факты о собаках', callback_data='facts'))
    button_menu5 = (telebot.types.InlineKeyboardButton('Оставить отзыв', callback_data='review'))
    button_menu6 = (telebot.types.InlineKeyboardButton('У меня было занятие\nНажмите эту кнопку, если у вас прошло занятие,\n Одно занятие-одно нажатие этой кнопки', callback_data='classes'))
    button_menu.row(button_menu1, button_menu2)  # Кнопки 1 и 2 в одной строке
    button_menu.row(button_menu4)  # Кнопка 3 в отдельной строке
    button_menu.row(button_menu3, button_menu5)
    button_menu.row(button_menu6)
    bot.send_message(message.chat.id,f'Хорошо, мы записали вас на занятие.\n Сейчас посещенных занятий {classescl}.\n Свяжусь с вами в ближайшее время для обсуждения подробностей, а пока что можете узнать интересную вам информацию', reply_markup=button_menu)





bot.polling(none_stop=True)
