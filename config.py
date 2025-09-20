
TELEGRAM_TOKEN = '8452848990:AAEdqyU2aqM0FeueUeGsg4pPtZCwLPrz3Ag'

#User_name администраторов
ADMIN_USER = 'Kafnik'

 # Функция проверки администратора
def is_admin(message):
    return message.from_user.first_name in ADMIN_USER