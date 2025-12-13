import telebot
import sqlite3
ch=0
name = ''
user_id = ''
bot = telebot.TeleBot('8363572127:AAGr9q6mpldhspA_Xq9B7svMxAVRk8hqYN0')

@bot.message_handler(commands=['start'])
def client(message):
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()
    #cur.execute('DROP TABLE IF EXISTS users') #удаление таблицы перед началом
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Здравствуйте, как я могу к вам обращаться?')
    bot.register_next_step_handler(message, namecl)


def namecl(message):
    global name
    global user_id
    global ch
    ch = 0
    user_id = message.from_user.id  # Получаем ID пользователя
    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()
    name = message.text.strip()

    cur.execute('INSERT INTO users(id, name, score) VALUES (?, ?, ?)', (user_id, name, ch))

    conn.commit()
    cur.close()
    conn.close()

    victorina1(message)

def victorina1(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('В Москве', callback_data='1')
    button_menu2 = telebot.types.InlineKeyboardButton('В Санкт-Петербурге', callback_data='2')
    button_menu3 = telebot.types.InlineKeyboardButton('В Самаре', callback_data='3')
    button_menu4 = telebot.types.InlineKeyboardButton('В Воронеже', callback_data='4')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id, 'Вопрос №1) В каком городе в 1909 году был открыт первый в России питомник полицейских сыскных собак, на базе которого также была создана школа дрессировки?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4'])
def handle_first_question(call):
    global ch
    response_text = ""

    if call.data == '1':
        response_text = '*Вы не правы!* К основанию первого питомника сыскных собак в Санкт-Петербурге 21 июня 1909 года и приурочен праздник День кинолога.'
    elif call.data == '2':
        response_text = '*Вы правы!* К основанию первого питомника сыскных собак в Санкт-Петербурге 21 июня 1909 года и приурочен праздник День кинолога.'
        ch += 1
    elif call.data == '3':
        response_text = '*Вы не правы!* К основанию первого питомника сыскных собак в Санкт-Петербурге 21 июня 1909 года и приурочен праздник День кинолога.'
    elif call.data == '4':
        response_text = '*Вы не правы!* К основанию первого питомника сыскных собак в Санкт-Петербурге 21 июня 1909 года и приурочен праздник День кинолога.'
    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌В Москве', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('✅В Санкт-Петербурге', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌В Самаре', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌В Воронеже', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina2(call.message)


def victorina2(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('32', callback_data='11')
    button_menu2 = telebot.types.InlineKeyboardButton('36', callback_data='22')
    button_menu3 = telebot.types.InlineKeyboardButton('42', callback_data='33')
    button_menu4 = telebot.types.InlineKeyboardButton('48', callback_data='44')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №2) Сколько зубов у собаки?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['11', '22', '33', '44'])
