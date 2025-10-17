import telebot
import random
from time import sleep
from config import is_admin, ADMIN_USER, TELEGRAM_TOKEN
from telebot import types

bot = telebot.TeleBot(TELEGRAM_TOKEN)

#---------Главные переменные--------
VERSION = '1.3'
error = True
active_game = False
events = [ 
        "Ты нашёл светящуюся тыкву 🎃",
        "Призрак прошёл сквозь тебя 👻",
        "Тебя укусил зомби 🧟",
        "Ведьма угостила зельем 💀",
        "Ты сбежал от чёрной кошки 🐈‍⬛",
        "Ты услышал шёпот из темноты 😱",
        "Ты получил подарок от скелета ☠️",
        "Ты поймал летучую мышь 🦇"]
nasty = ["😝Гадость", "🍬Сладость"]
hearts = 5
x = 10

def hallowen(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    tp1 = types.InlineKeyboardButton('🎡Колесо ужасов', callback_data='btn1')
    tp2 = types.InlineKeyboardButton('🍬Сладость или гадость', callback_data='btn2')
    markup.add(tp1, tp2)
    bot.send_message(message.chat.id, f'Вот все игры на Хэллуин', reply_markup=markup)

def complet_games(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🎡Колесо ужасов', callback_data='btn1')
    btn2 = types.InlineKeyboardButton('🍬Сладость или гадость', callback_data='btn2')
    btn3 = types.InlineKeyboardButton('Отгодай число', callback_data='btn3')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, '✅ Игра завершена ! Выберете команду 👇', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '❌У бота ведутся тех.работы не отвлекайте нас. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    msg = bot.send_message(message.chat.id, 'OpenbotAI')
    sleep(1)
    bot.edit_message_text(f'Привет {message.from_user.first_name}. \nГотов побеждать Тьму ! Если да то напиши /games', message_id=msg.message_id, chat_id=message.chat.id)
   
#---------------Меню игр-----------------
@bot.message_handler(commands=['halloween'])
def bot_commads_user(message):
    hallowen(message)

@bot.message_handler(commands=['games'])
def menu_games(message):
    if not error:
     bot.send_message(message.chat.id, '❌У бота ведутся тех.работы не отвлекайте нас. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🎡Колесо ужасов', callback_data='btn1')
        btn2 = types.InlineKeyboardButton('🍬Сладость или гадость', callback_data='btn2')
        btn3 = types.InlineKeyboardButton('Отгодай число', callback_data='btn3')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Меню игр открыто !', reply_markup=markup)

@bot.callback_query_handler(func=lambda m: True)
def callback(call):
    if call.data == 'btn1':
        num = random.choice(events)
        bot.send_message(call.message.chat.id, f'🎡*Колесо крутиться...*\n\n {num}', parse_mode="Markdown")
        sleep(1)
        bot.answer_callback_query(call.id)
        complet_games(call.message)

    elif call.data == 'btn2':
        num = random.choice(nasty)
        bot.send_message(call.message.chat.id, f'Тебе выподает: {num}')
        sleep(1)
        bot.answer_callback_query(call.id)
        complet_games(call.message)

    elif call.data == 'sistem1':
        error = False
        bot.send_message(call.message.chat.id, f'Бот переведенн в тех.работы')

    elif call.data == 'btn3':
        global active_game
        active_game = True
        bot.send_message(call.message.chat.id, f'🕷Игра началась! Я загадал число от 1 до {x} \n У тебя есть 5 жизней !')

@bot.message_handler(commands=['sistem'])
def sistem(message):
    if not is_admin (message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        num1 = types.InlineKeyboardButton('Отключение на техработы', callback_data='sistem1')
        markup.add(num1)
        bot.message_message(message.chat.id, f'Выбирите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '❌Эта команда вам не доступна !')

@bot.message_handler(commands=['help'])
def info_bot(message):
    if not error(message): 
        bot.reply_to(message, '❌У бота ведутся тех.работы не отвлекайте нас. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.send_message(message.chat.id, 'Список команд /start, /games, /help, /helloween')

@bot.message_handler(commands=['info'])
def info_bot(message):
    if not is_admin(message): 
        bot.reply_to(message, '❌У бота ведутся тех.работы не отвлекайте нас. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.send_message(message.chat.id, f'Бот cделан команиями: OpenbotAI и VECTORBOT \nНо большую чать выполнила комания: OpenbotAI \nЧто есть прикольного, команда /halloween. \nВерсия бота: {VERSION}')


@bot.message_handler(func=lambda message: True)
def message_bot_int(message):
    global hearts, active_game, x
    if not active_game: 
        return
    
    try:
        guess = int(message.text)

        if 1 <= guess <= x:
            secret = random.randint(1, x)
            if guess == secret:
                bot.reply_to(message, f'🎉Ты победил тьму и угодал число {secret}')
                active_game = False
                sleep(1)
                complet_games(message)
            else:
                hearts -= 1
                if hearts == 0:
                    bot.reply_to(message, f'💀 Ты проиграл.... Тьма поглотила тебя !\n число {secret}. \n Если хочешь отомсти судьбе ? Напиши /games')
                    sleep(1)                    
                    complet_games(message)
                    hearts = 5
                    active_game = False
                else:
                 bot.reply_to(message, f'💀Осталось жизней: {hearts}')
        else:
            bot.reply_to(message, f'🦇Число должно быть 1 до {x}')

    except ValueError:
         bot.reply_to(message, "👻 Это не число... Призраки не понимают слов !'")



print('Бот угодай число запущен!')
bot.polling(non_stop=True)