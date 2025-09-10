import telebot
import random
from time import sleep
from main2 import is_admin, ADMIN_USER
from telebot import types

bot = telebot.TeleBot('8452848990:AAEdqyU2aqM0FeueUeGsg4pPtZCwLPrz3Ag')

#Глобальные перемнные
active_game = False
secret_number = 0
start_number = 0
play_number =  0
stop_numder = 0
X = 10

@bot.message_handler(commands=['start'])
def start(message):
    global start_number
    start_number += 1
    bot.send_message(message.chat.id, 'VECTORBOT')
    sleep(1)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} '
                                    f'это бот для угадывания чисел. Напишите команду /play, что бы начать игру!')
@bot.message_handler(commands=['admins'])
def admins_users(message):
    bot.send_message(message.chat.id, f'Сейчас администраторы на посту: {ADMIN_USER}')

@bot.message_handler(commands=['admin_panel'])
def admin_panel_bot(message):
    if is_admin(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        stats = types.InlineKeyboardButton('Статистика', callback_data='stats1')
        markup.add(stats)
        bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Команда недоступна вам!')

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'stats1':
            bot.send_message(call.message.chat.id, f'За все время запускали бота {start_number} и играли в игру {play_number}.')

@bot.message_handler(commands=['help'])
def info_bot(message):
    if is_admin(message):
        bot.send_message(message.chat.id, f'{message.from_user.first_name} вам доступные стандартные вид команд  /start, /play, /help'
                                          f'и доступны вам администратору команды /admin_panel')
    else:
        bot.send_message(message.chat.id, 'Список команд /start, /play, /help')

@bot.message_handler(commands=['play'])
def play_start(message, x=X):
    global  play_number, active_game
    play_number += 1
    active_game = True
    bot.send_message(message.chat.id, f'Угадай число от 1 до {x}. Введите число')

@bot.message_handler()
def an_chek(message, x=X):
    global secret_number, active_game
    if not active_game:
        return

    try:
        num = int(message.text)
        if 1 <= num <= x:
          secret_number = random.randint(1, x)
          if num == secret_number:
              bot.reply_to(message, f'Ты угадал')
          else:
              bot.reply_to(message, f'Не угадал! Число {secret_number}')
              active_game = False
        else:
            bot.reply_to(message, f'Число должно быть от 1 до {x}')
    except ValueError:
          bot.reply_to(message, 'Пожалуйста введите корректное число!')

print('Бот запущен!')
bot.polling(non_stop=True)