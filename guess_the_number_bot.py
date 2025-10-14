import telebot
import random
from time import sleep
from config import is_admin, ADMIN_USER, TELEGRAM_TOKEN
from telebot import types

bot = telebot.TeleBot(TELEGRAM_TOKEN)

#Глобальные перемнные
admin_down = False
user_update = []
VERSION = '1.2'
active_game = False
secret_number = 0
start_number = 0
play_number =  0
stop_numder = 0
X = 5

@bot.message_handler(commands=['start'])
def start(message):
    if not is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        chat_id = message.chat.id
        user_update.append(chat_id)
        bot.send_message(message.chat.id, 'OpenbotAI')
        sleep(1)
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}. \nЭто бот для угадывания чисел. Напишите команду /play, что бы начать игру!')
   
 

@bot.message_handler(commands=['credit'])
def credit_user(message):
    if not  is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.reply_to(message, 'В следущих обновлениях !')


@bot.message_handler(commands=['update'])
def updute_user(message):
    if not is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
          text = f'Обновление: {VERSION} \nДобавлинно много команд, добавили команду /info. \nИзминили угадывание чисел на 10 было 100. \nОстольное системное.'
    for chat_id in user_update:
        try:
            bot.send_message(chat_id, text)
        except Exception as e:
            bot.reply_to(message, f'Не удолось оправить {chat_id}: {e}')

@bot.message_handler(commands=['admins'])
def admins_users(message):
    if not is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.send_message(message.chat.id, f'Сейчас администраторы на посту: \n{ADMIN_USER}')

@bot.message_handler(commands=['admin_panel'])
def admin_panel_bot(message):
    global admin_down
    if not is_admin(message):
        bot.reply_to(message, 'Команда недоступна вам!')
        return
    
    if not admin_down:
        bot.reply_to(message, 'Ошибка админ панель временно не работает!') 
        return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    stats = types.InlineKeyboardButton('Статистика', callback_data='stats1')
    markup.add(stats)
    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'stats1':
            bot.send_message(call.message.chat.id, f'За все время запускали бота: \n{start_number} \n и играли в игру: \n{play_number}')

@bot.message_handler(commands=['help'])
def info_bot(message):
    if not is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.send_message(message.chat.id, 'Список команд /start, /play, /help')

@bot.message_handler(commands=['play'])
def play_start(message, x=X):
    if not is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        global  play_number, active_game
    play_number += 1
    active_game = False
    bot.send_message(message.chat.id, f'Угадай число от 1 до {x}. Введите число')

@bot.message_handler(commands=['info'])
def info_bot(message):
    if is_admin(message): 
        bot.reply_to(message, '❌Бот прекратил работу на не определеное время. Нам жаль вся информация на канеле: https://t.me/+xtbO7MiUA180NzYy')
    else:
        bot.send_message(message.chat.id, f'Бот cделан команиями: OpenbotAI и VECTORBOT \nНо большую чать выполнила комания: OpenbotAI \nЧто есть прикольного, команда /credit. \nВерсия бота: {VERSION}')

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
              bot.reply_to(message, f'Ты угадал !')
          else:
              bot.reply_to(message, f'Не угадал! Число {secret_number}')
              active_game = False
        else:
            bot.reply_to(message, f'Число должно быть от 1 до {x}')
    except ValueError:
          bot.reply_to(message, 'Пожалуйста введите корректное число!')

print('Бот угодай число запущен!')
bot.polling(non_stop=True)