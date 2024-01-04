import telebot
import math
import time

token = "Token"
bot = telebot.TeleBot(token, parse_mode='html')

value = ''
old_value = ''
keybord = telebot.types.InlineKeyboardMarkup()
keybord.row( telebot.types.InlineKeyboardButton('🧹', callback_data='c'),
             telebot.types.InlineKeyboardButton('◀️', callback_data='<='),
             telebot.types.InlineKeyboardButton('o/a', callback_data='oa'),
             telebot.types.InlineKeyboardButton('o/g', callback_data='og'),
             telebot.types.InlineKeyboardButton('➗', callback_data='/') )

keybord.row( telebot.types.InlineKeyboardButton('7️⃣', callback_data='7'), 
             telebot.types.InlineKeyboardButton('8️⃣', callback_data='8'),
             telebot.types.InlineKeyboardButton('9️⃣', callback_data='9'),
             telebot.types.InlineKeyboardButton('✖️', callback_data='*') )

keybord.row( telebot.types.InlineKeyboardButton('4️⃣', callback_data='4'), 
             telebot.types.InlineKeyboardButton('5️⃣', callback_data='5'),
             telebot.types.InlineKeyboardButton('6️⃣', callback_data='6'),
             telebot.types.InlineKeyboardButton('➖', callback_data='-') )

keybord.row( telebot.types.InlineKeyboardButton('1️⃣', callback_data='1'), 
             telebot.types.InlineKeyboardButton('2️⃣', callback_data='2'),
             telebot.types.InlineKeyboardButton('3️⃣', callback_data='3'),
             telebot.types.InlineKeyboardButton('➕', callback_data='+') )

keybord.row( telebot.types.InlineKeyboardButton('+/-', callback_data='pm'), 
             telebot.types.InlineKeyboardButton('0️⃣', callback_data='0'),
             telebot.types.InlineKeyboardButton(',', callback_data=','),
             telebot.types.InlineKeyboardButton('🟰', callback_data='=') )

@bot.message_handler(commands=['start', 'calc'])
def getMessage(message):
    if(message.text == '/start'):
        bot.reply_to(message, "Hi 👋🏻 This is a calculator bot for Telegram\n\n👉🏻 Send /calc command to start the calculator!")
    elif (message.text == '/calc'):
        global value
        if value == '':
            bot.send_message(message.from_user.id, "0", reply_markup=keybord)
        else:
            bot.send_message(message.from_user.id, value, reply_markup=keybord)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == 'no':
        pass
    elif data == 'oa':
        list  = value.strip(',').split(',')
        res = ''
        for index in list:
            res += index + "+"

        value = str(eval(res.strip('+')) / len(list))
    elif data == 'og':
        list  = value.strip(',').split(',')
        res = ''
        for index in list:
            res += index + "*"

        value = str(math.pow(eval(res.strip('*')), (1 / len(list))))
    elif data == 'c':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value) - 1]
    elif data == 'pm':
        value = str(-1 * eval(value))
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'Error!' 
    else:
        value += data

    if ( value != old_value and value != '' ) or ('0' != old_value and value == '' ):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keybord)
            old_value = '0'
        else: 
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keybord)
            old_value = value
    
    if value == 'Error!' : value = '0'

while True:
    try:
        belgi = True
        bot.polling(none_stop=True)
    except Exception as e:
        if belgi == True:
            bot.send_message('admin telegram user id', f'<b>Server Error ❗️</b>\n\n<b>Content:</b>\n<code>{e}</code>')
            belgi = False
        time.sleep(5)