def handle_second_question(call):
    global ch
    response_text = ""
    if call.data == '11':
        response_text = '*Вы не правы!* В верхней челюсти расположено 20 зубов и в нижней 22.'
    elif call.data == '22':
        response_text = '*Вы не правы!* В верхней челюсти расположено 20 зубов и в нижней 22.'
    elif call.data == '33':
        response_text = '*Вы правы!* В верхней челюсти расположено 20 зубов и в нижней 22.'
        ch += 1
    elif call.data == '44':
        response_text = '*Вы не правы!* В верхней челюсти расположено 20 зубов и в нижней 22.'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌32', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌36', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('✅42', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌48', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina3(call.message)

def victorina3(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Собака Качалова', callback_data='111')
    button_menu2 = telebot.types.InlineKeyboardButton('Собака Баскервилей', callback_data='222')
    button_menu3 = telebot.types.InlineKeyboardButton('Собака Павлова', callback_data='333')
    button_menu4 = telebot.types.InlineKeyboardButton('Собака Менделеева', callback_data='444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id, 'Вопрос №3) Как называют собаку – собирательный образ всех собак, положивших свои жизни на алтарь науки?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['111', '222', '333', '444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '111':
        response_text = '*Вы не правы!* Собака Павлова. По проекту великого русского физиолога И. Павлова в Санкт-Петербурге в саду Института физиологии воздвигнут памятник собакам, без помощи которых были бы невозможны многие открытия в медицине.'
    elif call.data == '222':
        response_text = '*Вы не правы!* Собака Павлова. По проекту великого русского физиолога И. Павлова в Санкт-Петербурге в саду Института физиологии воздвигнут памятник собакам, без помощи которых были бы невозможны многие открытия в медицине.'
    elif call.data == '333':
        response_text = '*Вы правы!* Собака Павлова. По проекту великого русского физиолога И. Павлова в Санкт-Петербурге в саду Института физиологии воздвигнут памятник собакам, без помощи которых были бы невозможны многие открытия в медицине.'
        ch += 1
    elif call.data == '444':
        response_text = '*Вы не правы!* Собака Павлова. По проекту великого русского физиолога И. Павлова в Санкт-Петербурге в саду Института физиологии воздвигнут памятник собакам, без помощи которых были бы невозможны многие открытия в медицине.'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Собака Качалова', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Собака Баскервилей', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('✅Собака Павлова', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌Собака Менделеева', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina4(call.message)

def victorina4(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Мушка', callback_data='1111')
    button_menu2 = telebot.types.InlineKeyboardButton('Стрелка', callback_data='2222')
    button_menu3 = telebot.types.InlineKeyboardButton('Белка', callback_data='3333')
    button_menu4 = telebot.types.InlineKeyboardButton('Лайка', callback_data='4444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №4) Как звали собаку, первой побывавшей в космосе на советском спутнике «Спутник-2» в 1957 году?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['1111', '2222', '3333', '4444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '1111':
        response_text = '*Вы не правы!* На Землю, к огромному сожалению, она вернуться не смогла. Лайка показала, что живое существо может пережить запуск на орбиту и невесомость. 11 апреля 2008 года в Москве на Петровско-Разумовской аллее на территории Института военной медицины, где готовился космический эксперимент, был установлен памятник Лайке. Двухметровый памятник представляет собой космическую ракету, переходящую в ладонь, на которой гордо стоит Лайка.'
    elif call.data == '2222':
        response_text = '*Вы не правы!* На Землю, к огромному сожалению, она вернуться не смогла. Лайка показала, что живое существо может пережить запуск на орбиту и невесомость. 11 апреля 2008 года в Москве на Петровско-Разумовской аллее на территории Института военной медицины, где готовился космический эксперимент, был установлен памятник Лайке. Двухметровый памятник представляет собой космическую ракету, переходящую в ладонь, на которой гордо стоит Лайка.'
    elif call.data == '3333':
        response_text = 'vВы не правы!* На Землю, к огромному сожалению, она вернуться не смогла. Лайка показала, что живое существо может пережить запуск на орбиту и невесомость. 11 апреля 2008 года в Москве на Петровско-Разумовской аллее на территории Института военной медицины, где готовился космический эксперимент, был установлен памятник Лайке. Двухметровый памятник представляет собой космическую ракету, переходящую в ладонь, на которой гордо стоит Лайка.'
    elif call.data == '4444':
        response_text = '*Вы правы!* На Землю, к огромному сожалению, она вернуться не смогла. Лайка показала, что живое существо может пережить запуск на орбиту и невесомость. 11 апреля 2008 года в Москве на Петровско-Разумовской аллее на территории Института военной медицины, где готовился космический эксперимент, был установлен памятник Лайке. Двухметровый памятник представляет собой космическую ракету, переходящую в ладонь, на которой гордо стоит Лайка.'
        ch += 1

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Мушка', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Стрелка', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌Белка', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('✅Лайка', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina5(call.message)

def victorina5(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('2', callback_data='11111')
    button_menu2 = telebot.types.InlineKeyboardButton('4', callback_data='22222')
    button_menu3 = telebot.types.InlineKeyboardButton('6', callback_data='33333')
    button_menu4 = telebot.types.InlineKeyboardButton('8', callback_data='44444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №5) Над какой цифрой на стандартной клавиатуре компьютера расположена «собака»?', reply_markup=button_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['11111', '22222', '33333', '44444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '11111':
        response_text = '*Вы правы!* Конечно же рядом с цифрой 2 на клавиатуре'
        ch += 1
    elif call.data == '22222':
        response_text = '*Вы не правы!* Конечно же рядом с цифрой 2 на клавиатуре'
    elif call.data == '33333':
        response_text = '*Вы не правы!* Конечно же рядом с цифрой 2 на клавиатуре'
    elif call.data == '44444':
        response_text = '*Вы не правы!* Конечно же рядом с цифрой 2 на клавиатуре'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('✅2', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌4', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌6', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌8', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina6(call.message)

def victorina6(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('На льва', callback_data='111111')
    button_menu2 = telebot.types.InlineKeyboardButton('На мишку', callback_data='222222')
    button_menu3 = telebot.types.InlineKeyboardButton('На овцу', callback_data='333333')
    button_menu4 = telebot.types.InlineKeyboardButton('На свинью', callback_data='444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №6) На кого внешне похожа собака породы бедлингтон-терьер?', reply_markup=button_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['111111', '222222', '333333', '444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '111111':
        response_text = '*Вы не правы!* Бедлингтон-терьер внешне напоминает овечку, а точнее, ягненка, с элементами, напоминающими пуделя. Его выделяют кудрявая шерсть, грушевидная голова, изогнутая спина и изящные движения. '
    elif call.data == '222222':
        response_text = '*Вы не правы!* Бедлингтон-терьер внешне напоминает овечку, а точнее, ягненка, с элементами, напоминающими пуделя. Его выделяют кудрявая шерсть, грушевидная голова, изогнутая спина и изящные движения. '
    elif call.data == '333333':
        response_text = '*Вы правы!* Бедлингтон-терьер внешне напоминает овечку, а точнее, ягненка, с элементами, напоминающими пуделя. Его выделяют кудрявая шерсть, грушевидная голова, изогнутая спина и изящные движения. '
        ch += 1
    elif call.data == '444444':
        response_text = '*Вы не правы!* Бедлингтон-терьер внешне напоминает овечку, а точнее, ягненка, с элементами, напоминающими пуделя. Его выделяют кудрявая шерсть, грушевидная голова, изогнутая спина и изящные движения. '

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌На льва', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌На мишку', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('✅На овцу', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌На свинью', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina7(call.message)

def victorina7(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Такса', callback_data='1111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Бульдог', callback_data='2222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Пудель', callback_data='3333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Дог', callback_data='4444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №7) У собак какой породы есть признанные стандартом окрасы: чёрный, белый, коричневый, абрикосовый, серебристый и красный?', reply_markup=button_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['1111111', '2222222', '3333333', '4444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '1111111':
        response_text = '*Вы не правы!* Помимо перечисленных, к стандарту пуделей также относятся и другие цвета, такие как серый, а также различные вариации, включая двухцветные окрасы, тигровый и окрасы с подпалом. '
    elif call.data == '2222222':
        response_text = '*Вы не правы*! Помимо перечисленных, к стандарту пуделей также относятся и другие цвета, такие как серый, а также различные вариации, включая двухцветные окрасы, тигровый и окрасы с подпалом. '
    elif call.data == '3333333':
        response_text = '*Вы правы!* Помимо перечисленных, к стандарту пуделей также относятся и другие цвета, такие как серый, а также различные вариации, включая двухцветные окрасы, тигровый и окрасы с подпалом. '
        ch += 1
    elif call.data == '4444444':
        response_text = '*Вы не правы!* Помимо перечисленных, к стандарту пуделей также относятся и другие цвета, такие как серый, а также различные вариации, включая двухцветные окрасы, тигровый и окрасы с подпалом. '

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Такса', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Бульдог', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('✅Пудель', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌Дог', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina8(call.message)

def victorina8(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Такса', callback_data='11111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Мопс', callback_data='22222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Пудель', callback_data='33333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Дог', callback_data='44444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №8) В начале 1900-х гг., когда появились первые хот-доги, художник Тед Дорган нарисовал их первую рекламу — собаку, заложенную в огромную булку. А какой породы была эта собака?', reply_markup=button_menu)


@bot.callback_query_handler(func=lambda call: call.data in ['11111111', '22222222', '33333333', '44444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '11111111':
        response_text = '*Вы правы!* Она из собак больше всего похожа на сосиску.'
        ch+=1
    elif call.data == '22222222':
        response_text = '*Вы не правы!* Она из собак больше всего похожа на сосиску.'
    elif call.data == '33333333':
        response_text = '*Вы не правы!* Она из собак больше всего похожа на сосиску.'
    elif call.data == '44444444':
        response_text = '*Вы не правы!* Она из собак больше всего похожа на сосиску.'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('✅Такса', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Мопс', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌Пудель', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌Дог', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina9(call.message)

def victorina9(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Франция', callback_data='111111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Германия', callback_data='222222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Польша', callback_data='333333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Испания', callback_data='444444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №9) Какая европейская страна дала название породе собак спаниель?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['111111111', '222222222', '333333333', '444444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '111111111':
        response_text = '*Вы не правы!* Название породы собак «спаниель» происходит от Испании. Слово «spaniel» происходит от старофранцузского espaigneul, что означает «испанская (собака)», и в конечном итоге от латинского Hispaniolus — «испанский».'
    elif call.data == '222222222':
        response_text = '*Вы не правы!* Название породы собак «спаниель» происходит от Испании. Слово «spaniel» происходит от старофранцузского espaigneul, что означает «испанская (собака)», и в конечном итоге от латинского Hispaniolus — «испанский».'
    elif call.data == '333333333':
        response_text = '*Вы не правы!* Название породы собак «спаниель» происходит от Испании. Слово «spaniel» происходит от старофранцузского espaigneul, что означает «испанская (собака)», и в конечном итоге от латинского Hispaniolus — «испанский».'
    elif call.data == '444444444':
        response_text = '*Вы правы!* Название породы собак «спаниель» происходит от Испании. Слово «spaniel» происходит от старофранцузского espaigneul, что означает «испанская (собака)», и в конечном итоге от латинского Hispaniolus — «испанский».'
        ch += 1
    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Франция', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Германия', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌Польша', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('✅Испания', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina10(call.message)

def victorina10(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Пудель', callback_data='1111111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Английский сеттер', callback_data='2222222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Ирландский терьер', callback_data='3333333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Русская борзая', callback_data='4444444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №10) Назовите породу Белого Бима Чёрное Ухо из повести воронежского писателя Г. Троепольского?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['1111111111', '2222222222', '3333333333', '4444444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '1111111111':
        response_text = '*Вы не правы!* Порода собаки из фильма «Белый Бим Черное ухо» – английский сеттер.'
    elif call.data == '2222222222':
        response_text = '*Вы правы!* Порода собаки из фильма «Белый Бим Черное ухо» – английский сеттер.'
        ch += 1
    elif call.data == '3333333333':
        response_text = '*Вы не правы!* Порода собаки из фильма «Белый Бим Черное ухо» – английский сеттер.'
    elif call.data == '4444444444':
        response_text = '*Вы не правы!* Порода собаки из фильма «Белый Бим Черное ухо» – английский сеттер.'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Пудель', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('✅Английский сеттер', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌Ирландский терьер', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌Русская борзая', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina11(call.message)

def victorina11(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Плаванием', callback_data='11111111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Футболом', callback_data='22222222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Велогонкой', callback_data='33333333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Фотоохотой', callback_data='44444444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №11) Каким видом спорта занимался Шарик из деревни Простоквашино?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['11111111111', '22222222222', '33333333333', '44444444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '11111111111':
        response_text = '*Вы не правы!* _"А давайте я вас на память из фоторужья щёлкну!"_'
    elif call.data == '22222222222':
        response_text = '*Вы не правы!* _"А давайте я вас на память из фоторужья щёлкну!"_'
    elif call.data == '33333333333':
        response_text = '*Вы не правы!* _"А давайте я вас на память из фоторужья щёлкну!"_'
    elif call.data == '44444444444':
        response_text = '*Вы правы!* _"А давайте я вас на память из фоторужья щёлкну!"_'
        ch += 1

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Пудель', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Футболом', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('❌Велогонкой', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('✅Фотоохотой', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    victorina12(call.message)

def victorina12(message):
    button_menu = telebot.types.InlineKeyboardMarkup()
    button_menu1 = telebot.types.InlineKeyboardButton('Овчарки', callback_data='111111111111')
    button_menu2 = telebot.types.InlineKeyboardButton('Хаски', callback_data='222222222222')
    button_menu3 = telebot.types.InlineKeyboardButton('Чихуахуа', callback_data='333333333333')
    button_menu4 = telebot.types.InlineKeyboardButton('Русская борзая', callback_data='444444444444')

    button_menu.row(button_menu1, button_menu2)
    button_menu.row(button_menu3, button_menu4)

    bot.send_message(message.chat.id,'Вопрос №12) Собаки какой породы являются одними из самых долгоживущих?', reply_markup=button_menu)

@bot.callback_query_handler(func=lambda call: call.data in ['111111111111', '222222222222', '333333333333', '444444444444'])
def handle_third_question(call):
    global ch
    response_text = ""
    if call.data == '111111111111':
        response_text = '*Вы не правы!* Маленькие собаки этой породы часто доживают до 15 лет и более, а некоторые могут прожить и до 20 лет.'
    elif call.data == '222222222222':
        response_text = '*Вы не правы!* Маленькие собаки этой породы часто доживают до 15 лет и более, а некоторые могут прожить и до 20 лет.'
    elif call.data == '333333333333':
        response_text = '*Вы правы!* Маленькие собаки этой породы часто доживают до 15 лет и более, а некоторые могут прожить и до 20 лет.'
        ch += 1
    elif call.data == '444444444444':
        response_text = '*Вы не правы!* Маленькие собаки этой породы часто доживают до 15 лет и более, а некоторые могут прожить и до 20 лет.'

    # Создаем новую клавиатуру с значками
    new_button_menu = telebot.types.InlineKeyboardMarkup()
    new_button_yes = telebot.types.InlineKeyboardButton('❌Овчарки', callback_data='yes')
    new_button_no1 = telebot.types.InlineKeyboardButton('❌Хаски', callback_data='no1')
    new_button_no2 = telebot.types.InlineKeyboardButton('✅Чихуахуа', callback_data='no2')
    new_button_no3 = telebot.types.InlineKeyboardButton('❌Сенбернары', callback_data='no3')

    new_button_menu.row(new_button_yes, new_button_no1)
    new_button_menu.row(new_button_no2, new_button_no3)

    # Обновляем сообщение с новой клавиатурой
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response_text, reply_markup=new_button_menu, parse_mode='Markdown')
    the_end(call.message)

def the_end(message):
    global ch
    global name
    s = ''
    if ch == 1:
        s = 'балл'
    elif ch == 2 or ch == 3 or ch ==4:
        s = 'балла'
    else:
        s = 'баллов'
    result_button = telebot.types.InlineKeyboardMarkup()
    result_button1 = telebot.types.InlineKeyboardButton('Таблица участников', callback_data='result')
    result_button.row(result_button1)
    bot.send_message(message.chat.id,f'Поздравляю, {name}, вы прошли викторину на {ch} {s} из 12, это отличный результат!', reply_markup=result_button)



@bot.callback_query_handler(func=lambda call: call.data in ['result'])
def handle_third_question(call):
    global user_id
    global ch



    conn = sqlite3.connect('clients.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if user is None:
        print(f"Пользователь с ID {user_id} не найден.")

    try:
        cur.execute('UPDATE users SET score = ? WHERE id = ?', (ch, user_id))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")



    conn.commit()

    # Теперь получаем всех пользователей
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    information = ''
    for el in users:
        information += f'Имя: {el[1]}, Кол-во баллов: {el[2]} из 12\n'

    cur.close()
    conn.close()

    if len(information) > 0:
        bot.send_message(call.message.chat.id, information)
    else:
        bot.send_message(call.message.chat.id, 'Пока что никто из пользователей не прошел викторину')
















if __name__ == '__main__':
    bot.polling(none_stop=True)

