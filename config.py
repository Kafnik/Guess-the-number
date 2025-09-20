
TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'

#User_name администраторов
ADMIN_USER = 'Kafnik'

 # Функция проверки администратора
def is_admin(message):
    return message.from_user.first_name in ADMIN_USER